# gov-schemes-prototype

Pilot-ready prototype to help Indian citizens discover government schemes, check eligibility, and submit applications.

Repository layout
- backend/ — FastAPI service, rules engine, DB models, seed loader
- frontend/ — static frontend (HTML + JS)
- infra/ — docker-compose for local testing (docker-compose.yml at repo root)
- docs/ — pilot plan, India privacy checklist, data dictionary, API spec
- sample_data/ — CSVs for citizens and schemes
- .github/ — CI workflow skeleton

Quick local run (docker-compose)
1. Install Docker and docker-compose.
2. From repo root:
   docker-compose up --build
3. Backend: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs
4. Frontend: http://localhost:8080

Seed sample data (optional)
- POST http://localhost:8000/api/v1/admin/token  (use admin credentials in backend/.env)
- POST http://localhost:8000/api/v1/admin/load-sample  (use admin JWT to call)

Important before pilot
- Update backend/.env: change SECRET_KEY, ADMIN_USERNAME, ADMIN_PASSWORD.
- For India pilot (50k+), deploy to in-region infrastructure and follow docs/privacy_checklist_india.md.

See docs/ for full pilot plan, privacy checklist, and data dictionary.
