# UX: Manager dashboard

Design templates for the manager's dashboard, built around the org chart analogy from [03-design.md](../aidlc/03-design.md): the agents are a team, and you manage them the way you manage people.

> These are static mockups with sample data. They show the intended layout and wording, not working software.

## How to view

GitHub shows HTML as source code. To see the mockup, download [`dashboard-mockup.html`](dashboard-mockup.html) and open it in a browser.

## Screens

| Screen | What the manager does there | People-management equivalent |
| --- | --- | --- |
| Org chart (home) | Sees the whole team: each agent as an ID badge with title, employee ID (version), key KPI, rating and open escalations | Walking the floor |
| Employee profile | Reads one agent's goals vs. actuals, false positives and false negatives, skills by specialty, development plan and review history; signs off reviews | Personnel file and annual review |
| 1:1s | Runs a weekly 1:1: the agent's own written update, progress since last time, blockers, agenda, notes and action items with owners and due dates | Weekly 1:1 |
| Plans vs. actuals | Compares each agent's quarterly plan with actual results, with variance and an eight-week trend | Quarterly performance plan |
| 9-box | Places every agent by performance (results vs. plan) and potential (readiness for more autonomy), with a recommended action per agent | Talent review / calibration |
| Improvement plans | Tracks a time-boxed plan for an underperforming agent: reason, weekly checkpoints, support given, temporary guardrails and possible outcomes | Performance improvement plan (PIP) |
| Escalation inbox | Decides on items agents could not resolve, with the agent's reasoning shown | Questions from the team |
| Team vs. human baseline | Compares the agent team with an assumed human team on time, cost, error rate and manager hours | The executive story |

The profile mockup shows the Certified Medical Coder; the 1:1 and improvement plan show the Billing Specialist.

## How the 9-box works for agents

| | Low performance | Moderate performance | High performance |
| --- | --- | --- | --- |
| **High potential** | Develop | Grow: harder cases | Promote: more autonomy |
| **Medium potential** | Improvement plan | Core contributor | Expand scope |
| **Low potential** | Replace version | Maintain | Trusted specialist |

- **Performance** is this quarter's results against the manager's plan.
- **Potential** combines the eight-week accuracy trend, accuracy on hard cases, and how often the agent's escalations were truly needed.
- **Promotion** for an agent means more autonomy, such as a lower escalation threshold. **Replacement** means retiring a version and deploying a better one.

## Design principles

- **People language, not system language.** Agents have job titles, employee IDs, ratings, 1:1s and improvement plans.
- **Status color means performance against goals.** Green meets, amber is on watch, red is below target, blue exceeds. Nothing else uses those colors.
- **Reasoning before the decision.** Every escalation and 1:1 shows the agent's own account first.
- **Targets are visible.** Every KPI carries the plan the manager set.
- **Honest about the data.** A banner on every screen says the prototype uses synthetic data, and baseline figures are labeled as assumptions.

## Visual system

| Token | Light | Use |
| --- | --- | --- |
| Paper | `#F3F6F5` | Page background |
| Ink | `#1B2A3A` | Text |
| Accent | `#2F5D8A` | Navigation, you, primary actions, "Exceeds" |
| Meets | `#2E7D5B` | On target |
| Watch | `#9A6412` | Close to missing a target |
| Below | `#B3403A` | Target missed |

Typeface: Public Sans, with tabular numbers so KPIs line up. Dark mode is supported.
