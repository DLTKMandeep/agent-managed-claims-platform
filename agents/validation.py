"""Claims Validator: confirms every field an insurer needs is present."""
from agents.base import Agent
from agents.schemas import ValidationOutcome

REQUIRED = [
    ("patient", "name"), ("patient", "dob"), ("patient", "member_id"),
    ("provider", "name"), ("provider", "npi"), ("provider", "specialty"),
    (None, "visit_date"), (None, "note"),
]


def missing_fields(claim):
    missing = []
    for group, field in REQUIRED:
        value = (claim.get(group) or {}).get(field) if group else claim.get(field)
        if not str(value or "").strip():
            missing.append(f"{group}.{field}" if group else field)
    return missing


class ValidationAgent(Agent):
    key = "validation"
    outcome_model = ValidationOutcome

    def gather_evidence(self, claim):
        return {"missing_fields": missing_fields(claim)}

    def simulate(self, claim, evidence):
        missing = evidence["missing_fields"]
        if missing:
            outcome = self.maybe_err("invalid", "valid")
        else:
            outcome = self.maybe_err("valid", "invalid")
        reasons = {
            "invalid": f"Missing required field(s): {', '.join(missing) or 'flagged on review'}; not found elsewhere in the record.",
            "valid": "All required fields are present.",
        }
        return {"outcome": outcome, "reasoning": reasons[outcome], "confidence": 0.92}

    def escalation_reason(self, outcome, evidence):
        if outcome.outcome == "invalid":
            return "Required data missing: " + (", ".join(evidence["missing_fields"]) or "see reasoning")
        # Guardrail: a model may only call a claim valid despite blanks if it says where it found them.
        unresolved = [f for f in evidence["missing_fields"] if f not in outcome.inferred]
        if unresolved:
            return "Marked valid but required data is still missing: " + ", ".join(unresolved)
        return None

    def build_output(self, claim, outcome, evidence):
        return {"validated_claim": claim, "inferred": outcome.inferred} if outcome.outcome == "valid" else {}
