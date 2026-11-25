"""Generate synthetic claims and a hidden answer key.

Usage:
    python -m data.generate --count 200 --seed 42 --out data/out

Writes two files:
    claims.jsonl      what the agents see (no answers)
    answer_key.jsonl  the correct outcome for every claim (never shown to agents)
"""
import argparse
import copy
import json
import random
from datetime import date, timedelta
from pathlib import Path

from data.reference import SPECIALTIES, claim_total
from data.scenarios import SCENARIOS, UNPRICED_SCENARIOS, UNUSUAL_TOTAL

MESSY_SHARE = 0.30

# Each messy issue and the pipeline stage that should catch it.
ISSUES = {
    "missing_member_id": "validation",
    "missing_provider_npi": "validation",
    "missing_dob": "validation",
    "duplicate": "intake",
    "vague_note": "clinical_review",
    "conflicting_note": "clinical_review",
    "code_not_in_dictionary": "pricing",
    "unusual_total": "pricing",
}

FIRST = ["Avery", "Jordan", "Riley", "Morgan", "Casey", "Quinn", "Rowan", "Sasha",
         "Devon", "Harper", "Emerson", "Reese", "Parker", "Skyler", "Dakota", "Hayden"]
LAST = ["Synthwood", "Testbrook", "Mockley", "Sampleton", "Fakehurst", "Demoford",
        "Proto", "Placer", "Simmons-Synth", "Example", "Fixture", "Stubbins"]
PROVIDERS = {
    "primary_care": ["Dr. Lena Synth", "Dr. Omar Testa"],
    "cardiology": ["Dr. Priya Mockwell", "Dr. Ben Sampleheart"],
    "orthopedics": ["Dr. Carla Bonesynth", "Dr. Ivan Fixture"],
    "dermatology": ["Dr. Mei Dermock", "Dr. Sam Placeholder"],
}


def fake_npi(rng):
    # Real NPIs start with 1 or 2; a leading 9 guarantees this one is fake.
    return "9" + "".join(str(rng.randint(0, 9)) for _ in range(9))


def fake_patient(rng):
    dob = date(1945, 1, 1) + timedelta(days=rng.randint(0, 22000))
    return {
        "name": f"{rng.choice(FIRST)} {rng.choice(LAST)}",
        "dob": dob.isoformat(),
        "member_id": "SYN-" + "".join(str(rng.randint(0, 9)) for _ in range(6)),
    }


def plan_issues(count, rng):
    """Exactly 30% messy, spread evenly across issue types, in random order."""
    n_messy = round(count * MESSY_SHARE)
    types = list(ISSUES)
    plan = [types[i % len(types)] for i in range(n_messy)] + [None] * (count - n_messy)
    rng.shuffle(plan)
    # A duplicate needs an earlier claim to copy.
    while plan[0] == "duplicate":
        rng.shuffle(plan)
    return plan


def pick_scenario(issue, specialty, rng):
    by_id = {s["id"]: s for s in SCENARIOS}
    if issue == "code_not_in_dictionary":
        return rng.choice(UNPRICED_SCENARIOS)
    if issue == "unusual_total":
        return by_id[UNUSUAL_TOTAL["scenario"]]
    return rng.choice([s for s in SCENARIOS if s["specialty"] == specialty])


def generate(count=200, seed=42):
    rng = random.Random(seed)
    plan = plan_issues(count, rng)
    claims, answers = [], []
    received = date(2026, 11, 23)

    for i, issue in enumerate(plan):
        claim_id = f"CLM-{10400 + i}"

        if issue == "duplicate":
            src_index = rng.randrange(len(claims))
            claim = copy.deepcopy(claims[src_index])
            answer = copy.deepcopy(answers[src_index])
            claim["claim_id"] = claim_id
            answer.update(claim_id=claim_id, is_clean=False, issue="duplicate",
                          expected_escalation_stage="intake", expected_valid=False,
                          duplicate_of=claims[src_index]["claim_id"])
            claims.append(claim)
            answers.append(answer)
            continue

        specialty = SPECIALTIES[i % len(SPECIALTIES)]
        scenario = pick_scenario(issue, specialty, rng)
        lines = copy.deepcopy(scenario["cpt"])
        note = scenario["clear"]
        if issue == "vague_note":
            note = scenario["vague"]
        elif issue == "conflicting_note":
            note = scenario["conflict"]
        elif issue == "unusual_total":
            lines[0]["units"] = UNUSUAL_TOTAL["units"]
            note = UNUSUAL_TOTAL["note"]

        patient = fake_patient(rng)
        provider = {"name": rng.choice(PROVIDERS[scenario["specialty"]]),
                    "npi": fake_npi(rng), "specialty": scenario["specialty"]}
        if issue == "missing_member_id":
            patient["member_id"] = ""
        elif issue == "missing_dob":
            patient["dob"] = ""
        elif issue == "missing_provider_npi":
            provider["npi"] = ""

        visit = received - timedelta(days=rng.randint(1, 20))
        claims.append({
            "claim_id": claim_id,
            "received_at": received.isoformat(),
            "visit_date": visit.isoformat(),
            "patient": patient,
            "provider": provider,
            "note": note,
        })
        answers.append({
            "claim_id": claim_id,
            "scenario_id": scenario["id"],
            "specialty": scenario["specialty"],
            "is_clean": issue is None,
            "issue": issue,
            "expected_escalation_stage": ISSUES.get(issue),
            "expected_valid": issue not in ("missing_member_id", "missing_dob", "missing_provider_npi"),
            "icd10": scenario["icd10"],
            "cpt": lines,
            "expected_total": claim_total(lines),
        })
    return claims, answers


def write_jsonl(path, rows):
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--count", type=int, default=200)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", default="data/out")
    args = ap.parse_args()
    claims, answers = generate(args.count, args.seed)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    write_jsonl(out / "claims.jsonl", claims)
    write_jsonl(out / "answer_key.jsonl", answers)
    messy = sum(1 for a in answers if not a["is_clean"])
    print(f"Wrote {len(claims)} claims ({len(claims) - messy} clean, {messy} messy) to {out}/")


if __name__ == "__main__":
    main()
