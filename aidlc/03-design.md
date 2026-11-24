# Stage 3: Design (Dev, part 1)

**Phase:** Construction
**Status:** Proposed, awaiting manager approval

The platform is a Python backend where each worker agent is a Claude-powered component with a job description, typed inputs and outputs, and an escalation rule, plus a React dashboard for the manager. No code is written until this design is approved.

## Architecture

```
                 +---------------------------+
                 |  Manager dashboard (React) |
                 |  pipeline | inbox | scorecards | team view
                 +-------------+-------------+
                               | REST API
                 +-------------v-------------+
                 |   API server (FastAPI)    |
                 +-------------+-------------+
                               |
                 +-------------v-------------+
                 |      Orchestrator         |---- escalations ----> Manager inbox
                 +-------------+-------------+
                               |
  Intake -> Validation -> Clinical review -> Medical coding -> Pricing -> Submission
                               |                                            |
                 +-------------v-------------+                 +------------v-----------+
                 |  SQLite: claims, decisions, |                 |  Mock insurer service  |
                 |  escalations, scorecards    |                 +------------------------+
                 +-----------------------------+

  Synthetic data generator --> records + hidden answer key --> Test stage and scorecards
```

## Tech stack

| Layer | Choice | Why |
| --- | --- | --- |
| Language | Python 3.12 | Best AI and data tooling, easy for others to read |
| Agents | Anthropic Python SDK, one class per agent | Each agent's system prompt is its job description, readable by non-engineers |
| Models | Configurable per agent; default `claude-haiku-5-5` for intake and validation, `claude-sonnet-5-5` for clinical review and coding | Cheaper model for simple jobs, stronger model where judgment matters ([model docs](https://docs.claude.com/en/docs/about-claude/models/overview)) |
| Structured output | Pydantic schemas for every handoff | Handoffs are contracts; bad output is caught, not passed on |
| API | FastAPI | Simple, typed, auto-generated API docs |
| Storage | SQLite | Zero setup; enough for a prototype |
| Dashboard | React + Vite + Tailwind | Fast to build, easy to demo |
| Tests | pytest | Standard |
| Packaging | Docker Compose | One command to run everything |

## Agent design

Every agent follows the same contract, mirroring an employee role:

| Element | Implementation |
| --- | --- |
| Job description | System prompt in `agents/prompts/<agent>.md` |
| Input and output | Pydantic models in `agents/schemas.py` |
| Escalation rule | Code check after each decision (e.g. coding confidence below 0.85) |
| Decision log | Every decision saved with reasoning, model, latency and cost |
| Tools | Read-only lookups only: code set for coding, fee schedule for pricing |

## Two run modes

- **Live mode:** agents call Claude. Used for the real demo and the Test stage.
- **Simulated mode:** agents return scripted results with tunable error rates, no API key needed. Used for unit tests, offline demos, and showing how a scorecard reacts when an agent underperforms.

## Data model

| Table | Holds |
| --- | --- |
| `claims` | Each claim and its current stage and status |
| `decisions` | One row per agent decision: input, output, reasoning, confidence, latency, cost |
| `escalations` | Items sent to the manager, and the manager's decision |
| `answer_key` | Correct validity, codes and price per claim; never visible to agents |
| `code_set` | About 40 ICD-10 and 40 CPT codes in use |
| `fee_schedule` | Internal price per CPT code, plus modifier rules |
| `insurer_responses` | Accept or deny, with reason and blamed agent |
| `goals` | KPI targets per agent, editable by the manager |

Scorecards are computed from `decisions`, `escalations` and `answer_key`, so they always reflect real results.

## Repository layout

```
aidlc/            Approved AI-DLC artifacts
agents/           Six worker agents, prompts, schemas
orchestrator/     Pipeline runner and escalation routing
insurer/          Mock insurer rules
data/             Synthetic data generator, code set, fee schedule
scoring/          KPI and scorecard calculations
api/              FastAPI server
dashboard/        React manager dashboard
tests/            pytest suites
```

## Build plan (bolts)

AI-DLC works in short cycles called bolts. Each ends with a commit and a working, testable piece.

1. Synthetic data generator, code set, fee schedule and answer key
2. Agent framework, plus intake and validation agents
3. Clinical review and medical coding agents
4. Pricing and submission agents, plus the mock insurer
5. Orchestrator and escalation inbox
6. Scoring engine and scorecards
7. Manager dashboard

## Risks

| Risk | Mitigation |
| --- | --- |
| Model output drifts from schema | Pydantic validation with one automatic retry, then escalate |
| API cost during repeated tests | Simulated mode for most tests; live runs capped at 200 claims |
| Synthetic notes too easy, inflating accuracy | Generator includes vague, contradictory and unusual notes at about 30% |
| Viewers mistake it for a real billing system | "Synthetic data, prototype only" banner on every dashboard page |

## Decisions for the manager

- [ ] Approve the tech stack (Python, FastAPI, SQLite, React)
- [ ] Approve per-agent model defaults
- [ ] Approve the two run modes
- [ ] Approve the seven-bolt build plan
