from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, String

from threatxmanager.dbmanager.models import BaseModel


class StixObject(BaseModel):
    """
    Represents a STIX (Structured Threat Information Expression) object stored in the database

    Attributes:
        __tablename__ (str): The name of the database table associated with this model.
        stix_id (str): The unique identifier for the STIX object. Acts as the primary key.
        stix_type (str): The type of the STIX object (e.g., indicator, malware, etc.). Cannot be null.
        data (dict): A JSON field containing the serialized data of the STIX object.
        created_at (datetime): The timestamp when the STIX object was created. Defaults to the current UTC time.
        updated_at (datetime): The timestamp when the STIX object was last updated. Automatically updated on modification.
    """

    __tablename__ = "stix_objects"
    stix_id = Column(String(255), primary_key=True)
    stix_type = Column(String(100), nullable=False)
    data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
