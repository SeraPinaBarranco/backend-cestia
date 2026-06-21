from pydantic import BaseModel
from typing import List, Optional

class Producto(BaseModel):
    nombre: str
    cantidad: Optional[float] = None
    unidad: Optional[str] = None      # kg, ud, l
    precio_unitario: Optional[float] = None
    precio_total: float

class TicketResponse(BaseModel):
    supermercado: Optional[str] = None
    fecha: Optional[str] = None
    productos: List[Producto]
    subtotal: Optional[float] = None
    iva: Optional[float] = None
    total: Optional[float] = None