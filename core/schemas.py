from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class StockRowSchema(BaseModel):
    item_code: str = Field(..., alias="ItemCode")
    serial_number: Optional[str] = Field(None, alias="Serial")
    quantity: int = Field(..., alias="Cantidad")
    unit_cost: float = Field(..., alias="Costo unitario")
    in_date: Optional[datetime] = Field(None, alias="Indate")

    class Config:
        populate_by_name = True


class TransitRowSchema(BaseModel):
    item_code: str = Field(..., alias="ItemCode")
    supplier: str = Field(..., alias="CardName")
    quantity: int = Field(..., alias="OpenQty")
    unit_cost: float = Field(..., alias="PrecioUnitUsd")
    delivery_month: int = Field(..., alias="MesEntrega")
    delivery_year: int = Field(..., alias="Año")
    transit_type: str = Field(..., alias="TipoTransito") # 'REAL' o 'PROYECTADO'

    class Config:
        populate_by_name = True


class BacklogRowSchema(BaseModel):
    item_code: str = Field(..., alias="Código")
    customer: str = Field(..., alias="Cliente")
    quantity: int = Field(..., alias="Cantidad")
    unit_price: float = Field(..., alias="Costo unitario promedio")
    project_code: str = Field(..., alias="PC")
    executive: str = Field(..., alias="Ejecutivo Responsable")
    quarter: int = Field(..., alias="Trimestre")

    class Config:
        populate_by_name = True
