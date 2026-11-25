# UX: Manager dashboard

The approved design for the manager's dashboard, built around the org chart analogy from [03-design.md](../aidlc/03-design.md): the agents are a team, and people manage them the way they manage any team.

> Static mockup with sample data. It shows the intended layout and wording, not working software.

## Files

| File | What it is |
| --- | --- |
| [`dashboard-mockup.html`](dashboard-mockup.html) | Clickable mockup of every screen. Download it next to `theme.css` and open it in a browser |
| [`theme.css`](theme.css) | The "Clinical chart" CSS theme: color tokens, light and dark mode, all components |

## Personas

A switch in the header changes who the dashboard is for. Each persona lands on its own page and sees only its tabs; the last choice is remembered.

| Persona | Lands on | Sees |
| --- | --- | --- |
| Executive | Executive summary | Executive summary, plans vs. actuals, 9-box, fix roadmap, before and after |
| Claims manager | Org chart | Every screen |
| Engineering lead | Fix roadmap | Fix roadmap, employee profile, plans vs. actuals, escalation inbox |

## Screens

| Screen | What happens there | People-management equivalent |
| --- | --- | --- |
| Executive summary | Headline sentence, six KPIs with weekly change, 8-week volume and quality chart, workforce health, projected savings, decisions needed; export to PDF or schedule a weekly email | Leadership report |
| Org chart | The team as ID badges: title, employee ID (version), key KPI, rating, open escalations | Walking the floor |
| Employee profile | Goals vs. actuals, false positives and negatives, skills by specialty, development plan, review history | Personnel file and annual review |
| 1:1s | The agent's own written update, progress, blockers, agenda, notes and action items | Weekly 1:1 |
| Plans vs. actuals | Quarterly plan, actual, variance and 8-week trend for each goal | Quarterly performance plan |
| 9-box | Each agent by performance and potential, with a recommended action | Talent review |
| Improvement plans | Reason, weekly checkpoints, support, temporary guardrails, outcomes | Performance improvement plan |
| Fix roadmap | Target deviations as GitHub issues, tabs per agent, timeline to fix | Tracking commitments |
| Escalation inbox | Decisions agents could not make, with their reasoning | Questions from the team |
| Before and after | Manual process vs. agent team on time, cost, error rate and where people spend their time | The value story |

## How the 9-box works for agents

| | Low performance | Moderate performance | High performance |
| --- | --- | --- | --- |
| **High potential** | Develop | Grow: harder cases | Promote: more autonomy |
| **Medium potential** | Improvement plan | Core contributor | Expand scope |
| **Low potential** | Replace version | Maintain | Trusted specialist |

Performance is this quarter's results against plan. Potential combines the eight-week accuracy trend, accuracy on hard cases, and how often the agent's escalations were truly needed.

## Visual system: "Clinical chart"

- **Chart-paper backdrop:** a faint teal grid, like medical chart paper, with a heartbeat line along the navigation bar. This is the one bold move; everything else stays quiet.
- **Midnight command bar** for the header and tabs, with the learn4free logo and the animated claims platform logo (a medical record worked on by agents).
- **Typefaces:** Bricolage Grotesque for headings and numbers, Public Sans for body text.

| Token | Light | Role |
| --- | --- | --- |
| `--nav` | `#0F2235` | Command bar |
| `--accent` | `#0E6E7E` | Clinical teal: brand, actions, the manager |
| `--paper` | `#EEF3F6` | Work surface |
| `--ex` | `#5A48C6` | Exceeds |
| `--ok` | `#1E8556` | Meets |
| `--watch` | `#A86400` | Watch |
| `--risk` | `#C0402E` | Below |

Performance colors are used only for performance against goals. Each agent also has an identity color, used only on its avatar: Intake blue, Validator steel cyan, Clinical teal, Coder plum, Pricing olive, Billing indigo.

## Illustrations and disclaimers

Every page opens with an illustration generated with AI (Claude), tagged "AI illustration". A footer on every page states that the illustrations were generated with AI for this prototype and do not show a real system, patient or insurer. Illustrations stay in banners so tables, charts and KPIs remain easy to read.

## Design principles

- **People language, not system language.** Agents have job titles, employee IDs, ratings, 1:1s and improvement plans.
- **People move up, not out.** The story is people moving from routine checks to judgment and oversight.
- **Reasoning before the decision.** Every escalation and 1:1 shows the agent's own account first.
- **Targets are visible.** Every KPI carries the plan the manager set.
- **Honest about the data.** Synthetic-data banner, labeled assumptions and AI disclaimers on every page.
