from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.db import create_db_and_tables, get_engine, get_session
from app import models, rules
from app.schemas import CitizenCreate
from sqlalchemy.orm import Session
import os

app = FastAPI(title="Gov Schemes Prototype (Pilot)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data.db")
engine = get_engine(DATABASE_URL)
create_db_and_tables(engine)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/v1/citizens", status_code=201)
def create_citizen(payload: CitizenCreate):
    with get_session() as session:
        citizen = models.Citizen.from_orm(payload)
        session.add(citizen)
        session.commit()
        session.refresh(citizen)
    return {"citizen_id": citizen.id}


@app.get("/api/v1/citizens/{citizen_id}/eligible-schemes")
def eligible_schemes(citizen_id: str):
    with get_session() as session:
        citizen = session.get(models.Citizen, citizen_id)
        if not citizen:
            raise HTTPException(status_code=404, detail="Citizen not found")
        schemes = session.query(models.Scheme).all()
        results = []
        for s in schemes:
            eval_res = rules.evaluate_scheme_for_citizen(s, citizen)
            results.append({
                "scheme_id": s.id,
                "title": s.title,
                "eligible": eval_res["eligible"],
                "details": eval_res["details"],
                "required_documents": s.required_documents,
                "description": s.description
            })
    return {"citizen": {"id": citizen.id, "name": citizen.name}, "matches": results}


# Admin endpoints (token-based simple auth for pilot)
from app.admin import router as admin_router
app.include_router(admin_router, prefix="/api/v1/admin", tags=["admin"])

# Schemes public listing
@app.get("/api/v1/schemes")
def list_schemes():
    with get_session() as session:
        schemes = session.query(models.Scheme).all()
        return [s.to_dict() for s in schemes]
