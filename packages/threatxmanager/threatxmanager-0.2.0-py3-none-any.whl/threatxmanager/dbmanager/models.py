"""
This module provides the base model for SQLAlchemy ORM models.

It defines a declarative base and an abstract BaseModel class that includes
common attributes and functionality shared across all models.
"""

import datetime

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base, declared_attr

Base = declarative_base()


class BaseModel(Base):
    """
    Abstract base model for all ORM models.

    This abstract class defines common attributes for all models, such as a primary key
    (`id`), creation timestamp (`created_at`), and update timestamp (`updated_at`). It also
    dynamically sets the table name to the lowercase name of the class.

    Attributes
    ----------
    id : int
        Primary key of the record, automatically incremented.
    created_at : datetime.datetime
        Timestamp indicating when the record was created. Defaults to the current UTC time.
    updated_at : datetime.datetime
        Timestamp indicating when the record was last updated. Automatically updated on modifications.
    """

    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        """
        Dynamically defines the table name for the model based on the class name.

        The table name is set to the lowercase version of the class name.

        Returns
        -------
        str
            The table name derived from the class name in lowercase.
        """
        return cls.__name__.lower()
