from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class CitizenCreate(BaseModel):
    name: str
    date_of_birth: date
    residence_state: str
    monthly_income: float = 0.0
    household_size: int = 1
    disabilities: List[str] = []

class SchemeCreate(BaseModel):
    title: str
    description: str
    eligibility_rules: List[dict]
    required_documents: List[str] = []
    source_url: Optional[str] = None
