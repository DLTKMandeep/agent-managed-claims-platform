"""Tests for Bolt 2: agent framework, roster, Intake Clerk and Claims Validator."""
import json
from types import SimpleNamespace

import pytest

from agents.base import AGENTS_DIR, WorkLog, load_roster
from agents.intake import IntakeAgent
from agents.run import run
from agents.validation import ValidationAgent
from data.generate import generate


# ---------- roster and job descriptions ----------

def test_roster_lists_the_whole_team():
    roster = load_roster()
    assert roster["manager"]["title"] == "Director, Claims Operations"
    assert set(roster["agents"]) == {"orchestrator", "intake", "validation", "clinical_review",
                                     "coding", "pricing", "submission"}
    for key in ("intake", "validation"):
        a = roster["agents"][key]
        assert a["status"] == "deployed"
        assert a["employee_id"].endswith(a["version"])
        assert a["reports_to"] == "orchestrator"


def test_job_descriptions_say_when_to_ask_the_manager():
    for key in ("intake", "validation"):
        text = (AGENTS_DIR / load_roster()["agents"][key]["prompt"]).read_text()
        assert "When to ask your manager" in text
        assert "JSON only" in text


def test_planned_agents_cannot_be_hired_early():
    from agents.base import Agent

    class Coder(Agent):
        key = "coding"
    with pytest.raises(RuntimeError):
        Coder()


# ---------- simulated mode against the answer key ----------

def test_perfect_agents_catch_everything_with_no_false_alarms():
    _, scores = run(200, 42)
    assert scores["intake"] == {"processed": 200, "escalated": 8, "caught": 8,
                                "false_positives": 0, "false_negatives": 0}
    assert scores["validation"]["caught"] == 24
    assert scores["validation"]["false_positives"] == 0
    assert scores["validation"]["false_negatives"] == 0


def test_error_rate_produces_mistakes_but_guardrails_stop_misses():
    _, scores = run(200, 42, error_rate=0.1)
    assert scores["intake"]["false_positives"] > 0
    assert scores["validation"]["false_positives"] > 0
    # Code guardrails escalate known duplicates and blank fields even when the agent errs.
    assert scores["intake"]["false_negatives"] == 0
    assert scores["validation"]["false_negatives"] == 0


def test_work_log_records_every_decision_like_a_timesheet():
    log, _ = run(50, 3)
    assert len(log.by_agent("intake")) == 50
    d = log.decisions[0]
    assert d.employee_id == "INT-1.0" and d.title == "Intake Clerk"
    assert d.reasoning and 0 <= d.confidence <= 1 and d.latency_ms >= 0


def test_work_log_can_be_written_to_disk(tmp_path):
    path = tmp_path / "worklog.jsonl"
    run(10, 1, log_path=path)
    rows = [json.loads(l) for l in path.read_text().splitlines()]
    assert len(rows) >= 10 and {"employee_id", "escalated", "reasoning"} <= set(rows[0])


def test_intake_standardizes_records():
    claims, _ = generate(1, 5)
    messy = json.loads(json.dumps(claims[0]))
    messy["note"] = "  extra   spaces \n here "
    messy["patient"]["name"] = "avery   synthwood"
    d = IntakeAgent().handle(messy)
    rec = d.output["structured_claim"]
    assert rec["note"] == "extra spaces here"
    assert rec["patient"]["name"] == "Avery Synthwood"
    assert len(rec["fingerprint"]) == 16


def test_unreadable_records_are_escalated():
    claims, _ = generate(1, 5)
    bad = dict(claims[0], note="", visit_date="last tuesday")
    d = IntakeAgent().handle(bad)
    assert d.outcome == "unreadable" and d.escalated
    assert "note" in d.escalation_reason and "visit date" in d.escalation_reason


# ---------- live mode, with a stand-in for Claude ----------

class FakeClaude:
    """Mimics anthropic.Anthropic().messages.create with canned replies."""

    def __init__(self, replies):
        self.replies = list(replies)
        self.calls = []
        self.messages = self

    def create(self, **kwargs):
        self.calls.append(kwargs)
        text = self.replies.pop(0)
        return SimpleNamespace(content=[SimpleNamespace(type="text", text=text)],
                               usage=SimpleNamespace(input_tokens=120, output_tokens=30))


def _claim():
    return generate(1, 9)[0][0]


def test_live_mode_uses_the_job_description_and_records_the_model():
    fake = FakeClaude(['{"outcome": "accepted", "reasoning": "New record.", "confidence": 0.97}'])
    d = IntakeAgent(mode="live", client=fake).handle(_claim())
    call = fake.calls[0]
    assert "Job description: Intake Clerk" in call["system"]
    assert call["model"] == "claude-haiku-5-5"
    assert "tool_evidence" in call["messages"][0]["content"]
    assert d.mode == "live" and d.model == "claude-haiku-5-5"
    assert d.outcome == "accepted" and not d.escalated
    assert (d.input_tokens, d.output_tokens) == (120, 30)


def test_live_mode_accepts_json_in_code_fences():
    fake = FakeClaude(['```json\n{"outcome": "valid", "reasoning": "All present.", "confidence": 0.9}\n```'])
    d = ValidationAgent(mode="live", client=fake).handle(_claim())
    assert d.outcome == "valid"


def test_live_mode_retries_once_then_escalates_bad_output():
    fake = FakeClaude(["Sure! The claim looks fine.", '{"outcome": "maybe"}'])
    d = IntakeAgent(mode="live", client=fake).handle(_claim())
    assert len(fake.calls) == 2
    assert d.escalated and "handoff contract" in d.escalation_reason
    assert (d.input_tokens, d.output_tokens) == (240, 60)


def test_guardrail_escalates_a_duplicate_even_if_the_model_accepts_it():
    claim = _claim()
    fake = FakeClaude(['{"outcome": "accepted", "reasoning": "New.", "confidence": 0.9}'] * 2)
    agent = IntakeAgent(mode="live", client=fake)
    agent.handle(claim)
    d = agent.handle(dict(claim, claim_id="CLM-99999"))
    assert d.outcome == "accepted"          # the model got it wrong...
    assert d.escalated                       # ...but the code guardrail caught it
    assert "duplicate" in d.escalation_reason.lower()


def test_validator_may_infer_a_value_only_if_it_says_where():
    claim = _claim()
    claim["patient"]["member_id"] = ""
    vague = FakeClaude(['{"outcome": "valid", "reasoning": "Looks fine.", "confidence": 0.8}'])
    assert ValidationAgent(mode="live", client=vague).handle(claim).escalated
    sourced = FakeClaude(['{"outcome": "valid", "reasoning": "Member ID stated in the note.", '
                          '"confidence": 0.85, "inferred": {"patient.member_id": "SYN-123456"}}'])
    assert not ValidationAgent(mode="live", client=sourced).handle(claim).escalated
