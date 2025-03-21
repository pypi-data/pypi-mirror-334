import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy import Column, Integer, String, inspect
from sqlalchemy.orm import declarative_base

from threatxmanager.dbmanager.connection import DBManager

# Define a base and a dummy model for testing.
Base = declarative_base()


class DummyModel(Base):
    """
    Dummy model for testing purposes.

    Attributes
    ----------
    id : int
        Primary key of the dummy model.
    name : str
        Name field.
    """

    __tablename__ = "dummy_model"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)


class TestDBManager(unittest.TestCase):
    """
    Test suite for the DBManager class.

    This suite verifies:
        - Proper engine creation and session retrieval.
        - The creation of database tables.
        - CRUD operations (create, read, update, delete) functionality.
        - Exception handling in various methods.
        - Singleton and double initialization behavior.
    """

    def setUp(self):
        """
        Reset the singleton instance before each test and initialize a temporary SQLite database.

        It also creates a dummy config with the expected values for the 'database.bancode_dados' section.
        """
        DBManager._instance = None

        # Create a temporary file to be used as an SQLite database.
        fd, temp_path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        self.temp_db_file = temp_path
        self.database_url = "sqlite:///" + self.temp_db_file

        # Create a dummy config with the expected database settings.
        self.mock_config = MagicMock()
        self.mock_config.get_default_env.return_value = "test"

        def config_get(key, default=None):
            if key == "database":
                return {
                    "bancode_dados": {
                        "test": {
                            "DATABASE_URL": self.database_url,
                            "POOL_SIZE": 5,
                            "MAX_OVERFLOW": 10,
                            "POOL_TIMEOUT": 30,
                            "ECHO": False,
                        }
                    }
                }
            return default

        self.mock_config.get.side_effect = config_get

        # Instantiate DBManager with the dummy config.
        self.db_manager = DBManager(config_instance=self.mock_config, env="test")
        # Create tables in the database using the Base of the dummy models.
        self.db_manager.init_db(Base)

    def tearDown(self):
        """
        Dispose the engine connections and remove the temporary database file.
        """
        self.db_manager.get_engine().dispose()
        db_file = Path(self.temp_db_file)
        if db_file.exists():
            db_file.unlink()
        DBManager._instance = None

    def test_engine_creation(self):
        """
        Test that the engine is created correctly.

        Checks if the engine is not None and has the 'dialect' attribute.
        """
        engine = self.db_manager.get_engine()
        assert engine is not None
        assert hasattr(engine, "dialect")

    def test_get_session(self):
        """
        Test that get_session returns an instance of Session.

        Closes the session after verification.
        """
        session = self.db_manager.get_session()
        from sqlalchemy.orm import Session

        assert isinstance(session, Session)
        session.close()

    def test_init_db_creates_tables(self):
        """
        Test that init_db creates the tables defined in the Base.

        Uses SQLAlchemy inspector to verify that the 'dummy_model' table exists.
        """
        inspector = inspect(self.db_manager.get_engine())
        tables = inspector.get_table_names()
        assert "dummy_model" in tables

    def test_create_and_read(self):
        """
        Test the creation and reading of a record.

        Verifies that after creating a DummyModel instance, it can be read back correctly.
        """
        dummy = DummyModel(name="Test Name")
        created = self.db_manager.create(dummy)
        assert created.id is not None
        read_instance = self.db_manager.read(DummyModel, created.id)
        assert read_instance is not None
        assert read_instance.name == "Test Name"

    def test_update(self):
        """
        Test the update of a record.

        Verifies that updating a DummyModel instance correctly changes the 'name' field.
        """
        dummy = DummyModel(name="Old Name")
        created = self.db_manager.create(dummy)
        updated = self.db_manager.update(created, name="New Name")
        assert updated.name == "New Name"
        read_instance = self.db_manager.read(DummyModel, created.id)
        assert read_instance.name == "New Name"

    def test_delete(self):
        """
        Test the deletion of a record.

        Verifies that after deleting a DummyModel instance, it cannot be read back.
        """
        dummy = DummyModel(name="To be deleted")
        created = self.db_manager.create(dummy)
        record_id = created.id
        self.db_manager.delete(created)
        deleted_instance = self.db_manager.read(DummyModel, record_id)
        assert deleted_instance is None

    def test_missing_environment_configuration(self):
        """
        Test that an exception is raised when the environment is not found in the configuration.

        The dummy config is patched to simulate missing 'test' environment settings.
        """

        def config_get(key, default=None):
            if key == "database":
                return {"bancode_dados": {"other_env": {}}}
            return default

        self.mock_config.get.side_effect = config_get
        DBManager._instance = None
        with pytest.raises(Exception, match="Environment 'test' not found"):
            DBManager(config_instance=self.mock_config, env="test")

    def test_missing_database_url(self):
        """
        Test that an exception is raised when DATABASE_URL is missing.

        The dummy config is patched to simulate the absence of the DATABASE_URL key.
        """

        def config_get(key, default=None):
            if key == "database":
                return {
                    "bancode_dados": {
                        "test": {
                            # DATABASE_URL is missing
                            "POOL_SIZE": 5,
                            "MAX_OVERFLOW": 10,
                            "POOL_TIMEOUT": 30,
                            "ECHO": False,
                        }
                    }
                }
            return default

        self.mock_config.get.side_effect = config_get
        DBManager._instance = None
        with pytest.raises(Exception, match="DATABASE_URL is missing"):
            DBManager(config_instance=self.mock_config, env="test")

    def test_double_initialization(self):
        """
        Test that __init__ does not reconfigure if _initialized is already True.

        A second call to __init__ should not alter the existing engine.
        """
        original_engine = self.db_manager.get_engine()
        # A second call to __init__ should not change the engine.
        self.db_manager.__init__(config_instance=self.mock_config, env="test")
        assert self.db_manager.get_engine() is original_engine

    def test_engine_creation_exception(self):
        """
        Test exception handling during engine creation.

        Patches create_engine to simulate an exception and verifies the error message.
        """
        with patch(
            "threatxmanager.dbmanager.connection.create_engine",
            side_effect=Exception("engine error"),
        ):
            DBManager._instance = None
            with pytest.raises(Exception, match="Error creating database engine: engine error"):
                DBManager(config_instance=self.mock_config, env="test")

    def test_create_exception(self):
        """
        Test the exception branch in the create method.

        Simulates an exception during commit and verifies that rollback and session close are called.
        """
        dummy = DummyModel(name="Exception Test")
        fake_session = MagicMock()
        fake_session.commit.side_effect = Exception("commit error")
        # Also simulate that refresh is not called.
        with patch.object(self.db_manager, "get_session", return_value=fake_session):
            with pytest.raises(Exception, match="commit error"):
                self.db_manager.create(dummy)
            fake_session.rollback.assert_called_once()
            fake_session.close.assert_called_once()

    def test_update_exception(self):
        """
        Test the exception branch in the update method.

        Simulates an exception during commit and verifies that rollback and session close are called.
        """
        dummy = DummyModel(name="Old Name")
        created = self.db_manager.create(dummy)
        fake_session = MagicMock()
        fake_session.merge.return_value = created
        fake_session.commit.side_effect = Exception("commit error")
        with patch.object(self.db_manager, "get_session", return_value=fake_session):
            with pytest.raises(Exception, match="commit error"):
                self.db_manager.update(created, name="New Name")
            fake_session.rollback.assert_called_once()
            fake_session.close.assert_called_once()

    def test_delete_exception(self):
        """
        Test the exception branch in the delete method.

        Simulates an exception during commit and verifies that rollback and session close are called.
        """
        dummy = DummyModel(name="To be deleted")
        created = self.db_manager.create(dummy)
        fake_session = MagicMock()
        fake_session.commit.side_effect = Exception("commit error")
        with patch.object(self.db_manager, "get_session", return_value=fake_session):
            with pytest.raises(Exception, match="commit error"):
                self.db_manager.delete(created)
            fake_session.rollback.assert_called_once()
            fake_session.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
