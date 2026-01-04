# Pilot Plan — India (50k+ users)

Objectives
- Validate accuracy of eligibility rules at scale.
- Validate ingestion & rule management for diverse schemes.
- Validate onboarding flows, notifications, and human-review workflow.

Scope
- Region: targeted states (pick 1–3 states).
- Users: up to 50,000 pilot registrations over 8–12 weeks.
- Schemes: 5–10 initial schemes across categories.

Infrastructure recommendations
- Managed Postgres in India region (AWS RDS ap-south-1, GCP Mumbai, or Azure India Central).
- Kubernetes cluster (GKE/AKS/EKS) in India region with HPA & node pools.
- Redis cache & Celery/RQ for background jobs.
- Object storage in-region (S3 / Cloud storage).
- Use queue-based processing for ingestion and document OCR.

Operational plan
- Week -4: Legal review, data residency confirmation, consent text in regional languages.
- Week 0: Provision infra, create test users, import sample schemes.
- Week 1–2: Onboard 5k users via partners (offline + digital).
- Week 3–8: Scale to 50k, monitor KPIs, iterate on UX and rules.
- Final 2 weeks: Analyze results, prepare report.

KPIs
- Eligibility match precision and recall vs. human adjudication.
- % applications requiring manual review (target < 15%).
- Average response time for eligibility API (< 200ms median).
- User satisfaction (survey).
