from datetime import date
from app.models import Scheme, Citizen
from typing import Dict, Any, List

def _age_from_dob(dob: date) -> int:
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

def evaluate_operator(field_value, operator: str, target):
    if operator in ("equals", "eq"):
        return field_value == target
    if operator == "in":
        try:
            return field_value in target
        except Exception:
            return False
    if operator == "age_gte":
        return field_value >= target
    if operator == "age_lte":
        return field_value <= target
    if operator == "numeric_gte":
        try:
            return float(field_value) >= float(target)
        except Exception:
            return False
    if operator == "numeric_lte":
        try:
            return float(field_value) <= float(target)
        except Exception:
            return False
    return False

def evaluate_rule(rule: Dict[str, Any], citizen: Citizen) -> Dict[str, Any]:
    field = rule.get("field")
    operator = rule.get("operator")
    target = rule.get("value")
    if field == "date_of_birth":
        field_value = _age_from_dob(citizen.date_of_birth)
    else:
        field_value = getattr(citizen, field, None)
    passed = evaluate_operator(field_value, operator, target)
    return {"rule": rule, "value_evaluated": field_value, "passed": passed}

def evaluate_scheme_for_citizen(scheme: Scheme, citizen: Citizen) -> Dict[str, Any]:
    details = []
    all_pass = True
    for rule in scheme.eligibility_rules:
        res = evaluate_rule(rule, citizen)
        details.append(res)
        if not res["passed"]:
            all_pass = False
    return {"eligible": all_pass, "details": details}
