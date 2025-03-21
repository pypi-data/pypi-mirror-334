import csv
import json
import logging
import sys
import tempfile
import types
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import stix2
from sqlalchemy.exc import SQLAlchemyError

from threatxmanager.base_module.strix_serveses import Stix2Services
from threatxmanager.config.manager_config import Config

# --- Dummies for DBManager and LogManager ---


class DummyDBManagerSuccess:
    def __init__(self):
        self.init_db_called = False

    def init_db(self, base):  # Changed from Base to base
        self.init_db_called = True

    def get_session(self):
        dummy_session = MagicMock()
        dummy_session.get.return_value = None
        dummy_session.query.return_value.all.return_value = []
        dummy_session.commit.return_value = None
        dummy_session.close.return_value = None
        return dummy_session


class DummyDBManagerFailure:
    def init_db(self, base):  # Changed from Base to base
        raise Exception("init_db error")

    def get_session(self):
        dummy_session = MagicMock()
        dummy_session.get.return_value = None
        dummy_session.add.return_value = None
        dummy_session.commit.side_effect = SQLAlchemyError("commit error")
        dummy_session.rollback.return_value = None
        dummy_session.close.return_value = None
        return dummy_session


class DummyDBManagerQueryFailure:
    def get_session(self):
        dummy_session = MagicMock()
        dummy_session.query.side_effect = SQLAlchemyError("query error")
        dummy_session.close.return_value = None
        return dummy_session


class DummyLogManager:
    def __init__(self):
        self.logger = logging.getLogger("dummy")
        self.stream = StringIO()
        handler = logging.StreamHandler(self.stream)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def get_logger(self):
        return self.logger


# --- Enhanced Tests for Stix2Services ---


class TestStix2ServicesExtra(unittest.TestCase):
    def setUp(self) -> None:
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            self.temp_file_name = tf.name
        self.config = Config()
        self.service = Stix2Services(persist_file=self.temp_file_name, config=self.config)

    def tearDown(self) -> None:
        temp_path = Path(self.temp_file_name)
        if temp_path.exists():
            temp_path.unlink()

    def test_init_with_log_manager(self):
        """Checks if __init__ uses the provided log_manager."""
        dummy_log_manager = DummyLogManager()
        service = Stix2Services(persist_file=self.temp_file_name, log_manager=dummy_log_manager)
        assert service.logger.name == "dummy"

    def test_ensure_db_table_success(self):
        """Checks if _ensure_db_table runs successfully with a valid DBManager."""
        dummy_module = types.ModuleType("threatxmanager.models.base_model")
        dummy_module.Base = object
        sys.modules["threatxmanager.models.base_model"] = dummy_module

        dummy_db = DummyDBManagerSuccess()
        Stix2Services(db_manager=dummy_db, persist_file=None)  # Removed unused variable
        assert dummy_db.init_db_called

    def test_ensure_db_table_failure(self):
        """Checks exception handling in _ensure_db_table when init_db fails."""
        dummy_db = DummyDBManagerFailure()
        dummy_log_manager = DummyLogManager()
        service = Stix2Services(
            db_manager=dummy_db, persist_file=None, log_manager=dummy_log_manager
        )
        with self.assertLogs(dummy_log_manager.logger, level="ERROR") as cm:
            service._ensure_db_table()

        assert any("Error creating/verifying 'stix_objects'" in msg for msg in cm.output)

    def test_init_load_persistence_with_invalid_file(self):
        """Forces failure in load_persistence with a non-existent file."""
        dummy_log_manager = DummyLogManager()
        service = Stix2Services(
            persist_file="non_existent_file.json", log_manager=dummy_log_manager
        )
        with self.assertLogs(dummy_log_manager.logger, level="ERROR") as cm:
            service.load_persistence("non_existent_file.json")
        assert any("Error loading persistence" in msg for msg in cm.output)

    def test_register_callback_valid(self):
        """Tests callback registration for a valid event."""

        def callback(obj):  # Replaced lambda with def
            pass

        self.service.register_callback("add", callback)
        assert callback in self.service.callbacks["add"]

    def test_register_callback_invalid(self):
        """Tests callback registration for an invalid event, expecting a warning."""
        dummy_log_manager = DummyLogManager()
        service = Stix2Services(persist_file=self.temp_file_name, log_manager=dummy_log_manager)
        with self.assertLogs(dummy_log_manager.logger, level="WARNING") as cm:
            service.register_callback("invalid_event", lambda obj: None)
        assert any(
            "Event 'invalid_event' is not supported for callbacks" in msg for msg in cm.output
        )

    def test_trigger_event_with_exception(self):
        """Tests _trigger_event when a callback raises an exception."""
        dummy_log_manager = DummyLogManager()
        service = Stix2Services(persist_file=self.temp_file_name, log_manager=dummy_log_manager)

        def faulty_callback(obj):
            raise ValueError("Callback error")

        service.register_callback("add", faulty_callback)
        with self.assertLogs(dummy_log_manager.logger, level="ERROR") as cm:
            service._trigger_event("add", {"id": "dummy"})
        assert any("Error in callback for event" in msg for msg in cm.output)

    def test_update_object_description(self):
        """Tests update_object updating the description field."""
        indicator = self.service.create_indicator(
            name="Indicator to update",
            pattern="[ipv4-addr:value = '1.2.3.4']",
            pattern_type="stix",
            valid_from="2023-01-01T00:00:00Z",
            description="Old description",
        )
        updated = self.service.update_object(indicator.id, description="New description")
        assert json.loads(updated.serialize()).get("description") == "New description"

    def test_update_object_not_found(self):
        """Tests that update_object raises ValueError for a non-existent object."""
        with pytest.raises(ValueError):
            self.service.update_object("non-existent-id", description="Does not matter")

    def test_update_objects_batch_all_success(self):
        """Tests update_objects_batch updating all objects successfully."""
        ind1 = self.service.create_indicator(
            name="Batch 1",
            pattern="[ipv4-addr:value = '1.1.1.1']",
            pattern_type="stix",
            valid_from="2023-01-01T00:00:00Z",
            description="Desc1",
        )
        ind2 = self.service.create_indicator(
            name="Batch 2",
            pattern="[ipv4-addr:value = '2.2.2.2']",
            pattern_type="stix",
            valid_from="2023-01-01T00:00:00Z",
            description="Desc2",
        )
        updated_list = self.service.update_objects_batch(
            [ind1.id, ind2.id], description="Batch update"
        )
        assert len(updated_list) == 2
        for obj in updated_list:
            assert json.loads(obj.serialize()).get("description") == "Batch update"

    def test_update_objects_batch_with_invalid(self):
        """Tests update_objects_batch with an invalid ID."""
        ind = self.service.create_indicator(
            name="Batch Valid",
            pattern="[ipv4-addr:value = '10.0.0.1']",
            pattern_type="stix",
            valid_from="2023-01-01T00:00:00Z",
        )
        updated = self.service.update_objects_batch(
            [ind.id, "invalid-id"], description="batch update"
        )
        assert len(updated) == 1
        updated_obj = updated[0]
        assert json.loads(updated_obj.serialize()).get("description") == "batch update"

    def test_remove_object(self):
        """Tests removal of an existing object."""
        indicator = self.service.create_indicator(
            name="To Be Removed",
            pattern="[ipv4-addr:value = '1.1.1.1']",
            pattern_type="stix",
            valid_from="2023-01-01T00:00:00Z",
        )
        self.service.remove_object(indicator.id)
        assert self.service.get_object_by_id(indicator.id) is None

    def test_remove_object_not_found(self):
        """Tests that remove_object raises ValueError for a non-existent object."""
        with pytest.raises(ValueError):
            self.service.remove_object("non-existent-id")

    def test_remove_objects_batch_success(self):
        """Tests remove_objects_batch removing existing objects."""
        ind1 = self.service.create_indicator(
            name="Remove 1",
            pattern="[ipv4-addr:value = '3.3.3.3']",
            pattern_type="stix",
            valid_from="2023-01-01T00:00:00Z",
        )
        ind2 = self.service.create_indicator(
            name="Remove 2",
            pattern="[ipv4-addr:value = '4.4.4.4']",
            pattern_type="stix",
            valid_from="2023-01-01T00:00:00Z",
        )
        self.service.remove_objects_batch([ind1.id, ind2.id])
        assert self.service.get_object_by_id(ind1.id) is None
        assert self.service.get_object_by_id(ind2.id) is None

    def test_filter_objects(self):
        """Tests filter_objects applying a filter on the confidence field."""
        self.service.create_indicator(
            name="Filter Low",
            pattern="[ipv4-addr:value = '1.1.1.1']",
            pattern_type="stix",
            valid_from="2023-01-01T00:00:00Z",
            confidence=30,
        )
        high = self.service.create_indicator(
            name="Filter High",
            pattern="[ipv4-addr:value = '2.2.2.2']",
            pattern_type="stix",
            valid_from="2023-01-01T00:00:00Z",
            confidence=80,
        )
        filtered = self.service.filter_objects(
            [lambda o: hasattr(o, "confidence") and o.confidence >= 50]
        )
        assert any(o.id == high.id for o in filtered)
        for o in filtered:
            assert not (hasattr(o, "confidence") and o.confidence < 50)

    def test_advanced_search_no_results(self):
        """Tests advanced_search returning zero results for unmet criteria."""
        self.service.create_indicator(
            name="Low Confidence",
            pattern="[ipv4-addr:value = '3.3.3.3']",
            pattern_type="stix",
            valid_from="2023-01-01T00:00:00Z",
            confidence=20,
        )
        results = self.service.advanced_search({"confidence": lambda c: c and c > 50})
        assert len(results) == 0

    def test_get_objects_by_type_and_advanced_search(self):
        """Tests get_objects_by_type and advanced_search with combined criteria."""
        ind = self.service.create_indicator(
            name="Search Test",
            pattern="[ipv4-addr:value = '5.5.5.5']",
            pattern_type="stix",
            valid_from="2023-01-01T00:00:00Z",
            confidence=80,
        )
        objs = self.service.get_objects_by_type("indicator")
        assert any(o.id == ind.id for o in objs)
        results = self.service.advanced_search(
            {"confidence": lambda c: c > 50, "type": "indicator"}
        )
        assert any(o.id == ind.id for o in results)

    def test_get_relationships_for_object_case(self):
        """Tests get_relationships_for_object returning associated relationships."""
        ind = self.service.create_indicator(
            name="Rel Indicator",
            pattern="[ipv4-addr:value = '6.6.6.6']",
            pattern_type="stix",
            valid_from="2023-01-01T00:00:00Z",
        )
        mal = stix2.Malware(name="Rel Malware", is_family=False, description="Malware")
        self.service.add_object(mal)
        rel = self.service.create_relationship(
            source_ref=ind.id,
            target_ref=mal.id,
            relationship_type="indicates",
            description="Indicator indicates malware",
        )
        rels = self.service.get_relationships_for_object(ind.id)
        assert any(r.id == rel.id for r in rels)

    def test_load_bundle_multiple(self):
        """Tests load_bundle with a bundle containing multiple objects."""
        indicator = stix2.Indicator(
            name="Bundle Indicator",
            pattern="[ipv4-addr:value = '7.7.7.7']",
            pattern_type="stix",
            valid_from="2023-01-01T00:00:00Z",
        )
        malware = stix2.Malware(name="Bundle Malware", is_family=False, description="Malware")
        bundle = stix2.Bundle(objects=[indicator, malware])
        bundle_json = bundle.serialize()
        self.service.objects.clear()
        self.service.load_bundle(bundle_json)
        assert indicator.id in self.service.objects
        assert malware.id in self.service.objects

    def test_serialize_objects_valid(self):
        """Tests serialize_objects returning a valid JSON from a STIX Bundle."""
        ind = self.service.create_indicator(
            name="Serialize Indicator",
            pattern="[ipv4-addr:value = '8.8.8.8']",
            pattern_type="stix",
            valid_from="2023-01-01T00:00:00Z",
        )
        bundle_json = self.service.serialize_objects()
        parsed = stix2.parse(bundle_json, allow_custom=True)
        assert parsed.type == "bundle"
        assert any(obj.id == ind.id for obj in parsed.objects)

    def test_serialize_objects_empty(self):
        """Tests serialize_objects when there are no stored objects."""
        self.service.objects.clear()
        bundle_json = self.service.serialize_objects()
        raw_bundle = json.loads(bundle_json)
        # Checks that the "objects" key returns an empty list (or is absent).
        assert raw_bundle.get("objects", []) == []

    def test_export_to_dict_valid(self):
        """Tests export_to_dict returning the correct mapping of objects."""
        ind = self.service.create_indicator(
            name="Dict Indicator",
            pattern="[ipv4-addr:value = '9.9.9.9']",
            pattern_type="stix",
            valid_from="2023-01-01T00:00:00Z",
            description="Test",
        )
        export_dict = self.service.export_to_dict()
        assert ind.id in export_dict
        assert export_dict[ind.id]["name"] == "Dict Indicator"

    def test_export_to_dict_empty(self):
        """Tests export_to_dict when there are no objects, returning an empty dictionary."""
        self.service.objects.clear()
        export_dict = self.service.export_to_dict()
        assert export_dict == {}

    def test_save_persistence_no_file(self):
        """Tests save_persistence when no file is defined, logging a warning."""
        dummy_log_manager = DummyLogManager()
        service = Stix2Services(persist_file=None, log_manager=dummy_log_manager)
        with self.assertLogs(dummy_log_manager.logger, level="WARNING") as cm:
            service.save_persistence()
        assert any("No persistence file defined" in msg for msg in cm.output)

    def test_save_persistence_exception(self):
        """Tests save_persistence handling an exception during file write."""
        dummy_log_manager = DummyLogManager()
        service = Stix2Services(persist_file=self.temp_file_name, log_manager=dummy_log_manager)
        with (
            pytest.raises(Exception, match="write error"),
            patch("pathlib.Path.open", side_effect=Exception("write error")),
        ):
            service.save_persistence()

    def test_save_persistence_file(self):
        """Tests save_persistence writing data to a file."""
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            file_path = tf.name
        try:
            service = Stix2Services(persist_file=file_path)
            ind = service.create_indicator(
                name="Persist Indicator",
                pattern="[ipv4-addr:value = '10.10.10.10']",
                pattern_type="stix",
                valid_from="2023-01-01T00:00:00Z",
            )
            service.save_persistence()
            with Path(file_path).open(encoding="utf-8") as f:
                content = f.read()
            bundle = stix2.parse(content, allow_custom=True)
            assert any(obj.id == ind.id for obj in bundle.objects)
        finally:
            Path(file_path).unlink()

    def test_load_persistence_success(self):
        """Tests load_persistence loading objects from a JSON Bundle file."""
        with tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8") as tf:
            file_path = tf.name
            ind = stix2.Indicator(
                name="Load Indicator",
                pattern="[ipv4-addr:value = '11.11.11.11']",
                pattern_type="stix",
                valid_from="2023-01-01T00:00:00Z",
            )
            bundle = stix2.Bundle(objects=[ind])
            tf.write(bundle.serialize())
        try:
            service = Stix2Services(persist_file=file_path)
            assert ind.id in service.objects
        finally:
            Path(file_path).unlink()

    def test_load_persistence_db_no_db_manager(self):
        """Tests load_persistence_db logging a warning when DBManager is not provided."""
        dummy_log_manager = DummyLogManager()
        service = Stix2Services(persist_file=None, log_manager=dummy_log_manager)
        with self.assertLogs(dummy_log_manager.logger, level="WARNING") as cm:
            service.load_persistence_db()
        assert any("DBManager not provided" in msg for msg in cm.output)

    def test_load_persistence_db_empty(self):
        """Tests load_persistence_db when the query returns an empty list."""

        class DummyDBManagerEmpty:
            def init_db(self, base):  # base in lowercase
                pass

            def get_session(self):
                dummy_session = MagicMock()
                dummy_session.query.return_value.all.return_value = []
                dummy_session.close.return_value = None
                return dummy_session

        dummy_db = DummyDBManagerEmpty()
        service = Stix2Services(db_manager=dummy_db, persist_file=None)
        service.objects.clear()
        service.load_persistence_db()
        assert service.objects == {}

    def test_load_persistence_db_success(self):
        """Tests load_persistence_db loading objects from the database."""

        class DummyStixObject:
            def __init__(self, stix_id, data):
                self.stix_id = stix_id
                self.data = data

        class DummyDBManagerLoad:
            def init_db(self, base):  # base in lowercase
                pass

            def get_session(self):
                class DummyQuery:
                    def __init__(self, record):
                        self.record = record

                    def all(self):
                        return [self.record]

                class DummySession:
                    def query(self, model):
                        ind = stix2.Indicator(
                            name="DB Load",
                            pattern="[ipv4-addr:value = '4.4.4.4']",
                            pattern_type="stix",
                            valid_from="2023-01-01T00:00:00Z",
                        )
                        return DummyQuery(DummyStixObject(ind.id, ind.serialize()))

                    def close(self):
                        pass

                return DummySession()

        dummy_db = DummyDBManagerLoad()
        service = Stix2Services(db_manager=dummy_db, persist_file=None)
        service.objects.clear()
        service.load_persistence_db()
        keys = list(service.objects.keys())
        assert len(keys) == 1
        loaded_obj = service.objects[keys[0]]
        assert json.loads(loaded_obj.serialize()).get("name") == "DB Load"

    def test_save_persistence_db_update_and_insert(self):
        """Tests save_persistence_db updating existing records and inserting new ones."""
        ind1 = self.service.create_indicator(
            name="DB Update",
            pattern="[ipv4-addr:value = '7.7.7.7']",
            pattern_type="stix",
            valid_from="2023-01-01T00:00:00Z",
        )
        ind2 = self.service.create_indicator(
            name="DB Insert",
            pattern="[ipv4-addr:value = '8.8.8.8']",
            pattern_type="stix",
            valid_from="2023-01-01T00:00:00Z",
        )

        class DummyStixObject:
            def __init__(self, stix_id, data):
                self.stix_id = stix_id
                self.data = data

        class DummySession:
            def __init__(self):
                self.add_calls = 0

            class DummyQuery:
                def __init__(self, record):
                    self.record = record

                def filter_by(self, **kwargs):
                    # Simulate filtering by comparing the stix_id.
                    if kwargs.get("stix_id") == self.record.stix_id:
                        return self
                    # If not matching, simulate no results.
                    self.record = None
                    return self

                def first(self):
                    return self.record

                def all(self):
                    return [self.record] if self.record is not None else []

            def query(self, model):
                # Return a DummyQuery with a record for ind1.
                return DummySession.DummyQuery(DummyStixObject(ind1.id, ind1.serialize()))

            def get(self, model, obj_id):  # Renamed parameter to obj_id
                if obj_id == ind1.id:
                    return DummyStixObject(ind1.id, ind1.serialize())
                return None

            def add(self, record):
                self.add_calls += 1

            def commit(self):
                pass

            def rollback(self):
                pass

            def close(self):
                pass

        dummy_session = DummySession()
        dummy_db = MagicMock()
        dummy_db.get_session.return_value = dummy_session
        service = Stix2Services(db_manager=dummy_db, persist_file="")
        service.load_persistence_db = lambda: None
        service.add_object(ind1)
        service.add_object(ind2)
        service.save_persistence_db()
        # Expect one call to add() for the new object (ind2) since ind1 is updated.
        assert dummy_session.add_calls == 1

    def test_generate_report(self):
        """Tests generate_report returning statistics of the stored objects."""
        _ = self.service.create_indicator(  # Using _ to avoid warning
            name="Report Indicator",
            pattern="[ipv4-addr:value = '12.12.12.12']",
            pattern_type="stix",
            valid_from="2023-01-01T00:00:00Z",
        )
        report = self.service.generate_report()
        assert report["total_objects"] >= 1
        assert "indicator" in report["count_by_type"]

    def test_export_to_csv_missing_fields(self):
        """Tests export_to_csv gracefully handling missing fields (name and description)."""
        dummy_obj = stix2.Indicator(
            pattern="[ipv4-addr:value = '13.13.13.13']",
            pattern_type="stix",
            valid_from="2023-01-01T00:00:00Z",
        )
        self.service.add_object(dummy_obj)
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            csv_file = tf.name
        try:
            self.service.export_to_csv(csv_file)
            with Path(csv_file).open(encoding="utf-8") as f:
                content = f.read()
            assert dummy_obj.id in content
            reader = csv.DictReader(content.splitlines())
            row = next(reader)
            assert row["name"] == ""
            assert row["description"] == ""
        finally:
            Path(csv_file).unlink()

    def test_init_prefers_file_over_db(self):
        """Tests that if both persist_file and db_manager are provided, load_persistence is called and not load_persistence_db."""
        dummy_log_manager = DummyLogManager()
        with tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8") as tf:
            file_path = tf.name
            ind = stix2.Indicator(
                name="File Load",
                pattern="[ipv4-addr:value = '14.14.14.14']",
                pattern_type="stix",
                valid_from="2023-01-01T00:00:00Z",
            )
            bundle = stix2.Bundle(objects=[ind])
            tf.write(bundle.serialize())
        dummy_db = DummyDBManagerSuccess()
        service = Stix2Services(
            persist_file=file_path, db_manager=dummy_db, log_manager=dummy_log_manager
        )
        assert ind.id in service.objects
        Path(file_path).unlink()

    def test_update_object_no_changes(self):
        """Tests update_object when no field is modified."""
        indicator = self.service.create_indicator(
            name="No Change",
            pattern="[ipv4-addr:value = '15.15.15.15']",
            pattern_type="stix",
            valid_from="2023-01-01T00:00:00Z",
            description="Initial",
        )
        updated = self.service.update_object(indicator.id)
        assert updated.id.startswith("indicator--")
        assert json.loads(updated.serialize()).get("description") == "Initial"


if __name__ == "__main__":
    unittest.main(verbosity=2)
