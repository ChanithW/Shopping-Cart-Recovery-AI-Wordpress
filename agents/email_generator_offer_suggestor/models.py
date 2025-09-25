from pydantic import BaseModel, field_validator
from typing import List, Dict, Optional, Union

class Offer(BaseModel):
    type: str  # e.g., "discount", "free_shipping"
    value: str  # e.g., "10%", "Free"
    description: str

class EmailData(BaseModel):
    user_id: Optional[str] = None
    email: str
    name: Optional[str] = None
    items: List[Dict]  # From abandonment data
    recommendations: List[Dict]
    behavior: Dict
    persona: str  # e.g., "loyal", "first_time"

class GeneratedEmail(BaseModel):
    subject: str
    body: str
    offers: List[Offer]