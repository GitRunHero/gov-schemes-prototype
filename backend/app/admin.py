from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.db import get_session
from app import models
from app.schemas import SchemeCreate
from sqlalchemy.orm import Session
import os
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel

router = APIRouter()
SECRET_KEY = os.getenv("SECRET_KEY", "change_this")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Simple admin (for pilot)
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "adminpass")

class Token(BaseModel):
    access_token: str
    token_type: str

def create_access_token(data: dict, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != ADMIN_USERNAME or form_data.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    token = create_access_token({"sub": ADMIN_USERNAME})
    return {"access_token": token, "token_type": "bearer"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/admin/token")

def admin_required(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        if sub != ADMIN_USERNAME:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    return True

@router.post("/schemes")
def add_scheme(payload: SchemeCreate, ok: bool = Depends(admin_required)):
    with get_session() as session:
        s = models.Scheme(title=payload.title, description=payload.description,
                          eligibility_rules=payload.eligibility_rules,
                          required_documents=payload.required_documents,
                          source_url=payload.source_url)
        session.add(s)
        session.commit()
        session.refresh(s)
    return {"scheme_id": s.id}

@router.post("/load-sample")
def load_sample(ok: bool = Depends(admin_required)):
    sample1 = {
        "title": "Senior Health Check (StateX)",
        "description": "Annual free health check for citizens aged 60+ residing in StateX.",
        "eligibility_rules": [
            {"field": "date_of_birth", "operator": "age_gte", "value": 60},
            {"field": "residence_state", "operator": "equals", "value": "StateX"}
        ],
        "required_documents": ["id_card", "residence_proof"]
    }
    sample2 = {
        "title": "Low Income Family Support",
        "description": "Monthly cash support for households of 3+ with monthly income <= 15000.",
        "eligibility_rules": [
            {"field": "household_size", "operator": "numeric_gte", "value": 3},
            {"field": "monthly_income", "operator": "numeric_lte", "value": 15000}
        ],
        "required_documents": ["id_card", "income_proof"]
    }
    with get_session() as session:
        existing = session.query(models.Scheme).filter(models.Scheme.title == sample1["title"]).first()
        if not existing:
            s1 = models.Scheme(title=sample1["title"], description=sample1["description"],
                        eligibility_rules=sample1["eligibility_rules"], required_documents=sample1["required_documents"])
            session.add(s1)
        existing2 = session.query(models.Scheme).filter(models.Scheme.title == sample2["title"]).first()
        if not existing2:
            s2 = models.Scheme(title=sample2["title"], description=sample2["description"],
                        eligibility_rules=sample2["eligibility_rules"], required_documents=sample2["required_documents"])
            session.add(s2)
        session.commit()
    return {"loaded": True}
