# Data Dictionary (summary)

Citizens
- id (UUID): internal id
- name (string)
- date_of_birth (date)
- residence_state (string)
- monthly_income (numeric)
- household_size (int)
- disabilities (list[string])
- created/updated timestamps

Schemes
- id (UUID)
- title (string)
- description (text)
- eligibility_rules (JSON): list of rule objects {field, operator, value}
- required_documents (list[string])
- source_url (string)

Applications
- id (UUID)
- scheme_id (UUID)
- citizen_id (UUID)
- status (string)
- submitted_documents (JSON)
- adjudication (JSON)
- audit trail entries

Rule object (example)
- { "field": "date_of_birth", "operator": "age_gte", "value": 60 }
- Operators supported (prototype): equals, in, age_gte, age_lte, numeric_gte, numeric_lte

Notes
- Do not store Aadhaar or biometrics in the pilot unless legally approved. Store minimal PII and encrypt sensitive fields in production.
