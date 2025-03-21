from sqlalchemy import BigInteger, Column, DateTime, Integer, Text

from threatxmanager.dbmanager.models import BaseModel


class Certificate(BaseModel):
    """
    Modelo para armazenar os dados dos certificados extraídos do JSON

    Campos do JSON:
      - id (BigInteger): Identificador do certificado (usado como chave primária)
      - issuer_ca_id (BigInteger)
      - issuer_name (Text)
      - common_name (Text)
      - name_value (Text)
      - entry_timestamp (DateTime)
      - not_before (DateTime)
      - not_after (DateTime)
      - serial_number (Text)
      - result_count (Integer)
    """

    __tablename__ = "certificates"

    issuer_ca_id = Column(BigInteger, nullable=False)
    issuer_name = Column(Text, nullable=False)
    common_name = Column(Text, nullable=False)
    name_value = Column(Text, nullable=False)
    entry_timestamp = Column(DateTime, nullable=False)
    not_before = Column(DateTime, nullable=False)
    not_after = Column(DateTime, nullable=False)
    serial_number = Column(Text, nullable=False)
    result_count = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Certificate(id={self.id}, common_name='{self.common_name}')>"
