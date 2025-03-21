# dbmanager/models/venda.py

from sqlalchemy import Column, Date, Float, Integer, String

from threatxmanager.dbmanager.models import BaseModel


class Venda(BaseModel):
    __tablename__ = "vendas"  # Explicitly set the table name to "vendas"

    sale_date = Column(Date, nullable=False)
    customer = Column(String(100), nullable=False)
    product = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)

    def __repr__(self):
        return (
            f"<Venda(id={self.id}, sale_date={self.sale_date}, "
            f"customer='{self.customer}', product='{self.product}', "
            f"quantity={self.quantity}, unit_price={self.unit_price})>"
        )
