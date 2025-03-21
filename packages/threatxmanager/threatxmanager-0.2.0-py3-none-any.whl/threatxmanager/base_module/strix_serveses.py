import csv
import json
import logging
from collections.abc import Callable
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any

import stix2
from sqlalchemy.exc import SQLAlchemyError

from threatxmanager.config.manager_config import Config
from threatxmanager.dbmanager.connection import DBManager
from threatxmanager.dbmanager.models import Base
from threatxmanager.dbmanager.modules_models.stix_objects import StixObject
from threatxmanager.logmanager.logmanager import LogManager

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class STIXWrapper:
    """
    Wrapper for STIX objects providing attribute access and a serialize() method.
    """

    def __init__(self, data: dict):
        self._data = data
        for key, value in data.items():
            setattr(self, key, value)

    def serialize(self) -> str:
        return json.dumps(self._data)


class Stix2Services:
    def __init__(
        self,
        persist_file: str | None = None,
        db_manager: DBManager | None = None,
        log_manager: LogManager | None = None,
        config: Config | None = None,
    ) -> None:
        """
        Initialize STIX2 service with optional file or database persistence
        """
        self.objects: dict[str, Any] = {}
        self.persist_file = persist_file
        self.db_manager = db_manager
        self.config = config or Config()
        self.logger = log_manager.get_logger() if log_manager else logging.getLogger(__name__)
        self.callbacks: dict[str, list[Callable[[Any], None]]] = {
            "add": [],
            "update": [],
            "remove": [],
        }

        if self.db_manager:
            self._ensure_db_table()

        if self.persist_file:
            self.load_persistence(self.persist_file)
        elif self.db_manager and hasattr(self.db_manager, "get_session"):
            self.load_persistence_db()

    def _ensure_db_table(self) -> None:
        try:
            self.db_manager.init_db(Base)
            self.logger.info("Table 'stix_objects' verified/created successfully (via ORM).")
        except Exception as e:
            self.logger.error(f"Error creating/verifying 'stix_objects' table: {e}")

    def register_callback(self, event: str, callback: Callable[[Any], None]) -> None:
        if event in self.callbacks:
            self.callbacks[event].append(callback)
            self.logger.info(f"Callback registered for event '{event}'.")
        else:
            self.logger.warning(f"Event '{event}' is not supported for callbacks.")

    def _safe_invoke(self, event: str, callback: Callable[[Any], None], obj: Any) -> None:
        try:
            callback(obj)
        except Exception as e:
            self.logger.error(f"Error in callback for event '{event}': {e}")

    def _trigger_event(self, event: str, obj: Any) -> None:
        for cb in self.callbacks.get(event, []):
            self._safe_invoke(event, cb, obj)

    def add_object(self, obj: Any) -> None:
        self.objects[obj.id] = obj
        self.logger.info(f"Object {obj.type}--{obj.id} added/updated.")
        self._trigger_event("add", obj)

    def remove_object(self, object_id: str) -> None:
        if object_id in self.objects:
            removed = self.objects.pop(object_id)
            self.logger.info(f"Object {removed.type}--{object_id} removed.")
            self._trigger_event("remove", removed)
        else:
            raise ValueError(f"Object {object_id} not found.")

    def update_object(self, object_id: str, **kwargs: Any) -> Any:
        if object_id not in self.objects:
            raise ValueError(f"Object {object_id} not found.")
        old_obj = self.objects[object_id]
        data: dict[str, Any] = json.loads(old_obj.serialize())
        data.update(kwargs)
        new_obj = stix2.parse(data, allow_custom=True)
        self.add_object(new_obj)
        self.logger.info(
            f"Object {object_id} updated at {datetime.now(tz=timezone.utc).isoformat()}"
        )
        self._trigger_event("update", new_obj)
        return new_obj

    def update_objects_batch(self, object_ids: list[str], **kwargs: Any) -> list[Any]:
        updated = []
        for obj_id in object_ids:
            try:
                updated.append(self.update_object(obj_id, **kwargs))
            except Exception as e:
                self.logger.error(f"Error updating object {obj_id}: {e}")
        return updated

    def remove_objects_batch(self, object_ids: list[str]) -> None:
        for obj_id in object_ids:
            try:
                self.remove_object(obj_id)
            except Exception as e:
                self.logger.error(f"Error removing object {obj_id}: {e}")

    def get_object_by_id(self, object_id: str) -> Any:
        return self.objects.get(object_id)

    def get_objects_by_type(self, obj_type: str) -> list[Any]:
        return [obj for obj in self.objects.values() if obj.type == obj_type]

    def create_indicator(self, **kwargs: Any) -> Any:
        indicator = stix2.Indicator(**kwargs)
        self.add_object(indicator)
        return indicator

    def create_relationship(self, **kwargs: Any) -> Any:
        relationship = stix2.Relationship(**kwargs)
        self.add_object(relationship)
        return relationship

    def filter_objects(self, filters: list[Callable[[Any], bool]]) -> list[Any]:
        results = list(self.objects.values())
        for f in filters:
            results = list(filter(f, results))
        return results

    def advanced_search(self, criteria: dict[str, Any | Callable[[Any], bool]]) -> list[Any]:
        results = []
        for obj in self.objects.values():
            match = True
            obj_dict = json.loads(obj.serialize())
            for key, condition in criteria.items():
                value = obj_dict.get(key)
                if callable(condition):
                    if not condition(value):
                        match = False
                        break
                elif value != condition:
                    match = False
                    break
            if match:
                results.append(obj)
        return results

    def get_relationships_for_object(self, object_id: str) -> list[Any]:
        return [
            obj
            for obj in self.objects.values()
            if obj.type == "relationship" and object_id in {obj.source_ref, obj.target_ref}
        ]

    def load_bundle(self, bundle_json: str) -> None:
        bundle = stix2.parse(bundle_json, allow_custom=True)
        for obj in bundle.objects:
            self.add_object(obj)
        self.logger.info("Bundle loaded successfully.")

    def serialize_objects(self) -> str:
        return stix2.Bundle(objects=list(self.objects.values())).serialize()

    def export_to_dict(self) -> dict[str, Any]:
        return {obj_id: json.loads(obj.serialize()) for obj_id, obj in self.objects.items()}

    def save_persistence(self, filepath: str | None = None) -> None:
        target = filepath or self.persist_file
        if target:
            with Path(target).open("w", encoding="utf-8") as f:
                f.write(self.serialize_objects())
            self.logger.info(f"Data persisted to {target}.")
        else:
            self.logger.warning("No persistence file defined.")

    def load_persistence(self, filepath: str) -> None:
        try:
            with Path(filepath).open(encoding="utf-8") as f:
                bundle_json = f.read()
            self.load_bundle(bundle_json)
            self.logger.info(f"Persistence loaded from: {filepath}.")
        except Exception as e:
            self.logger.error(f"Error loading persistence: {e}")

    def save_persistence_db(self) -> None:
        if not self.db_manager:
            self.logger.warning("DBManager not provided; skipping DB persistence.")
            return

        session: Session = self.db_manager.get_session()
        try:
            for obj in self.objects.values():
                obj_data = json.loads(obj.serialize())
                stix_type = getattr(obj, "type", None)
                # Consulta usando stix_id, evitando o uso de session.get que exige todos os valores da chave composta.
                record = session.query(StixObject).filter_by(stix_id=obj.id).first()
                if record:
                    record.data = obj_data
                    record.stix_type = stix_type
                else:
                    session.add(StixObject(stix_id=obj.id, stix_type=stix_type, data=obj_data))
            session.commit()
            self.logger.info("Persistence saved to the database successfully.")
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Error saving persistence to the database: {e}")
        finally:
            session.close()

    def load_persistence_db(self) -> None:
        if not self.db_manager:
            self.logger.warning("DBManager not provided; skipping DB persistence load.")
            return

        session: Session = self.db_manager.get_session()
        try:
            records = session.query(StixObject).all()
            for record in records:
                obj_data = record.data if isinstance(record.data, dict) else json.loads(record.data)
                obj = stix2.parse(obj_data, allow_custom=True)
                if not hasattr(obj, "id"):
                    obj = STIXWrapper(obj)
                self.add_object(obj)
            self.logger.info("Persistence loaded from the database successfully.")
        except SQLAlchemyError as e:
            self.logger.error(f"Error loading persistence from the database: {e}")
        finally:
            session.close()

    def generate_report(self) -> dict[str, Any]:
        total = len(self.objects)
        by_type: dict[str, int] = {}
        for obj in self.objects.values():
            by_type[obj.type] = by_type.get(obj.type, 0) + 1
        report = {
            "total_objects": total,
            "count_by_type": by_type,
            "generation_date": datetime.now(tz=timezone.utc).isoformat(),
        }
        self.logger.info(f"Report generated: {report}")
        return report

    def export_to_csv(self, filepath: str) -> None:
        fieldnames = ["id", "type", "name", "description"]
        try:
            with Path(filepath).open("w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for obj in self.objects.values():
                    obj_dict = json.loads(obj.serialize())
                    writer.writerow(
                        {
                            "id": obj_dict.get("id"),
                            "type": obj_dict.get("type"),
                            "name": obj_dict.get("name", ""),
                            "description": obj_dict.get("description", ""),
                        }
                    )
            self.logger.info(f"Data exported to CSV at {filepath}.")
        except Exception as e:
            self.logger.error(f"Error exporting data to CSV: {e}")
