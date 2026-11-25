"""The agent framework: every agent is an employee with a profile, a job
description, tools that gather evidence, and a rule for when to ask the manager.

Two run modes (see aidlc/03-design.md):
  simulated  rule-based decisions with a tunable error rate; no API key needed
  live       Claude makes the decision from the job description and tool evidence
"""
import json
import random
import time
from pathlib import Path

import yaml
from pydantic import ValidationError

from agents.schemas import Decision

AGENTS_DIR = Path(__file__).parent


def load_roster():
    with open(AGENTS_DIR / "roster.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


class WorkLog:
    """Every decision every agent makes. Scorecards are computed from this."""

    def __init__(self, path=None):
        self.decisions = []
        self.path = Path(path) if path else None

    def record(self, decision):
        self.decisions.append(decision)
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(decision.model_dump_json() + "\n")

    def by_agent(self, agent_key):
        return [d for d in self.decisions if d.agent_key == agent_key]


class Agent:
    key = ""                 # roster key, set by each subclass
    outcome_model = None     # pydantic model the decision must match
    max_tokens = 400

    def __init__(self, mode="simulated", client=None, error_rate=None, seed=0, worklog=None):
        if mode not in ("simulated", "live"):
            raise ValueError("mode must be 'simulated' or 'live'")
        roster = load_roster()
        self.profile = roster["agents"][self.key]
        if self.profile.get("status") != "deployed":
            raise RuntimeError(f"{self.profile['title']} is not deployed yet")
        self.job_description = (AGENTS_DIR / self.profile["prompt"]).read_text(encoding="utf-8")
        self.mode = mode
        self.client = client
        if mode == "live" and client is None:
            import anthropic  # only needed for live mode
            self.client = anthropic.Anthropic()
        self.error_rate = self.profile.get("simulated_error_rate", 0.0) if error_rate is None else error_rate
        self.rng = random.Random(seed)
        self.worklog = worklog if worklog is not None else WorkLog()

    # ----- to be provided by each agent -----
    def gather_evidence(self, record):
        """Run this agent's tools. Deterministic facts the decision is based on."""
        raise NotImplementedError

    def simulate(self, record, evidence):
        """Rule-based decision for simulated mode: returns an outcome dict."""
        raise NotImplementedError

    def escalation_reason(self, outcome, evidence):
        """Return why the manager must look at this, or None. Enforced in code."""
        raise NotImplementedError

    def build_output(self, record, outcome, evidence):
        """The deliverable handed to the next agent."""
        return {}

    # ----- shared behaviour -----
    def handle(self, record):
        start = time.perf_counter()
        evidence = self.gather_evidence(record)
        tokens = (0, 0)
        if self.mode == "live":
            outcome, tokens, error = self._decide_live(record, evidence)
        else:
            outcome, error = self.outcome_model(**self.simulate(record, evidence)), None

        reason = error or self.escalation_reason(outcome, evidence)
        decision = Decision(
            claim_id=record["claim_id"],
            agent_key=self.key,
            employee_id=self.profile["employee_id"],
            title=self.profile["title"],
            version=self.profile["version"],
            mode=self.mode,
            model=self.profile["model"] if self.mode == "live" else None,
            outcome=outcome.outcome if outcome else "error",
            reasoning=outcome.reasoning if outcome else error,
            confidence=outcome.confidence if outcome else 0.0,
            escalated=reason is not None,
            escalation_reason=reason,
            evidence=evidence,
            output=self.build_output(record, outcome, evidence) if outcome else {},
            latency_ms=round((time.perf_counter() - start) * 1000, 2),
            input_tokens=tokens[0],
            output_tokens=tokens[1],
        )
        self.worklog.record(decision)
        return decision

    def maybe_err(self, correct, wrong):
        """In simulated mode, make a mistake at the configured error rate."""
        return wrong if self.rng.random() < self.error_rate else correct

    def _decide_live(self, record, evidence):
        message = json.dumps({"claim": record, "tool_evidence": evidence}, indent=2)
        tokens_in = tokens_out = 0
        last_error = None
        for _ in range(2):  # one automatic retry, then escalate
            response = self.client.messages.create(
                model=self.profile["model"],
                max_tokens=self.max_tokens,
                system=self.job_description,
                messages=[{"role": "user", "content": message}],
            )
            usage = getattr(response, "usage", None)
            tokens_in += getattr(usage, "input_tokens", 0) or 0
            tokens_out += getattr(usage, "output_tokens", 0) or 0
            text = "".join(b.text for b in response.content if getattr(b, "type", "") == "text")
            try:
                data = json.loads(_strip_fences(text))
                return self.outcome_model(**data), (tokens_in, tokens_out), None
            except (json.JSONDecodeError, ValidationError, TypeError) as e:
                last_error = e
        return None, (tokens_in, tokens_out), f"Output did not match the handoff contract twice: {type(last_error).__name__}"


def _strip_fences(text):
    t = text.strip()
    if t.startswith("```"):
        t = t.split("\n", 1)[1] if "\n" in t else ""
        t = t.rsplit("```", 1)[0]
    return t.strip()
