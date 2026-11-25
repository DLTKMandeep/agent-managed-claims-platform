# UX: Manager dashboard

Design templates for the manager's dashboard, built around the org chart analogy from [03-design.md](../aidlc/03-design.md): the agents are a team, and you manage them the way you manage people.

> These are static mockups with sample data. They show the intended layout and wording, not working software.

## How to view

GitHub shows HTML as source code. To see the mockup, download [`dashboard-mockup.html`](dashboard-mockup.html) and open it in a browser, or use GitHub's raw view with a local file.

## Screens

| Screen | What the manager does there | Maps to |
| --- | --- | --- |
| Org chart (home) | Sees the whole team at a glance: each agent as an ID badge with title, employee ID (version), key KPI, rating and open escalations | Daily check of team health |
| Employee profile | Reads one agent's goals vs. actuals, false positives and false negatives, skills by specialty, development plan and review history; signs off reviews | Weekly 1:1 and annual review |
| Escalation inbox | Decides on items agents could not resolve, with the agent's reasoning shown | Daily check-ins |
| Team vs. human baseline | Compares the agent team with an assumed human team on time, cost, error rate and manager hours | The executive story |

The profile mockup shows the Certified Medical Coder; every badge on the org chart links to it.

## Design principles

- **People language, not system language.** Agents have job titles, employee IDs and ratings. The screens say "Reports to Operations Supervisor," not "pipeline stage 4."
- **Status color means performance against goals.** Green meets, amber is on watch, red is below target, blue exceeds. Nothing else uses those colors.
- **Reasoning before the decision.** Every escalation shows why the agent stopped, so the manager can decide in seconds.
- **Targets are visible.** Every KPI bar carries a mark for the target the manager set.
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
