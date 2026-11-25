# Stage 2: Requirements

**Phase:** Inception
**Status:** Approved by the manager on 2026-11-24; additions from the UX review approved on 2026-11-24

## Intent and scope

The platform is a prototype claims pipeline run entirely by AI agents, built to show leaders what being a "manager of agents" means. The manager treats each agent like an employee: job description, goals, KPIs, quality audits, skills profile, yearly review and development plan.

- **In scope:** six worker agents, an orchestrator, a mock insurer, a manager dashboard with per-agent reviews, and a before-and-after comparison with the manual process.
- **Out of scope:** real patient data, real insurers, real billing rules, production security and compliance.
- **Lifecycle:** AI-DLC. Inception (Intake, Requirements), Construction (Dev, Build, Test), Operations (Deploy, Maintenance). AI proposes at each stage; the manager approves at each gate.
- **Framing:** people move up from routine checks to judgment and oversight. The platform does not present itself as replacing people.

## Synthetic data

All data is generated; no real patients, providers or insurers. Every record carries a hidden answer key (correct validity, codes and price) so agent accuracy can be measured exactly. Built in [Bolt 1](04-bolt-1-data-generator.md).

| Item | Requirement |
| --- | --- |
| Volume | 200 claims for the first test run |
| Record contents | Fake patient, provider, insurance member ID, visit date, free-text doctor's note |
| Clean records | About 70%: complete, clear notes, codes in the dictionary |
| Messy records | About 30%: missing fields, vague or contradictory notes, duplicates, unusual totals, codes absent from the dictionary |
| Specialties | 4: primary care, cardiology, orthopedics, dermatology |
| Code set | 40 ICD-10 diagnoses and 40 CPT procedures |
| Data dictionary | Internal fee schedule: one price per CPT code, plus modifier rules |
| Answer key | Hidden from agents; used only by the Test stage and scorecards |

## Agent job descriptions

Each agent has one job, a defined handoff, and a rule for when to stop and ask the manager.

| Agent | Job | Receives | Hands off | Escalates when |
| --- | --- | --- | --- | --- |
| Intake | Standardize incoming records | Raw synthetic record | Structured record | Unreadable or duplicate record |
| Validation | Confirm all claim-required fields exist | Structured record | Pass, or fail with reasons | Required data missing and not inferable |
| Clinical review | Extract diagnoses and procedures from the note | Validated record | Clinical summary | Note ambiguous or contradictory |
| Medical coding | Assign ICD-10 and CPT codes | Clinical summary | Codes, confidence score, justification | Confidence below the manager's threshold (0.85) |
| Pricing | Price each CPT code from the data dictionary | Coded claim | Priced line items and total | Code not in dictionary, or total over 3x the specialty average |
| Submission | Assemble the claim and send it to the mock insurer | Priced claim | Submission receipt | Insurer rejects the claim |

Every agent logs each decision with its reasoning, so the manager can audit any claim end to end.

## Goals and KPIs

- **False positive:** the agent flags a problem that isn't there (e.g. rejects a good record).
- **False negative:** the agent misses a real problem (e.g. passes a bad record). False negatives cost more because they become insurer denials.

| Agent | KPI | Target |
| --- | --- | --- |
| Intake | Parse success rate | 99% |
| Intake | Duplicates caught | 95% |
| Validation | False positive rate | Under 3% |
| Validation | False negative rate | Under 1% |
| Clinical review | Diagnoses and procedures correctly extracted | 95% |
| Medical coding | ICD-10 accuracy | 95% |
| Medical coding | CPT accuracy | 95% |
| Medical coding | Escalation rate | 5 to 10% |
| Pricing | Line items priced correctly | 99.5% |
| Submission | First-pass insurer acceptance | 90% |
| All agents | Average time per claim | Under 30 seconds |

- **Escalation rate** applies to every agent: near zero suggests overconfidence; very high means the agent saves no work.
- **Review rating:** Exceeds (all KPIs met, half beaten by 2+ points), Meets (all KPIs met), Watch (a KPI narrowly missed), Below (a KPI clearly missed).
- **Skills profile:** accuracy broken down by specialty, showing strengths and gaps.
- **Development plan:** the fixes proposed for any gap (better instructions, more dictionary entries, new tools, a stronger model).

## Supporting components

**Orchestrator.** Moves each claim through the six agents in order, tracks its status, retries on transient failures, and routes escalations to the manager's queue. A claim waiting on the manager pauses; the rest keep flowing.

**Mock insurer.** Accepts or denies submitted claims using simple rules (valid member ID, codes consistent with each other, price within the fee schedule). It returns a reason for every denial so denials trace back to the agent at fault.

## Manager dashboard

The approved layout is the mockup in [`ux/`](../ux/). Views:

| View | Purpose |
| --- | --- |
| Executive summary | One-minute report for leadership: headline, six KPIs with weekly change, 8-week volume and quality trend, workforce health, projected savings, decisions needed |
| Org chart | The team at a glance, each agent's health against goals |
| Employee profile | Goals vs. actuals, false positives and negatives, skills by specialty, development plan, review history |
| 1:1s | Weekly check-in: the agent's own update, blockers, notes, action items |
| Plans vs. actuals | Quarterly plan, actual, variance and trend per goal |
| 9-box | Performance vs. potential, with a recommended action per agent |
| Improvement plans | Time-boxed plan with checkpoints, support, guardrails and outcomes |
| Fix roadmap | GitHub issues for target deviations, filterable per agent, with a timeline |
| Escalation inbox | Decisions the agents could not make, with their reasoning |
| Before and after | Manual process vs. agent team on time, cost, error rate and where people spend their time |

Manager decisions in the inbox are recorded and count as feedback in each agent's review.

## Additions from the UX review

| Requirement | Detail |
| --- | --- |
| Persona views | Executive, Claims manager and Engineering lead; each sees its own landing page and tabs; last choice remembered |
| Executive report | Exportable as PDF and schedulable as a weekly email |
| Automatic GitHub issues | The orchestrator opens an issue when an agent misses a target for a full week, labels it by agent and severity, links related issues (e.g. "blocks #12"), and closes it when the target is met again |
| Branding | learn4free company logo and the animated claims platform logo |
| Visual theme | "Clinical chart" theme from `ux/theme.css`, light and dark mode |
| AI illustrations | One per page, each tagged "AI illustration", with a footer disclaimer that they were generated with AI and show no real system, patient or insurer |

## Before and after

The before-and-after view compares the current manual process with the agent team that people manage, for the same claims volume. Manual-process figures are illustrative assumptions, labeled as such in the app, and editable by the manager.

| Measure | Manual process (assumed) | With agents |
| --- | --- | --- |
| Time per claim | About 25 minutes end to end | Measured in test |
| Cost per claim | Assumed processing cost | Model usage cost |
| Error rate | Assumed 5% | Measured against answer key |
| Where people spend their time | Data entry, completeness checks, code lookups | Judgment calls, escalations, goals and performance reviews |

## Acceptance criteria

The finished prototype is accepted when:

- [ ] 200 synthetic claims run end to end without manual restarts
- [ ] At least one escalation per agent type appears in the inbox and can be resolved
- [ ] Every agent has a scorecard with goals, actuals, false positive and false negative rates, skills by specialty, rating and development plan
- [ ] Every insurer denial traces back to the responsible agent
- [ ] The before-and-after view compares the manual process with the agent team
- [ ] Each persona lands on its own view with the right tabs
- [ ] A target missed for a full week opens a GitHub issue automatically
- [ ] A first-time viewer understands "manager of agents" in a 10-minute demo

## Manager decisions (approved 2026-11-24)

- [x] Default KPI targets accepted
- [x] 0.85 coding confidence threshold accepted
- [x] Manual-process assumptions accepted (25 minutes, 5% error rate)
