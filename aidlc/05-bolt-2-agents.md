# Bolt 2: Agent framework, Intake Clerk and Claims Validator

**Phase:** Construction
**Status:** Done, 2026-11-24

## What was built

| File | Purpose |
| --- | --- |
| `agents/roster.yaml` | The team roster: every agent's title, comparable role, reporting line, seniority (model), version and employee ID, and whether it is deployed or still planned |
| `agents/prompts/*.md` | Job descriptions, written in plain English. In live mode each one is the agent's system prompt |
| `agents/schemas.py` | Handoff contracts (Pydantic): what each agent must return and what it passes on |
| `agents/base.py` | The framework every agent inherits: tools gather evidence, the agent decides, code enforces escalation rules, and every decision goes in the work log |
| `agents/intake.py` | Intake Clerk: standardizes records, fingerprints them, stops duplicates and unreadable claims |
| `agents/validation.py` | Claims Validator: checks the eight fields an insurer needs |
| `agents/run.py` | Runs both agents over the synthetic claims and prints a first scorecard |
| `tests/test_agents.py` | 14 tests |

## How the employee analogy shows up in code

| Employee | In the code |
| --- | --- |
| Personnel record | Roster entry with employee ID (e.g. `INT-1.0`) |
| Job description | `prompts/intake.md`, used as the system prompt |
| Tools of the trade | `gather_evidence`: deterministic checks such as duplicate fingerprints and blank fields |
| Judgment | `simulate` (rules with a tunable error rate) or Claude in live mode |
| Company policy | `escalation_reason`: rules enforced in code, whatever the agent decides |
| Timesheet | `WorkLog`: every decision with reasoning, confidence, latency and tokens |
| Not yet hired | Planned agents in the roster refuse to start |

## Results (200 claims, seed 42, simulated mode)

| Agent | Processed | Escalated | Caught | False positives | False negatives |
| --- | --- | --- | --- | --- | --- |
| Intake Clerk (INT-1.0) | 200 | 8 | 8 of 8 duplicates | 0 | 0 |
| Claims Validator (VAL-1.0) | 192 | 24 | 24 of 24 missing-field claims | 0 | 0 |

With `--error-rate 0.1`, both agents raise false alarms (22 and 18), but still miss nothing, because the code guardrails escalate known duplicates and blank fields even when the agent decides wrongly.

## What this teaches

**Guardrails turn judgment errors into extra escalations instead of missed problems.** For checks with a clear rule (a duplicate fingerprint, a blank field), code backs up the agent, so mistakes cost the manager some time but never let a bad claim through. Later agents (clinical review, coding) make judgment calls that no simple rule can check, so that is where false negatives, and the manager's oversight, will really matter.

## Live mode

Live mode sends the job description as the system prompt and the claim plus tool evidence as the message, expects JSON back, retries once if the reply breaks the contract, then escalates. It is tested with a stand-in for Claude; to run it for real, set `ANTHROPIC_API_KEY` and run `python -m agents.run --mode live --count 20`.

## Next

Bolt 3: the Clinical Documentation Specialist and the Certified Medical Coder.
