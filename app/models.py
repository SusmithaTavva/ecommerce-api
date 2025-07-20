from pydantic import BaseModel
from typing import List, Optional

class Size(BaseModel):
    size: str
    quantity: int

class ProductCreate(BaseModel):
    name: str
    price: float
    sizes: Optional[List[Size]] = None

class ProductResponse(BaseModel):
    id: str
    name: str
    price: float
    sizes: Optional[List[Size]] = None

class OrderItem(BaseModel):
    productId: str
    qty: int

class OrderCreate(BaseModel):
    userId: str
    items: List[OrderItem]

class OrderResponse(BaseModel):
    id: str

class OrderDetails(BaseModel):
    name: str
    id: str
    qty: int

class GetOrdersResponse(BaseModel):
    data: List[dict]
    total: float
    page: dict