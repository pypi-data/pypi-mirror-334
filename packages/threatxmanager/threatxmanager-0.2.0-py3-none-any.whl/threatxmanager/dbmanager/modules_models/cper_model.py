from sqlalchemy import JSON, Boolean, Column, String

from threatxmanager.dbmanager.models import BaseModel


class CPERecord(BaseModel):
    """
    Represents a record in the 'cpe_records' table, which stores Common Platform Enumeration (CPE) data.

    Attributes:
        id (str): The primary key identifier for the record.
        cpe (str): The Common Platform Enumeration (CPE) string, which uniquely identifies a hardware or software product.
        is_hardware (bool): Indicates whether the CPE represents hardware (True) or not (False).
        vendor (str, optional): The vendor or manufacturer of the product.
        name (str, optional): The name of the product.
        version (str, optional): The version of the product.
        language (str, optional): The language associated with the product.
        raw_data (dict): The raw JSON data associated with the CPE record.
    """

    __tablename__ = "cpe_records"
    id = Column(String(255), primary_key=True)
    cpe = Column(String(255), nullable=False)
    is_hardware = Column(Boolean, nullable=False)
    vendor = Column(String(255))
    name = Column(String(255))
    version = Column(String(50))
    language = Column(String(50))
    raw_data = Column(JSON)
