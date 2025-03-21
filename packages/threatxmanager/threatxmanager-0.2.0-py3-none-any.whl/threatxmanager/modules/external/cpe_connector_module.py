import datetime
import json
import math
import time
from typing import Any
from uuid import uuid4

import langcodes
import requests
import stix2
from requests.adapters import HTTPAdapter
from sqlalchemy.orm import sessionmaker
from urllib3.util import Retry

from threatxmanager.base_module.base_module import BaseModule
from threatxmanager.base_module.strix_serveses import Stix2Services, STIXWrapper
from threatxmanager.config.manager_config import Config
from threatxmanager.dbmanager.modules_models.cper_model import CPERecord

APP_VERSION: str = "1.0.0"


class CPEConnectorModule(BaseModule):
    """
    Module responsible for collecting CPE (Common Platform Enumeration) data from the NIST API
    and storing it in the database. This module uses configuration, logging, and database management
    features inherited from BaseModule

    Process Flow:
        1. Initialization: Loads necessary configuration and creates an instance of Stix2Services.
        2. Interval Conversion: Converts the configured interval string to seconds (_get_interval).
        3. URL Construction: Builds API URLs based on index and optional date filters.
        4. API Request: Retrieves pagination parameters and the list of CPEs from the NIST API.
        5. Data Processing: Converts the returned JSON into CPERecord instances by extracting information
           such as hardware flag, vendor, name, version, and language (_get_cpe_infos).
        6. Persistence and STIX Conversion: Saves raw API data to the database and converts the records
           to custom STIX objects (x-cpe-record) via Stix2Services.
        7. Paginated Import: Processes data page by page (_import_page) and iterates sequentially (_import_all).
        8. Execution: The run() method triggers the complete import process.

    The class utilizes type annotations to improve code clarity and adheres to the NumPy docstring standard.
    """

    def __init__(
        self,
        config_instance: Config | None = None,
        log_manager_instance: Any = None,
        db_instance: Any = None,
        env: str | None = None,
    ) -> None:
        """
        Initialize the CPEConnectorModule with dependency injection for configuration, logging, and database access.

        Parameters
        ----------
        config_instance : Optional[Config], optional
            Configuration instance, by default None.
        log_manager_instance : Any, optional
            Logging manager instance, by default None.
        db_instance : Any, optional
            Database manager instance, by default None.
        env : Optional[str], optional
            Execution environment, by default None.

        Raises
        ------
        ValueError
            If any required configuration parameters (base_url, api_key, or interval) are missing.
        """
        super().__init__(
            config_instance=config_instance,
            log_manager_instance=log_manager_instance,
            db_instance=db_instance,
            env=env,
        )
        self.base_url: str = self.module_config.get("base_url")
        self.api_key: str = self.module_config.get("api_key")
        self.interval: str = self.module_config.get("interval")
        if not self.base_url or not self.api_key or not self.interval:
            self.logger.error("Missing configuration parameters for the CPE connector.")
            raise ValueError("Missing configuration parameters for the CPE connector.")
        self.logger.info("CPEConnectorModule initialized successfully.")

        # Instantiate Stix2Services for managing STIX objects.
        self.stix2_services = Stix2Services(
            persist_file=None,
            db_manager=self.db_manager,
            log_manager=self.log_manager,
            config=self.config,
        )

    def _get_interval(self) -> int:
        """
        Convert the configured interval (string) into seconds.

        Returns
        -------
        int
            The interval converted into seconds.

        Raises
        ------
        ValueError
            If the interval unit is invalid or conversion fails.
        """
        unit: str = self.interval[-1]
        value: str = self.interval[:-1]
        try:
            if unit == "h":
                return int(value) * 3600
            if unit == "s":
                return int(value)
            raise ValueError("Invalid interval unit.")
        except Exception as err:
            self.logger.error(f"Error converting interval '{self.interval}': {err!s}")
            raise ValueError(f"Error converting interval '{self.interval}'.") from err

    def _get_request_params(self, api_url: str) -> dict[str, Any]:
        """
        Make an API request to obtain pagination parameters.

        Parameters
        ----------
        api_url : str
            The API URL to obtain the parameters from.

        Returns
        -------
        Dict[str, Any]
            A dictionary containing 'resultsPerPage', 'startIndex', and 'totalResults' returned by the API.
            Returns an empty dictionary in case of an error.
        """
        self.logger.info("Retrieving API request parameters...")
        session = requests.Session()
        headers: dict[str, str] = {
            "api_key": self.api_key,
            "User-Agent": f"CPEConnectorModule/{APP_VERSION}",
        }
        retry_strategy = Retry(
            total=4,
            backoff_factor=6,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)

        response = session.get(api_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            params: dict[str, Any] = {
                "resultsPerPage": data.get("resultsPerPage"),
                "startIndex": data.get("startIndex"),
                "totalResults": data.get("totalResults"),
            }
            self.logger.info("API request parameters retrieved successfully.")
            return params
        self.logger.error(f"Error retrieving API parameters: {response.status_code}")
        return {}

    def _get_cpe_list(self, api_url: str) -> dict[str, Any]:
        """
        Make an API request to retrieve the list of CPEs.

        Parameters
        ----------
        api_url : str
            The API URL to obtain the CPE list.

        Returns
        -------
        Dict[str, Any]
            A dictionary with the JSON data returned by the API.
            In case of an error, returns an empty dictionary.
        """
        self.logger.debug(f"Making API request to: {api_url}")
        session = requests.Session()
        headers: dict[str, str] = {
            "api_key": self.api_key,
            "User-Agent": f"CPEConnectorModule/{APP_VERSION}",
        }
        retry_strategy = Retry(
            total=4,
            backoff_factor=6,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)

        response = session.get(api_url, headers=headers)
        if response.status_code == 200:
            self.logger.info(f"{response.json().get('resultsPerPage')} CPEs retrieved.")
            return response.json()
        self.logger.error(f"Error retrieving CPE list: {response.status_code}")
        return {}

    def _get_date_iso(self, timestamp: int) -> str:
        """
        Convert a timestamp to an ISO-formatted date string in UTC.

        Parameters
        ----------
        timestamp : int
            The timestamp value.

        Returns
        -------
        str
            ISO 8601 formatted date (UTC).
        """
        return datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc).isoformat()

    def _get_id(self, obj_type: str) -> str:
        """
        Generate a unique identifier for an object using uuid4.

        Parameters
        ----------
        obj_type : str
            The type of object for which to generate the ID.

        Returns
        -------
        str
            A unique identifier in the format 'obj_type--UUID'.
        """
        return f"{obj_type}--{uuid4()}"

    def _get_api_url(self, start_index: int, start_date: str | None, end_date: str | None) -> str:
        """
        Build the API URL based on provided parameters.

        Parameters
        ----------
        start_index : int
            The starting index for pagination.
        start_date : Optional[str]
            The start date for filtering (ISO format) or None if not used.
        end_date : Optional[str]
            The end date for filtering (ISO format) or None if not used.

        Returns
        -------
        str
            The complete API URL.
        """
        if start_date is None and end_date is None:
            return f"{self.base_url}?startIndex={start_index}"
        return f"{self.base_url}?startIndex={start_index}&lastModStartDate={start_date}&lastModEndDate={end_date}"

    def _get_cpe_infos(self, cpe: str) -> dict[str, Any]:
        """
        Extract detailed information from the CPE string, including hardware flag, vendor,
        name, version, and language.

        Parameters
        ----------
        cpe : str
            The CPE string in standard format.

        Returns
        -------
        Dict[str, Any]
            A dictionary with the following keys:
                - is_hardware: bool
                - vendor: str
                - name: str
                - version: str
                - language: str
        """
        parts = cpe.split(":")
        is_hardware: bool = parts[2] == "h"
        vendor: str = "" if parts[3] == "*" else parts[3]
        name: str = "" if parts[4] == "*" else parts[4].replace("_", " ")
        version: str = "" if parts[5] == "*" else parts[5]
        language: str = ""
        if len(parts) > 8:
            lang_candidate: str = parts[8].strip()
            if lang_candidate == "*" and len(parts) > 9:
                lang_candidate = parts[9].strip()
            if lang_candidate.lower() in {"address", "email", "premium"} or not (
                lang_candidate.isalpha() and 1 <= len(lang_candidate) <= 8
            ):
                language = ""
            else:
                try:
                    language = langcodes.standardize_tag(lang_candidate, "ietf")
                except Exception as err:
                    self.logger.error(f"Error standardizing language: {err}")
                    language = ""
        return {
            "is_hardware": is_hardware,
            "vendor": vendor,
            "name": name,
            "version": version,
            "language": language,
        }

    def _json_to_cpe_records(self, json_objects: dict[str, Any]) -> list[CPERecord]:
        """
        Convert the JSON object returned by the API into a list of CPERecord instances.
        The raw CPE data is stored in the 'raw_data' field as a dictionary.

        Parameters
        ----------
        json_objects : Dict[str, Any]
            JSON object containing CPE data obtained from the API.

        Returns
        -------
        List[CPERecord]
            A list of processed and filtered CPE records.
        """
        self.logger.info("Converting JSON objects to CPE records...")
        nb_results: int = json_objects.get("resultsPerPage", 0)
        records: list[CPERecord] = []
        products: list[dict[str, Any]] = json_objects.get("products", [])
        for i in range(nb_results):
            product: dict[str, Any] = products[i]
            cpe_data: dict[str, Any] = product.get("cpe", {})
            cpe_name: str = cpe_data.get("cpeName", "")
            cpe_infos: dict[str, Any] = self._get_cpe_infos(cpe_name)
            # Process only if the CPE is not deprecated and is not hardware.
            if cpe_data.get("deprecated") is False and not cpe_infos["is_hardware"]:
                record = CPERecord(
                    id=self._get_id("cpe-record"),
                    cpe=cpe_name,
                    is_hardware=cpe_infos["is_hardware"],
                    vendor=cpe_infos["vendor"],
                    name=self._get_cpe_title(cpe_data),
                    version=cpe_infos["version"],
                    language=cpe_infos["language"],
                    raw_data=cpe_data,
                )
                records.append(record)
        self.logger.info(f"{len(records)} CPE records created.")
        return records

    def _get_cpe_title(self, cpe: dict[str, Any]) -> str:
        """
        Extract the CPE title (name) from the available titles in the dictionary.

        Parameters
        ----------
        cpe : Dict[str, Any]
            Dictionary containing CPE data.

        Returns
        -------
        str
            The CPE title. If no English title is found, uses the name extracted by _get_cpe_infos.
        """
        cpe_title: str = ""
        for title in cpe.get("titles", []):
            if title.get("lang") == "en":
                cpe_title = title.get("title", "")
                break
        if not cpe_title:
            cpe_title = self._get_cpe_infos(cpe.get("cpeName", ""))["name"]
        return cpe_title

    def _cpe_to_stix(self, record: CPERecord) -> Any:
        """
        Convert a CPERecord into a custom STIX object of type 'x-cpe-record'.
        The object includes the raw CPE data in the 'x_raw_data' field and is wrapped with
        STIXWrapper to ensure attribute access and a serialize() method.

        Parameters
        ----------
        record : CPERecord
            Instance containing the CPE data.

        Returns
        -------
        Any
            A custom STIX object representing the CPE record.
        """
        data = {
            "type": "x-cpe-record",
            "id": f"x-cpe-record--{uuid4()}",
            "spec_version": "2.1",
            "x_cpe": record.cpe,
            "x_vendor": record.vendor,
            "x_name": record.name,
            "x_version": record.version,
            "x_language": record.language,
            "x_created": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "x_raw_data": record.raw_data,
        }
        stix_dict = stix2.parse(json.dumps(data), allow_custom=True)
        stix_obj = STIXWrapper(stix_dict) if isinstance(stix_dict, dict) else stix_dict
        return stix_obj

    def _import_page(self, page_index: int, results_per_page: int) -> int:
        """
        Process a single page of API results:
            1. Build the URL for the page based on the index.
            2. Retrieve the list of CPEs and convert the JSON into CPERecord instances.
            3. Persist the raw records in the database.
            4. Convert the records into STIX objects and add them via Stix2Services.

        Parameters
        ----------
        page_index : int
            The index of the page to process.
        results_per_page : int
            Number of results per page as returned by the API.

        Returns
        -------
        int
            The number of STIX objects imported from this page.
        """
        start_index: int = page_index * results_per_page
        page_url: str = self._get_api_url(start_index, None, None)
        self.logger.debug(f"Starting import for page {page_index + 1} with URL: {page_url}")
        json_objects: dict[str, Any] = self._get_cpe_list(page_url)
        raw_records: list[CPERecord] = self._json_to_cpe_records(json_objects)
        imported: int = 0

        if raw_records:
            # Persist raw CPERecord objects in the database.
            session_factory = sessionmaker(bind=self.db_manager.get_engine())
            session = session_factory()
            try:
                for record in raw_records:
                    session.add(record)
                session.commit()
                self.logger.info(f"Saved {len(raw_records)} raw CPE records in the database.")
                # Prepare data for STIX conversion.
                records_data = [
                    {
                        "id": record.id,
                        "cpe": record.cpe,
                        "vendor": record.vendor,
                        "name": record.name,
                        "version": record.version,
                        "language": record.language,
                        "raw_data": record.raw_data,
                    }
                    for record in raw_records
                ]
            except Exception as e:
                session.rollback()
                self.logger.error(f"Error saving raw CPERecords on page {page_index + 1}: {e}")
                records_data = []
            finally:
                session.close()

            # Convert each record to a STIX object.
            stix_objects = []
            for rec in records_data:
                dummy_record = type("DummyCPERecord", (object,), rec)
                stix_obj = self._cpe_to_stix(dummy_record)
                stix_objects.append(stix_obj)
            for obj in stix_objects:
                self.stix2_services.add_object(obj)
            self.stix2_services.save_persistence_db()
            imported = len(stix_objects)
            self.logger.info(f"{imported} STIX objects imported on page {page_index + 1}.")
        else:
            self.logger.info(f"No records found on page {page_index + 1}.")

        return imported

    def _import_all(self) -> None:
        """
        Import all available CPEs from the NIST API sequentially:
            1. Retrieve initial parameters (totalResults, resultsPerPage) from the API.
            2. Calculate the total number of pages.
            3. Process each page, waiting 6 seconds between requests to avoid overload.
            4. Accumulate and log the total number of records imported.
        """
        self.logger.info("Starting bulk import of all CPEs sequentially...")
        api_url: str = self._get_api_url(0, None, None)
        parameters: dict[str, Any] = self._get_request_params(api_url)
        total_results: int = parameters.get("totalResults", 0)
        if total_results == 0:
            self.logger.info("No CPEs to import!")
            return
        results_per_page: int = parameters.get("resultsPerPage", 1)
        total_pages: int = math.ceil(total_results / results_per_page)
        self.logger.info(f"Total pages to import: {total_pages}")

        total_imported: int = 0
        for page_index in range(total_pages):
            imported = self._import_page(page_index, results_per_page)
            total_imported += imported
            self.logger.info(
                f"Page {page_index + 1} processed. Total imported so far: {total_imported}"
            )
            # Wait 6 seconds between requests.
            time.sleep(6)

        self.logger.info(f"Import completed. Total records imported: {total_imported}")

    def run(self) -> None:
        """
        Execute the complete import process:
            1. Start the sequential import of all CPEs.
            2. Log the beginning and end of the process.

        Returns
        -------
        None
        """
        self.logger.info("Executing CPEConnectorModule...")
        self._import_all()
        self.logger.info("CPEConnectorModule execution finished.")
