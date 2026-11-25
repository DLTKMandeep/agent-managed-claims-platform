"""Intake Clerk: standardizes records and stops duplicates and unreadable claims."""
import hashlib
from datetime import date

from agents.base import Agent
from agents.schemas import IntakeOutcome, RawClaim


def _iso_ok(value):
    try:
        date.fromisoformat(value)
        return True
    except (TypeError, ValueError):
        return False


def normalize(record):
    """Standard format: trimmed text, collapsed spaces, title-case names."""
    clean = lambda s: " ".join(str(s or "").split())
    out = {
        "claim_id": clean(record.get("claim_id")),
        "received_at": clean(record.get("received_at")),
        "visit_date": clean(record.get("visit_date")),
        "patient": {k: clean(v) for k, v in (record.get("patient") or {}).items()},
        "provider": {k: clean(v) for k, v in (record.get("provider") or {}).items()},
        "note": clean(record.get("note")),
    }
    for group in ("patient", "provider"):
        if out[group].get("name"):
            out[group]["name"] = out[group]["name"].title()
    return out


def fingerprint(rec):
    """Same patient, provider, visit and note means the same claim."""
    p, v = rec["patient"], rec["provider"]
    key = "|".join([p.get("name", "").lower(), p.get("dob", ""), p.get("member_id", ""),
                    v.get("npi", ""), rec.get("visit_date", ""), rec.get("note", "").lower()])
    return hashlib.sha256(key.encode()).hexdigest()[:16]


class IntakeAgent(Agent):
    key = "intake"
    outcome_model = IntakeOutcome

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.seen = {}  # fingerprint -> first claim_id

    def gather_evidence(self, record):
        rec = normalize(record)
        problems = []
        if not rec["note"]:
            problems.append("doctor's note is empty")
        if not _iso_ok(rec["visit_date"]):
            problems.append("visit date is not a valid date")
        fp = fingerprint(rec)
        seen_before = self.seen.get(fp)
        if seen_before is None and not problems:
            self.seen[fp] = rec["claim_id"]
        return {"fingerprint": fp, "seen_before": seen_before, "problems": problems}

    def simulate(self, record, evidence):
        if evidence["problems"]:
            return {"outcome": "unreadable", "confidence": 0.95,
                    "reasoning": "Cannot process: " + "; ".join(evidence["problems"]) + "."}
        if evidence["seen_before"]:
            outcome = self.maybe_err("duplicate", "accepted")
        else:
            outcome = self.maybe_err("accepted", "duplicate")
        reasons = {
            "duplicate": f"Same patient, provider, visit and note as {evidence['seen_before'] or 'an earlier claim'}.",
            "accepted": "New, readable record; standardized and passed to validation.",
        }
        return {"outcome": outcome, "reasoning": reasons[outcome], "confidence": 0.9}

    def escalation_reason(self, outcome, evidence):
        # Guardrail in code: a known duplicate is escalated even if the model accepted it.
        if evidence["seen_before"] or outcome.outcome == "duplicate":
            return f"Possible duplicate of {evidence['seen_before'] or 'an earlier claim'}"
        if outcome.outcome == "unreadable":
            return "Unreadable record: " + "; ".join(evidence["problems"] or ["see reasoning"])
        return None

    def build_output(self, record, outcome, evidence):
        if outcome.outcome != "accepted" or evidence["seen_before"]:
            return {}
        rec = normalize(record)
        rec["fingerprint"] = evidence["fingerprint"]
        RawClaim(**{k: v for k, v in rec.items() if k != "fingerprint"})  # contract check
        return {"structured_claim": rec}
