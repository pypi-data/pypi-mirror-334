from typing import Any, Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import QueuePool

from threatxmanager.config.manager_config import Config


class DBManagerError(Exception):
    """Custom exception class for DBManager errors."""


class DBManager:
    """
    Singleton for centralized database management using SQLAlchemy.

    This class handles the creation and configuration of the database engine,
    session management, and provides basic CRUD operations.
    """

    _instance: Optional["DBManager"] = None

    def __new__(cls, config_instance: Config | None = None, env: str | None = None) -> "DBManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, config_instance: Config | None = None, env: str | None = None) -> None:
        if self._initialized:
            return

        self.config = config_instance if config_instance is not None else Config()
        env = env if env is not None else self.config.get_default_env()

        # Obtain the "database" section and the "bancode_dados" sub-section.
        database_section = self.config.get("database", {})
        bancode_config = database_section.get("bancode_dados", {})
        db_config = bancode_config.get(env, {})

        if not db_config:
            raise DBManagerError(f"Environment '{env}' not found")
        self.database_url = db_config.get("DATABASE_URL")
        if not self.database_url:
            raise DBManagerError("DATABASE_URL is missing")

        self.pool_size = db_config.get("POOL_SIZE", 10)
        self.max_overflow = db_config.get("MAX_OVERFLOW", 20)
        self.pool_timeout = db_config.get("POOL_TIMEOUT", 30)
        self.echo = db_config.get("ECHO", False)

        try:
            self.engine: Engine = create_engine(
                self.database_url,
                poolclass=QueuePool,
                pool_size=self.pool_size,
                max_overflow=self.max_overflow,
                pool_timeout=self.pool_timeout,
                echo=self.echo,
            )
        except Exception as e:
            raise DBManagerError(f"Error creating database engine: {e}") from e

        # Create a session factory to support CRUD operations.
        self.Session = sessionmaker(bind=self.engine)

        self._initialized = True

    def get_engine(self) -> Engine:
        return self.engine

    def init_db(self, base: Any) -> None:
        base.metadata.create_all(bind=self.engine)

    def get_session(self) -> Session:
        return self.Session()

    def create(self, instance: Any) -> Any:
        session = self.get_session()
        try:
            session.add(instance)
            session.commit()
        except Exception:
            session.rollback()
            raise
        else:
            session.refresh(instance)
            return instance
        finally:
            session.close()

    def read(self, model: type[Any], _id: Any) -> Any | None:
        session = self.get_session()
        try:
            return session.get(model, _id)
        finally:
            session.close()

    def update(self, instance: Any, **kwargs: Any) -> Any:
        session = self.get_session()
        try:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            merged_instance = session.merge(instance)
            session.commit()
        except Exception:
            session.rollback()
            raise
        else:
            session.refresh(merged_instance)
            return merged_instance
        finally:
            session.close()

    def delete(self, instance: Any) -> None:
        session = self.get_session()
        try:
            session.delete(instance)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
