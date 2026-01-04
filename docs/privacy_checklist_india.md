# Privacy & Security Checklist — India (Pilot)

Legal & policy
- Conduct a Data Protection Impact Assessment (DPIA) for the pilot.
- Check Aadhaar / UIDAI rules before any use of Aadhaar numbers; avoid storing Aadhaar or biometrics unless fully compliant and signed MoU with UIDAI.
- Consult state-specific notification requirements.

Data residency & hosting
- Host all PII and backups in Indian region data centers.
- Use KMS with keys stored in region and access control for admins.

Consent & transparency
- Provide consent forms and privacy policy in English + Hindi + regional languages for the pilot states.
- Store consent timestamps and versions.

Minimization & retention
- Only collect fields required for eligibility checks.
- Define retention policy (e.g., retain records for pilot period + 1 year, then archive/encrypt).

Encryption & access control
- TLS everywhere.
- AES-256 at rest for sensitive fields.
- Role-based access controls for admin and case workers.
- Logging & immutable audit trail for eligibility decisions.

Operational security
- Vulnerability scanning on CI.
- Regular backups, tested restore.
- Incident response & breach notification plan.

Human review
- All uncertain or borderline decisions must be flagged for manual review before benefits issuance.

Third-party services
- Ensure DPAs with any OCR, SMS, or cloud providers; prefer vendors with Indian data residency.
