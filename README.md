# Agent-Managed Claims Platform

A prototype medical claims pipeline run entirely by AI agents, built to show what it means to be a **manager of agents**.

Each agent is treated like an employee: it has a job description, yearly goals, KPIs, quality audits, a skills profile, a performance review and a development plan. The human manager sets goals and guardrails, handles escalations, and reviews performance.

> **Synthetic data only.** No real patients, providers, insurers or billing rules are used anywhere in this project.

## The pipeline

```
Manager (human)
   |
Orchestrator agent
   |
Intake -> Validation -> Clinical review -> Medical coding -> Pricing -> Submission -> Mock insurer
```

| Agent | Job |
| --- | --- |
| Intake | Standardize incoming records |
| Validation | Confirm all claim-required fields exist |
| Clinical review | Extract diagnoses and procedures from the doctor's note |
| Medical coding | Assign ICD-10 and CPT codes |
| Pricing | Price each procedure from the internal data dictionary |
| Submission | Assemble the claim and send it to the mock insurer |

## How it is built: AI-DLC

The project follows the AI-Driven Development Lifecycle. AI proposes the work at each stage; the manager approves at each gate. Every stage's approved artifact lives in [`aidlc/`](aidlc/).

| Phase | Stage | Status | Artifact |
| --- | --- | --- | --- |
| Inception | Intake | Approved 2026-11-24 | [01-intake-intent.md](aidlc/01-intake-intent.md) |
| Inception | Requirements | Approved 2026-11-24 | [02-requirements.md](aidlc/02-requirements.md) |
| Construction | Dev: design | Awaiting approval | [03-design.md](aidlc/03-design.md) |
| Construction | Dev: code | Not started | |
| Construction | Build | Not started | |
| Construction | Test | Not started | |
| Operations | Deploy | Not started | |
| Operations | Maintenance | Not started | |

## Repository layout

```
aidlc/        Approved artifacts for each AI-DLC stage
```

Code folders are added once the design is approved.
