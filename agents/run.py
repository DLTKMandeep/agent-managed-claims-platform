"""Run the deployed agents over synthetic claims and print a first scorecard.

    python -m agents.run                      # simulated, no API key needed
    python -m agents.run --error-rate 0.1     # watch the scorecard react to mistakes
    python -m agents.run --mode live --count 20   # needs ANTHROPIC_API_KEY
"""
import argparse

from agents.base import WorkLog
from agents.intake import IntakeAgent
from agents.validation import ValidationAgent
from data.generate import generate


def run(count=200, seed=42, mode="simulated", error_rate=None, log_path=None):
    claims, answers = generate(count, seed)
    key = {a["claim_id"]: a for a in answers}
    log = WorkLog(log_path)
    intake = IntakeAgent(mode=mode, error_rate=error_rate, seed=seed, worklog=log)
    validator = ValidationAgent(mode=mode, error_rate=error_rate, seed=seed + 1, worklog=log)

    for claim in claims:
        d = intake.handle(claim)
        if d.output.get("structured_claim"):
            validator.handle(d.output["structured_claim"])

    def score(agent_key, is_problem):
        tp = fp = fn = tn = 0
        for d in log.by_agent(agent_key):
            actual = is_problem(key[d.claim_id])
            flagged = d.escalated
            tp += actual and flagged
            fp += (not actual) and flagged
            fn += actual and not flagged
            tn += (not actual) and not flagged
        return {"processed": tp + fp + fn + tn, "escalated": tp + fp,
                "caught": tp, "false_positives": fp, "false_negatives": fn}

    return log, {
        "intake": score("intake", lambda a: a["issue"] == "duplicate"),
        "validation": score("validation", lambda a: not a["expected_valid"]),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=200)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--mode", choices=["simulated", "live"], default="simulated")
    ap.add_argument("--error-rate", type=float, default=None)
    ap.add_argument("--log", default=None, help="optional path for the work log (JSON lines)")
    args = ap.parse_args()
    _, scores = run(args.count, args.seed, args.mode, args.error_rate, args.log)
    titles = {"intake": "Intake Clerk (INT-1.0)", "validation": "Claims Validator (VAL-1.0)"}
    print(f"{'Agent':28} {'Processed':>9} {'Escalated':>9} {'Caught':>7} {'False +':>8} {'False -':>8}")
    for k, s in scores.items():
        print(f"{titles[k]:28} {s['processed']:>9} {s['escalated']:>9} {s['caught']:>7} "
              f"{s['false_positives']:>8} {s['false_negatives']:>8}")


if __name__ == "__main__":
    main()
