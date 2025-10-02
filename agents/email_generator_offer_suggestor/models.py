from pydantic import BaseModel, field_validator
from typing import List, Dict, Optional, Union

class CartItem(BaseModel):
    product_id: int
    name: str
    price: float
    quantity: int
    category: Optional[str] = None
    description: Optional[str] = None
    stock_quantity: Optional[int] = None

class Offer(BaseModel):
    type: str  # e.g., "discount", "free_shipping"
    value: str  # e.g., "10%", "Free"
    description: str

class EmailData(BaseModel):
    user_id: Optional[str] = None
    email: str
    name: Optional[str] = None
    items: List[Dict]  # From abandonment data - cart items with product info
    recommendations: Optional[List[Dict]] = []
    behavior: Optional[Dict] = {}
    persona: Optional[str] = "valued_customer"  # e.g., "loyal", "first_time"

class GeneratedEmail(BaseModel):
    subject: str
    body: str
    offers: List[Offer]
    recommendations: Optional[List[str]] = []
    total_savings: Optional[float] = 0.0
    final_amount: Optional[float] = 0.0