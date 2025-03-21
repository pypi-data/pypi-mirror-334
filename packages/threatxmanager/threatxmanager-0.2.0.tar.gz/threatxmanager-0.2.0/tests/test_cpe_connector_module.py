import unittest
import uuid
from unittest.mock import MagicMock, patch

import pytest

from threatxmanager.dbmanager.modules_models.cper_model import CPERecord
from threatxmanager.modules.external.cpe_connector_module import CPEConnectorModule


# Dummies para Config e DBManager.
class DummyConfig:
    def __init__(self, interval="1s"):
        self.config = {
            "default_env": "test",
            "modules": {
                "CPEConnectorModule": {
                    "base_url": "http://dummyapi",
                    "api_key": "dummy_api_key",
                    "interval": interval,
                }
            },
            "logs": {
                "test": {}  # Configuração mínima para o LogManager.
            },
        }

    def get(self, key, default=None):
        return self.config.get(key, default)

    def get_default_env(self):
        return self.config.get("default_env", "test")

    def get_section(self, section: str, environment: str | None = None) -> dict:
        sec = self.config.get(section, {})
        env = environment if environment else self.get_default_env()
        if isinstance(sec, dict):
            return sec.get(env, {})
        return {}

    def obfuscate_config(self, config):
        return config


class DummyDBManager:
    def __init__(self):
        self.engine = MagicMock()

    def get_engine(self):
        return self.engine

    def init_db(self, base):
        # Simula a inicialização sem nenhuma operação.
        pass

    def get_session(self):
        # Retorna uma sessão dummy para os testes.
        dummy_session = MagicMock()
        dummy_session.add = MagicMock()
        dummy_session.commit = MagicMock()
        dummy_session.rollback = MagicMock()
        dummy_session.close = MagicMock()
        return dummy_session


class TestCPEConnectorModuleFull(unittest.TestCase):
    def setUp(self):
        self.dummy_config = DummyConfig()
        self.dummy_db_manager = DummyDBManager()
        self.module = CPEConnectorModule(
            config_instance=self.dummy_config,
            db_instance=self.dummy_db_manager,
            log_manager_instance=None,
            env="test",
        )

    # Testa _get_interval
    def test_get_interval_hours(self):
        self.dummy_config.config["modules"]["CPEConnectorModule"]["interval"] = "1h"
        module = CPEConnectorModule(
            config_instance=self.dummy_config, db_instance=self.dummy_db_manager, env="test"
        )
        assert module._get_interval() == 3600

    def test_get_interval_seconds(self):
        self.dummy_config.config["modules"]["CPEConnectorModule"]["interval"] = "30s"
        module = CPEConnectorModule(
            config_instance=self.dummy_config, db_instance=self.dummy_db_manager, env="test"
        )
        assert module._get_interval() == 30

    def test_get_interval_invalid(self):
        self.dummy_config.config["modules"]["CPEConnectorModule"]["interval"] = "1x"
        module = CPEConnectorModule(
            config_instance=self.dummy_config, db_instance=self.dummy_db_manager, env="test"
        )
        with pytest.raises(ValueError):
            module._get_interval()

    # Testa _get_request_params
    @patch("requests.Session.get")
    def test_get_request_params_success(self, mock_get):
        dummy_response = MagicMock()
        dummy_response.status_code = 200
        dummy_response.json.return_value = {
            "resultsPerPage": 10,
            "startIndex": 0,
            "totalResults": 100,
        }
        mock_get.return_value = dummy_response
        params = self.module._get_request_params("http://dummyapi")
        assert params["resultsPerPage"] == 10
        assert params["startIndex"] == 0
        assert params["totalResults"] == 100

    @patch("requests.Session.get")
    def test_get_request_params_failure(self, mock_get):
        dummy_response = MagicMock()
        dummy_response.status_code = 500
        mock_get.return_value = dummy_response
        params = self.module._get_request_params("http://dummyapi")
        assert params == {}

    # Testa _get_cpe_list
    @patch("requests.Session.get")
    def test_get_cpe_list_success(self, mock_get):
        dummy_response = MagicMock()
        dummy_response.status_code = 200
        dummy_response.json.return_value = {"resultsPerPage": 10, "products": []}
        mock_get.return_value = dummy_response
        result = self.module._get_cpe_list("http://dummyapi")
        assert result["resultsPerPage"] == 10

    @patch("requests.Session.get")
    def test_get_cpe_list_failure(self, mock_get):
        dummy_response = MagicMock()
        dummy_response.status_code = 404
        mock_get.return_value = dummy_response
        result = self.module._get_cpe_list("http://dummyapi")
        assert result == {}

    # Testa _get_date_iso
    def test_get_date_iso(self):
        ts = 1609459200  # corresponde a 2021-01-01T00:00:00Z
        iso_str = self.module._get_date_iso(ts)
        assert iso_str == "2021-01-01T00:00:00+00:00"

    # Testa _get_id
    def test_get_id(self):
        obj_type = "test"
        id_str = self.module._get_id(obj_type)
        assert id_str.startswith("test--")
        uuid_part = id_str.split("--")[1]
        uuid_obj = uuid.UUID(uuid_part)
        assert isinstance(uuid_obj, uuid.UUID)

    # Testa _get_api_url
    def test_get_api_url_without_dates(self):
        url = self.module._get_api_url(0, None, None)
        assert url == "http://dummyapi?startIndex=0"

    def test_get_api_url_with_dates(self):
        url = self.module._get_api_url(10, "2021-01-01", "2021-01-31")
        assert (
            url
            == "http://dummyapi?startIndex=10&lastModStartDate=2021-01-01&lastModEndDate=2021-01-31"
        )

    # Testa _get_cpe_infos
    def test_get_cpe_infos_hardware(self):
        cpe_str = "cpe:2.3:h:vendor:product:version:*:*:*:*:*:*"
        infos = self.module._get_cpe_infos(cpe_str)
        assert infos["is_hardware"]
        assert infos["vendor"] == "vendor"
        assert infos["name"] == "product"
        assert infos["version"] == "version"

    def test_get_cpe_infos_software(self):
        cpe_str = "cpe:2.3:a:vendor:product:version:*:*:*:*:*:*"
        infos = self.module._get_cpe_infos(cpe_str)
        assert not infos["is_hardware"]
        assert infos["vendor"] == "vendor"
        assert infos["name"] == "product"
        assert infos["version"] == "version"

    def test_get_cpe_infos_language_invalid(self):
        # Caso em que a informação de idioma não é válida.
        cpe_str = "cpe:2.3:a:vendor:product:version:*:*:*:*:*:*"
        infos = self.module._get_cpe_infos(cpe_str)
        assert infos["language"] == ""

    # Testa _json_to_cpe_records
    def test_json_to_cpe_records(self):
        json_data = {
            "resultsPerPage": 1,
            "products": [
                {
                    "cpe": {
                        "cpeName": "cpe:2.3:a:vendor:product:1.0:*:*:*:*:*:*",
                        "deprecated": False,
                        "titles": [{"lang": "en", "title": "Product Title"}],
                    }
                }
            ],
        }
        records = self.module._json_to_cpe_records(json_data)
        assert len(records) == 1
        record = records[0]
        assert isinstance(record, CPERecord)
        assert record.cpe == "cpe:2.3:a:vendor:product:1.0:*:*:*:*:*:*"
        assert record.name == "Product Title"
        assert record.vendor == "vendor"
        assert record.version == "1.0"

    # Testa _get_cpe_title
    def test_get_cpe_title_with_en(self):
        cpe_dict = {
            "titles": [
                {"lang": "es", "title": "Título en Español"},
                {"lang": "en", "title": "English Title"},
            ],
            "cpeName": "cpe:2.3:a:vendor:product:1.0:*:*:*:*:*:*",
        }
        title = self.module._get_cpe_title(cpe_dict)
        assert title == "English Title"

    def test_get_cpe_title_without_en(self):
        cpe_dict = {
            "titles": [{"lang": "es", "title": "Título en Español"}],
            "cpeName": "cpe:2.3:a:vendor:product:1.0:*:*:*:*:*:*",
        }
        title = self.module._get_cpe_title(cpe_dict)
        # O fallback extrai o nome do CPE; espera-se "product"
        assert title == "product"

    # Testa _import_page
    @patch("time.sleep", return_value=None, autospec=True)
    @patch("threatxmanager.modules.external.cpe_connector_module.sessionmaker")
    @patch("requests.Session.get")
    def test_import_page_success(self, mock_get, mock_sessionmaker, mock_sleep):
        dummy_response = MagicMock()
        dummy_response.status_code = 200
        dummy_response.json.return_value = {
            "resultsPerPage": 1,
            "products": [
                {
                    "cpe": {
                        "cpeName": "cpe:2.3:a:vendor:product:1.0:*:*:*:*:*:*",
                        "deprecated": False,
                    },
                    "titles": [{"lang": "en", "title": "Product Title"}],
                }
            ],
        }
        mock_get.return_value = dummy_response

        dummy_session = MagicMock()
        dummy_session.__enter__.return_value = dummy_session
        dummy_session.add = MagicMock()
        dummy_session.commit = MagicMock()
        dummy_session.rollback = MagicMock()
        dummy_session.close = MagicMock()
        dummy_session_factory = MagicMock(return_value=dummy_session)
        mock_sessionmaker.return_value = dummy_session_factory

        imported = self.module._import_page(0, 1)
        assert imported == 1

    @patch("threatxmanager.modules.external.cpe_connector_module.CPEConnectorModule._import_all")
    def test_run(self, mock_import_all):
        self.module.run()
        mock_import_all.assert_called_once()


if __name__ == "__main__":
    unittest.main()
