import re
import uuid
from datetime import datetime
from typing import Any, ClassVar

import httpx  # We use httpx instead of requests
import stix2
from dateutil.parser import parse
from stix2 import (
    DomainName,
    EmailAddress,
    Identity,
    Relationship,
    X509Certificate,
    X509V3ExtensionsType,
)
from stix2.exceptions import AtLeastOnePropertyError

from threatxmanager.base_module.base_module import BaseModule
from threatxmanager.base_module.strix_serveses import Stix2Services
from threatxmanager.config.manager_config import Config
from threatxmanager.dbmanager.modules_models.certificate_model import Certificate

APP_VERSION: str = "1.0.0"


def generate_id(object_type: str, *args) -> str:
    """
    Generate a STIX identifier in the format 'object_type--<uuid>'.

    The UUID is generated using uuid5 with a seed composed of the provided arguments.

    Parameters
    ----------
    object_type : str
        The STIX object type.
    *args
        Additional values used to generate the seed.

    Returns
    -------
    str
        A string representing the STIX ID.
    """
    seed = "".join(str(arg) for arg in args)
    uid = uuid.uuid5(uuid.NAMESPACE_DNS, seed)
    return f"{object_type}--{uid}"


class CrtSHClient(BaseModule):
    """
    Client module to retrieve certificate data from crt.sh and convert it to STIX objects

    The module performs the following steps:
        1. Domain Transformation: Validates and (optionally) wildcards the domain.
        2. Data Request: Retrieves certificate data in JSON format using httpx.
        3. Data Conversion: Converts date strings, validates UUIDs, and processes certificate details.
        4. STIX Conversion: Creates STIX objects for certificates, domains, and email addresses.
        5. Relationship Creation: Establishes STIX relationships between certificate objects and their related domain/email objects.
        6. Persistence: Stores certificate data in the database and STIX objects via Stix2Services.
        7. Module Info: Updates module information.

    Attributes
    ----------
    TLP_MAP : ClassVar[dict[str, Any]]
        A mapping of TLP marking strings to STIX TLP constants.
    """

    TLP_MAP: ClassVar[dict[str, Any]] = {
        "TLP:WHITE": stix2.TLP_WHITE,
        "TLP:GREEN": stix2.TLP_GREEN,
        "TLP:AMBER": stix2.TLP_AMBER,
        "TLP:RED": stix2.TLP_RED,
    }

    def __init__(
        self,
        domain: str,
        labels: str = "crtsh",
        marking_refs: str = "TLP:WHITE",
        *,
        is_expired: bool = False,
        is_wildcard: bool = False,
        config_instance: Config | None = None,
        log_manager_instance: Any | None = None,
        db_instance: Any | None = None,
        env: str | None = None,
    ) -> None:
        """
        Initialize the CrtSHClient module with domain parameters and dependencies.

        Parameters
        ----------
        domain : str
            The domain to be processed.
        labels : str, optional
            A comma-separated list of labels to assign to the STIX objects, by default "crtsh".
        marking_refs : str, optional
            The TLP marking reference as a string, by default "TLP:WHITE".
        is_expired : bool, optional
            If True, includes expired certificates, by default False.
        is_wildcard : bool, optional
            If True, converts the domain into a wildcard domain (prepends "%."), by default False.
        config_instance : Config | None, optional
            Configuration instance, by default None.
        log_manager_instance : Any | None, optional
            Logging manager instance, by default None.
        db_instance : Any | None, optional
            Database manager instance, by default None.
        env : str | None, optional
            Execution environment, by default None.
        """
        super().__init__(config_instance, log_manager_instance, db_instance, env)
        self.logger.info("Initializing CRTSH client module.")

        self.marking_refs = self.TLP_MAP.get(marking_refs, stix2.TLP_WHITE)
        self.labels = [label.strip() for label in labels.split(",") if label.strip()]
        self.domain = self._transform_domain(domain, is_wildcard=is_wildcard)
        self.url = f"https://crt.sh/?q={self.domain}&output=json" + (
            "&exclude=expired" if is_expired else ""
        )
        self.author = self._create_author("crtsh")

        # Instantiate Stix2Services to manage STIX objects.
        self.stix2_services = Stix2Services(
            persist_file=None,
            db_manager=self.db_manager,
            log_manager=self.log_manager,
            config=self.config,
        )

    def _transform_domain(self, domain: str, *, is_wildcard: bool) -> str:
        """
        Validate and optionally transform the provided domain.

        If the domain is valid and is_wildcard is True, it prepends '%.' to enable wildcard matching.

        Parameters
        ----------
        domain : str
            The domain to validate.
        is_wildcard : bool, optional
            If True, returns the wildcard version of the domain.

        Returns
        -------
        str
            The validated (and possibly transformed) domain.

        Raises
        ------
        ValueError
            If the domain fails validation.
        """
        from validators import domain as domain_validator

        try:
            if domain_validator(domain):
                return f"%.{domain}" if is_wildcard else domain
            raise ValueError(f"Domain failed validation: {domain}")
        except Exception as e:
            self.logger.error(f"Domain validation error for '{domain}': {e}")
            raise ValueError(f"Invalid domain ({domain}): {e}")

    def _request_data(self) -> list[dict[str, Any]] | None:
        """
        Request certificate data from crt.sh.

        Uses httpx to make a GET request to the constructed URL with a 10-second timeout.

        Returns
        -------
        list[dict[str, Any]] | None
            A list of dictionaries containing certificate data if the request is successful;
            None otherwise.
        """
        try:
            self.logger.info(f"Requesting data from: {self.url}")
            response = httpx.get(self.url, timeout=10)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            self.logger.error(f"Error fetching data from {self.url}: {e}")
            return None

    def convert_to_datetime(self, date_str: str) -> datetime | None:
        """
        Convert a date string into a datetime object.

        Attempts to parse the string using dateutil.parser. If the initial parsing fails,
        a regex pattern is used to adjust the format and parse again.

        Parameters
        ----------
        date_str : str
            The date string to convert.

        Returns
        -------
        datetime | None
            The parsed datetime object or None if conversion fails.
        """
        if not date_str:
            return None
        try:
            return parse(date_str)
        except Exception as e:
            pattern = r"^(?P<base>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})(?:\.(?P<fraction>\d+))?(?P<tz>Z|[+-]\d{2}:\d{2})?$"
            match = re.match(pattern, date_str)
            if match:
                base = match.group("base")
                fraction = (match.group("fraction") or "").ljust(6, "0")
                tz = match.group("tz") or ""
                new_date_str = f"{base}.{fraction}{tz}"
                try:
                    return parse(new_date_str)
                except Exception as ex:
                    self.logger.error(f"Error parsing adjusted date '{new_date_str}': {ex}")
                    return None
            self.logger.error(f"Error parsing date '{date_str}': {e}")
            return None

    def is_valid_uuid(self, uuid_to_test: str) -> bool:
        """
        Validate whether a string is a valid UUID of versions 1, 3, 4, or 5.

        Parameters
        ----------
        uuid_to_test : str
            The UUID string to validate.

        Returns
        -------
        bool
            True if valid, False otherwise.
        """
        try:
            val = uuid.UUID(uuid_to_test)
            return val.version in (1, 3, 4, 5)
        except Exception as e:
            self.logger.debug(f"UUID validation error for '{uuid_to_test}': {e}")
            return False

    def is_valid_stix_id(self, stix_id: str) -> bool:
        """
        Validate if the provided string is a valid STIX ID.

        A valid STIX ID must be a string containing '--' and the second part must be a valid UUID.

        Parameters
        ----------
        stix_id : str
            The STIX ID to validate.

        Returns
        -------
        bool
            True if valid, False otherwise.
        """
        if isinstance(stix_id, str) and "--" in stix_id:
            parts = stix_id.split("--")
            return len(parts) == 2 and self.is_valid_uuid(parts[1])
        return False

    def is_valid_entry_timestamp(
        self, entry_timestamp: str, min_datetime: datetime | None = None
    ) -> bool:
        """
        Validate that the entry timestamp is a valid datetime and optionally after a minimum datetime.

        Parameters
        ----------
        entry_timestamp : str
            The timestamp string to validate.
        min_datetime : datetime | None, optional
            A minimum datetime to compare against. If provided, the entry timestamp must be later.

        Returns
        -------
        bool
            True if valid (and later than min_datetime, if provided), False otherwise.
        """
        dt = self.convert_to_datetime(entry_timestamp)
        if dt is None:
            return False
        return dt > min_datetime if min_datetime else True

    @staticmethod
    def _create_author(name: str) -> Identity:
        """
        Create an Identity object to represent the author of the imported data.

        Parameters
        ----------
        name : str
            The name for the Identity.

        Returns
        -------
        Identity
            A STIX Identity object with the given name and a fixed description.
        """
        identity_class = "organization"
        return Identity(
            id=generate_id("identity", name, identity_class),
            name=name,
            description="CRTSH external import connector",
            identity_class=identity_class,
        )

    def process_certificate(self, item: dict[str, Any], stix_objects: list[Any]) -> str | None:
        """
        Process a certificate item from the JSON data into an X509Certificate STIX object.

        Extracts certificate properties, creates a STIX certificate object, and appends it to the provided list.
        In case of missing required properties or errors, logs the issue and returns None.

        Parameters
        ----------
        item : dict[str, Any]
            A dictionary containing certificate data.
        stix_objects : list[Any]
            A list to which the created STIX certificate object will be appended.

        Returns
        -------
        str | None
            The ID of the created certificate STIX object if successful, or None otherwise.
        """
        x509_extensions = None
        name_value = item.get("name_value")
        if name_value:
            x509_extensions = X509V3ExtensionsType(subject_alternative_name=name_value)
        try:
            cert = X509Certificate(
                type="x509-certificate",
                issuer=item.get("issuer_name"),
                validity_not_before=self.convert_to_datetime(item.get("not_before")),
                validity_not_after=self.convert_to_datetime(item.get("not_after")),
                subject=item.get("common_name"),
                serial_number=item.get("serial_number"),
                object_marking_refs=self.marking_refs,
                x509_v3_extensions=x509_extensions,
                custom_properties={
                    "labels": self.labels,
                    "x_opencti_created_by_ref": self.author.id,
                },
            )
            stix_objects.append(cert)
            return cert.id
        except AtLeastOnePropertyError as e:
            self.logger.error(f"Certificate processing error (missing property): {e}")
        except Exception as e:
            self.logger.error(f"Certificate processing error: {e}")
        return None

    def process_domain_name(self, domain: str) -> DomainName | None:
        """
        Process a domain string into a DomainName STIX object.

        Validates the domain using an external validator. If the domain is a wildcard
        (starts with "*."), it removes the wildcard and processes the domain.

        Parameters
        ----------
        domain : str
            The domain string to process.

        Returns
        -------
        DomainName | None
            A STIX DomainName object if the domain is valid; None otherwise.

        Raises
        ------
        ValueError
            If the domain is invalid.
        """
        from validators import domain as domain_validator

        domain = domain.lower().strip()
        try:
            if domain_validator(domain):
                return DomainName(
                    type="domain-name",
                    value=domain,
                    object_marking_refs=self.marking_refs,
                    custom_properties={
                        "labels": self.labels,
                        "x_opencti_created_by_ref": self.author.id,
                    },
                )
            if domain.startswith("*."):
                return self.process_domain_name(domain[2:])
        except Exception as e:
            self.logger.error(f"Error processing domain '{domain}': {e}")
            raise ValueError(f"Invalid domain ({domain}): {e}")
        return None

    def process_email_address(self, email: str) -> EmailAddress | None:
        """
        Process an email string into an EmailAddress STIX object.

        Validates the email using an external email validator.

        Parameters
        ----------
        email : str
            The email address to process.

        Returns
        -------
        EmailAddress | None
            A STIX EmailAddress object if valid; None otherwise.

        Raises
        ------
        ValueError
            If the email address is invalid.
        """
        from validators import email as email_validator

        email = email.lower().strip()
        try:
            if email_validator(email):
                return EmailAddress(
                    type="email-addr",
                    value=email,
                    object_marking_refs=self.marking_refs,
                    custom_properties={
                        "labels": self.labels,
                        "x_opencti_created_by_ref": self.author.id,
                    },
                )
        except Exception as e:
            self.logger.error(f"Error processing email '{email}': {e}")
            raise ValueError(f"Failed to process email address ({email}): {e}")
        return None

    def stix_relationship(self, source_ref: str, target_ref: str) -> Relationship | None:
        """
        Create a STIX Relationship object of type 'related-to' between two objects.

        Parameters
        ----------
        source_ref : str
            The STIX ID of the source object.
        target_ref : str
            The STIX ID of the target object.

        Returns
        -------
        Relationship | None
            A STIX Relationship object if both references are provided and distinct; None otherwise.
        """
        if not source_ref or not target_ref or source_ref == target_ref:
            return None
        return Relationship(
            id=generate_id("relationship", source_ref, target_ref, "related-to"),
            relationship_type="related-to",
            source_ref=source_ref,
            target_ref=target_ref,
            object_marking_refs=self.marking_refs,
            created_by_ref=self.author.id,
            custom_properties={"labels": self.labels},
        )

    def process_common_name(
        self, item: dict[str, Any], stix_objects: list[Any], certificate_id: str | None
    ) -> None:
        """
        Process the common name from the certificate data and create a DomainName STIX object.

        If a common name is found, a domain object is created and, if a certificate ID is provided,
        a relationship is also established between the certificate and the domain.

        Parameters
        ----------
        item : dict[str, Any]
            Certificate data dictionary.
        stix_objects : list[Any]
            List to which created STIX objects and relationships will be appended.
        certificate_id : str | None
            The STIX ID of the certificate to relate to the domain.
        """
        common_name = item.get("common_name")
        if common_name:
            domain_obj = self.process_domain_name(common_name)
            if domain_obj:
                if certificate_id:
                    rel = self.stix_relationship(certificate_id, domain_obj.id)
                    if rel:
                        stix_objects.append(rel)
                stix_objects.append(domain_obj)

    def process_name_value(
        self, item: dict[str, Any], stix_objects: list[Any], certificate_id: str | None
    ) -> None:
        """
        Process the name_value field from the certificate data.

        Splits the name_value by line, processes each entry as an email address if it contains '@'
        or as a domain otherwise, and creates corresponding STIX objects and relationships with the certificate.

        Parameters
        ----------
        item : dict[str, Any]
            Certificate data dictionary.
        stix_objects : list[Any]
            List to which created STIX objects and relationships will be appended.
        certificate_id : str | None
            The STIX ID of the certificate to relate to the processed entries.
        """
        if not certificate_id or not self.is_valid_stix_id(certificate_id):
            self.logger.error(f"Invalid or missing certificate STIX ID: {certificate_id}")
            return
        name_value = item.get("name_value")
        if name_value and isinstance(name_value, str):
            for name in [n.strip() for n in name_value.splitlines() if n.strip()]:
                if "@" in name:
                    stix_obj = None
                    try:
                        stix_obj = self.process_email_address(name)
                    except Exception as e:
                        self.logger.error(f"Error processing email address '{name}': {e}")
                    if stix_obj:
                        stix_objects.append(stix_obj)
                        rel = self.stix_relationship(certificate_id, stix_obj.id)
                        if rel:
                            stix_objects.append(rel)
                else:
                    stix_obj = None
                    try:
                        stix_obj = self.process_domain_name(name)
                    except Exception as e:
                        self.logger.error(f"Error processing domain '{name}': {e}")
                    if stix_obj:
                        stix_objects.append(stix_obj)
                        rel = self.stix_relationship(certificate_id, stix_obj.id)
                        if rel:
                            stix_objects.append(rel)

    def get_stix_objects(self, since: datetime | None = None) -> list[Any]:
        """
        Retrieve certificate data from crt.sh, process each item, and convert them into STIX objects.

        For each data item, validates the entry timestamp against an optional minimum datetime,
        processes the certificate into an X509Certificate object, and then processes common names
        and name_value entries into domain and email STIX objects with relationships.

        Parameters
        ----------
        since : datetime | None, optional
            A minimum datetime; only data with an entry_timestamp later than this will be processed,
            by default None.

        Returns
        -------
        list[Any]
            A deduplicated list of STIX objects created from the certificate data.
        """
        data = self._request_data()
        if not data:
            return []
        stix_objects: list[Any] = []
        for item in data:
            if self.is_valid_entry_timestamp(item.get("entry_timestamp", ""), since):
                self.logger.debug(f"Processing item: {item}")
                cert_id = self.process_certificate(item, stix_objects)
                if cert_id:
                    self.process_common_name(item, stix_objects, cert_id)
                    self.process_name_value(item, stix_objects, cert_id)
        # Deduplicate objects based on their 'id' attribute.
        unique_objects: dict[str, Any] = {
            getattr(obj, "id", None): obj for obj in stix_objects if getattr(obj, "id", None)
        }
        return list(unique_objects.values())

    def store_certificate_data(self) -> None:
        """
        Retrieve certificate data from crt.sh and store raw certificate records in the database.

        For each certificate data item, converts date fields and checks for the existence of the certificate
        in the database (by serial number and entry timestamp). If the certificate does not exist, it is inserted.
        """
        data = self._request_data()
        if not data:
            self.logger.info("No certificate raw data received.")
            return
        session = self.db_manager.get_session()
        for item in data:
            try:
                entry_timestamp = self.convert_to_datetime(item.get("entry_timestamp"))
                not_before = self.convert_to_datetime(item.get("not_before"))
                not_after = self.convert_to_datetime(item.get("not_after"))
                if not entry_timestamp:
                    raise ValueError("Invalid entry_timestamp")
            except Exception as e:
                self.logger.error(
                    f"Date conversion error for certificate {item.get('serial_number')}: {e}"
                )
                continue

            exists = (
                session.query(Certificate)
                .filter_by(
                    serial_number=item.get("serial_number"),
                    entry_timestamp=entry_timestamp,
                )
                .first()
            )
            if exists:
                self.logger.info(f"Certificate {item.get('serial_number')} already exists.")
                continue

            new_cert = Certificate(
                issuer_ca_id=item.get("issuer_ca_id"),
                issuer_name=item.get("issuer_name"),
                common_name=item.get("common_name"),
                name_value=item.get("name_value"),
                entry_timestamp=entry_timestamp,
                not_before=not_before,
                not_after=not_after,
                serial_number=item.get("serial_number"),
                result_count=item.get("result_count"),
            )
            session.add(new_cert)
            try:
                session.commit()
                self.logger.info(f"Inserted certificate {item.get('serial_number')} successfully.")
            except Exception as e:
                session.rollback()
                self.logger.error(f"Failed to insert certificate {item.get('serial_number')}: {e}")
        session.close()

    def update_info(self) -> dict[str, Any]:
        """
        Update and return the module's information dictionary.

        The information includes module name, configuration, labels, domain, URL, and author details.

        Returns
        -------
        dict[str, Any]
            The updated module information.
        """
        info = {
            "module": self.__class__.__name__,
            "configuration": self.module_config,
            "labels": self.labels,
            "domain": self.domain,
            "url": self.url,
            "author": self.author.to_dict()
            if hasattr(self.author, "to_dict")
            else str(self.author),
        }
        self.info.update(info)
        self.logger.debug(f"Updated module info: {self.info}")
        return self.info

    def run(self) -> None:
        """
        Execute the CrtSHClient module workflow

        The process includes:
            1. Updating the module info.
            2. Retrieving and processing certificate data to create STIX objects.
            3. Storing the STIX objects via Stix2Services.
            4. Persisting raw certificate data into the database.
        """
        self.logger.info("Running CrtSHClient module.")
        self.update_info()
        stix_objects = self.get_stix_objects()
        if stix_objects:
            # Instead of directly inserting via session, use Stix2Services.
            for obj in stix_objects:
                self.stix2_services.add_object(obj)
            # Save persistence in the database through the service.
            self.stix2_services.save_persistence_db()
            self.logger.info(
                f"Processed and stored {len(stix_objects)} STIX objects via Stix2Services."
            )
        else:
            self.logger.info("No STIX objects processed.")
        self.store_certificate_data()
