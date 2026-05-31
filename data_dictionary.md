# Data Dictionary

| Table | Grain | Purpose |
|---|---|---|
| `journey_health.csv` | Post-order journey stage | Scores buyer pain, support load, SLA risk, visibility gap, and CSAT-style sentiment change. |
| `feature_backlog.csv` | Product initiative | Converts journey pain into PRD-ready roadmap candidates with user stories and RICE-style scoring. |
| `experiment_plan.csv` | Product experiment | Defines hypotheses, target populations, metrics, guardrails, durations, and ship decisions. |
| `support_workflows.csv` | Workflow trigger | Maps operational triggers to system actions, human owners, and buyer-facing outputs. |
| `research_notes.csv` | Research theme | Summarizes the synthesized themes that anchor product decisions. |
| `artifact_data.json` | App data bundle | Normalized JSON used by the static browser app. |

## Key Fields

| Field | Meaning |
|---|---|
| `priority_score` | Weighted stage score using pain, support contacts, SLA risk, visibility gap, and sentiment change. |
| `support_contacts_per_100` | Synthetic rate of post-order support contacts per 100 active orders. |
| `sla_risk` | Synthetic 0 to 100 estimate of risk that a stage will breach promised timing or transparency expectations. |
| `visibility_gap` | Synthetic 0 to 100 estimate of how unclear the journey moment feels to a buyer. |
| `rice_score` | Reach times impact times confidence divided by effort, used to rank roadmap candidates. |
