from pydantic import BaseModel
from typing import List, Dict, Optional

class CartItem(BaseModel):
    product_id: int
    name: str
    price: float
    quantity: int

class UserBehavior(BaseModel):
    pages_viewed: int
    idle_time: int  # in seconds
    session_duration: int  # in seconds

class CartData(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None
    items: List[CartItem]
    timestamp: float
    behavior: UserBehavior

class AbandonmentResponse(BaseModel):
    abandoned: bool
    data: Optional[Dict] = None