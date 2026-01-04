from sqlmodel import SQLModel, Field
from typing import Optional, List, Dict, Any
from datetime import date
import uuid

def gen_uuid():
    return str(uuid.uuid4())

class Citizen(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=gen_uuid, primary_key=True)
    name: str
    date_of_birth: date
    residence_state: str
    monthly_income: float = 0.0
    household_size: int = 1
    disabilities: List[str] = Field(default_factory=list)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "date_of_birth": str(self.date_of_birth),
            "residence_state": self.residence_state,
            "monthly_income": self.monthly_income,
            "household_size": self.household_size,
            "disabilities": self.disabilities
        }

class Scheme(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=gen_uuid, primary_key=True)
    title: str
    description: str
    eligibility_rules: List[Dict[str, Any]] = Field(default_factory=list)
    required_documents: List[str] = Field(default_factory=list)
    source_url: Optional[str] = None

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "eligibility_rules": self.eligibility_rules,
            "required_documents": self.required_documents,
            "source_url": self.source_url
        }
