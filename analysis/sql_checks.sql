-- Journey priority review
select
  stage,
  priority_score,
  support_contacts_per_100,
  sla_risk,
  visibility_gap
from journey_health
order by priority_score desc;

-- Roadmap candidate ranking
select
  initiative,
  rice_score,
  metric,
  dependency
from feature_backlog
order by rice_score desc;

-- Experiment guardrail review
select
  name,
  primary_metric,
  guardrail,
  ship_decision
from experiment_plan;
