"""Handoff contracts between agents. Bad output is caught here, not passed on."""
from datetime import date, datetime, timezone
from typing import Literal, Optional

from pydantic import BaseModel, Field


class Patient(BaseModel):
    name: str
    dob: str
    member_id: str


class Provider(BaseModel):
    name: str
    npi: str
    specialty: str


class RawClaim(BaseModel):
    claim_id: str
    received_at: str
    visit_date: str
    patient: Patient
    provider: Provider
    note: str


class StructuredClaim(RawClaim):
    """A claim after intake: same fields, normalized, with a fingerprint."""
    fingerprint: str


class AgentOutcome(BaseModel):
    """What a model (or the simulator) must return. Validated before use."""
    outcome: str
    reasoning: str = Field(min_length=1)
    confidence: float = Field(ge=0.0, le=1.0)
    inferred: dict[str, str] = Field(default_factory=dict)


class IntakeOutcome(AgentOutcome):
    outcome: Literal["accepted", "duplicate", "unreadable"]


class ValidationOutcome(AgentOutcome):
    outcome: Literal["valid", "invalid"]


class Decision(BaseModel):
    """One entry in an agent's work log: the unit every scorecard is built from."""
    claim_id: str
    agent_key: str
    employee_id: str
    title: str
    version: str
    mode: Literal["simulated", "live"]
    model: Optional[str] = None
    outcome: str
    reasoning: str
    confidence: float
    escalated: bool
    escalation_reason: Optional[str] = None
    evidence: dict = Field(default_factory=dict)
    output: dict = Field(default_factory=dict)
    latency_ms: float
    input_tokens: int = 0
    output_tokens: int = 0
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
