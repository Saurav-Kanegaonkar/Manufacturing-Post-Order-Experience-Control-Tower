import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ANALYSIS = ROOT / "analysis"
OUTPUTS = ANALYSIS / "outputs"


JOURNEY_STAGES = [
    {
        "stage_id": "J01",
        "stage": "Order confirmation",
        "buyer_need": "Know the order was accepted, reviewed, and ready for supplier kickoff.",
        "pain_score": 58,
        "support_contacts_per_100": 9.4,
        "sla_risk": 26,
        "visibility_gap": 39,
        "csat_delta": -4.2,
        "primary_signal": "Buyers ask whether the order is truly in motion after checkout.",
        "prd_opportunity": "Add a confirmation panel that separates payment received, manufacturability review, and supplier assignment.",
    },
    {
        "stage_id": "J02",
        "stage": "Supplier kickoff",
        "buyer_need": "See that a matched supplier has accepted the work and understands key requirements.",
        "pain_score": 66,
        "support_contacts_per_100": 12.8,
        "sla_risk": 38,
        "visibility_gap": 54,
        "csat_delta": -6.6,
        "primary_signal": "The handoff from marketplace order to manufacturing work is opaque.",
        "prd_opportunity": "Expose a supplier kickoff milestone with requirement acknowledgement and owner timestamp.",
    },
    {
        "stage_id": "J03",
        "stage": "Production progress",
        "buyer_need": "Understand whether parts are actively being produced and what changed since the last visit.",
        "pain_score": 71,
        "support_contacts_per_100": 16.1,
        "sla_risk": 43,
        "visibility_gap": 61,
        "csat_delta": -8.7,
        "primary_signal": "Static status labels do not explain whether a custom job is progressing.",
        "prd_opportunity": "Replace static status copy with line-item milestones, last update freshness, and next expected update.",
    },
    {
        "stage_id": "J04",
        "stage": "Delay notification",
        "buyer_need": "Learn about schedule risk early enough to adjust downstream plans.",
        "pain_score": 87,
        "support_contacts_per_100": 24.9,
        "sla_risk": 72,
        "visibility_gap": 76,
        "csat_delta": -15.3,
        "primary_signal": "Late delay disclosure creates avoidable tickets and buyer distrust.",
        "prd_opportunity": "Launch proactive delay alerts with reason codes, revised ETA, confidence, and next action.",
    },
    {
        "stage_id": "J05",
        "stage": "Shipment tracking",
        "buyer_need": "Track packages, partial shipments, packing documents, and expected delivery in one place.",
        "pain_score": 63,
        "support_contacts_per_100": 13.7,
        "sla_risk": 34,
        "visibility_gap": 49,
        "csat_delta": -5.9,
        "primary_signal": "Shipment data exists, but line-item and package-level views are fragmented.",
        "prd_opportunity": "Unify line-item shipment tracking, package status, downloadable packing lists, and delivery exceptions.",
    },
    {
        "stage_id": "J06",
        "stage": "Support resolution",
        "buyer_need": "Resolve an exception without repeating context across support, operations, and supplier teams.",
        "pain_score": 79,
        "support_contacts_per_100": 21.6,
        "sla_risk": 55,
        "visibility_gap": 68,
        "csat_delta": -11.8,
        "primary_signal": "Support workflows lack a clear path from ticket intake to accountable resolution.",
        "prd_opportunity": "Create an exception workspace that links order context, owner, SLA timer, and buyer-facing status copy.",
    },
]


FEATURES = [
    {
        "feature_id": "F01",
        "initiative": "Proactive delay promise center",
        "problem": "Buyers learn about custom manufacturing delays too late to adjust their own production plans.",
        "user_story": "As a buyer, I want delay reasons, revised ETA, and next update timing so I can reset internal expectations.",
        "reach": 82,
        "impact": 9.2,
        "confidence": 84,
        "effort": 8,
        "dependency": "Supplier reason-code capture and ETA confidence service",
        "acceptance_criteria": "Delay alert fires before SLA breach, includes reason code, revised ETA, confidence band, and next update owner.",
        "metric": "Delay-contact rate per 100 affected orders",
    },
    {
        "feature_id": "F02",
        "initiative": "Line-item milestone timeline",
        "problem": "A single order status hides what is happening across custom parts, partial shipments, and production steps.",
        "user_story": "As a procurement lead, I want each line item to show current milestone and next expected update.",
        "reach": 76,
        "impact": 8.1,
        "confidence": 78,
        "effort": 10,
        "dependency": "Event normalization across supplier updates, QA checkpoints, and shipping events",
        "acceptance_criteria": "Each line item shows current milestone, last update age, next step, and exception state.",
        "metric": "Order status page return rate after support contact",
    },
    {
        "feature_id": "F03",
        "initiative": "Exception ownership workspace",
        "problem": "Support, operations, and supplier teams need one record of what changed and who owns the next action.",
        "user_story": "As a support agent, I want order context and owner routing so I can resolve exceptions without manual investigation.",
        "reach": 54,
        "impact": 8.7,
        "confidence": 72,
        "effort": 12,
        "dependency": "Support ticket integration and escalation taxonomy",
        "acceptance_criteria": "Every exception has owner, SLA timer, root cause, customer-safe update copy, and next action.",
        "metric": "Median exception resolution time",
    },
    {
        "feature_id": "F04",
        "initiative": "Buyer-facing update digest",
        "problem": "Buyers with many active orders cannot quickly see which orders changed since the prior visit.",
        "user_story": "As a program manager, I want a digest of changed orders so I can focus on risk instead of checking every order.",
        "reach": 61,
        "impact": 6.4,
        "confidence": 74,
        "effort": 8,
        "dependency": "Notification preferences and account-level order grouping",
        "acceptance_criteria": "Digest summarizes changed milestones, delayed orders, shipped line items, and unresolved support items.",
        "metric": "Weekly active buyer return rate",
    },
    {
        "feature_id": "F05",
        "initiative": "Support reason-code instrumentation",
        "problem": "Roadmap decisions are weakened when support tickets lack consistent post-order reasons.",
        "user_story": "As a PM, I want support contacts tagged to journey moments so I can prioritize product fixes.",
        "reach": 68,
        "impact": 6.9,
        "confidence": 81,
        "effort": 6,
        "dependency": "Support taxonomy, agent workflow changes, and QA sampling",
        "acceptance_criteria": "At least 90 percent of post-order tickets contain journey stage, reason code, and resolution path.",
        "metric": "Tagged ticket completeness",
    },
    {
        "feature_id": "F06",
        "initiative": "Shipment document hub",
        "problem": "Packing lists, tracking numbers, and partial shipment details are hard to inspect together.",
        "user_story": "As a buyer, I want shipping documents and tracking grouped by line item and package.",
        "reach": 46,
        "impact": 5.8,
        "confidence": 76,
        "effort": 7,
        "dependency": "Carrier tracking links and document availability service",
        "acceptance_criteria": "Buyer can access package tracking, packing list, carrier, shipped items, and exception state in one view.",
        "metric": "Shipment-related support contacts",
    },
]


EXPERIMENTS = [
    {
        "experiment_id": "E01",
        "name": "Early delay alert",
        "hypothesis": "Sending a delay alert with reason, revised ETA, and next update timing will reduce delay-related support contacts.",
        "population": "Orders with projected SLA risk above 50 and no shipment scan.",
        "primary_metric": "Delay support contacts per 100 affected orders",
        "guardrail": "No increase in cancellation rate or negative CSAT comments about alert quality.",
        "duration_days": 28,
        "ship_decision": "Ship if contact rate drops by at least 12 percent and guardrails remain flat.",
    },
    {
        "experiment_id": "E02",
        "name": "Line-item milestone clarity",
        "hypothesis": "Showing current milestone and next expected update will lower repeated order-status page visits after a ticket.",
        "population": "Orders with three or more line items and active production status.",
        "primary_metric": "Repeat status-check tickets within seven days",
        "guardrail": "No drop in order status page comprehension survey.",
        "duration_days": 21,
        "ship_decision": "Ship if repeat tickets fall by 10 percent with no comprehension decline.",
    },
    {
        "experiment_id": "E03",
        "name": "Exception ownership routing",
        "hypothesis": "Routing exceptions to an accountable owner with buyer-safe update copy will shorten resolution time.",
        "population": "Support tickets tagged delay, quality question, supplier handoff, or shipment exception.",
        "primary_metric": "Median exception resolution hours",
        "guardrail": "No increase in agent handle time beyond 8 percent.",
        "duration_days": 35,
        "ship_decision": "Ship if resolution time improves by 15 percent and handle time remains within guardrail.",
    },
]


WORKFLOWS = [
    {
        "trigger": "SLA risk rises above 50",
        "system_action": "Create delay-alert candidate and request supplier reason code",
        "human_owner": "Operations lead",
        "buyer_output": "Revised ETA, reason, confidence, and next update window",
    },
    {
        "trigger": "No supplier update for 72 hours during production",
        "system_action": "Flag stale milestone and route to supplier manager",
        "human_owner": "Supplier manager",
        "buyer_output": "Freshness indicator and next expected update",
    },
    {
        "trigger": "Support ticket repeats within seven days",
        "system_action": "Attach order timeline, prior messages, and recommended owner",
        "human_owner": "Support lead",
        "buyer_output": "Single case status with accountable next action",
    },
    {
        "trigger": "Shipment scan mismatch or partial shipment",
        "system_action": "Group carrier events by line item and document availability",
        "human_owner": "Logistics coordinator",
        "buyer_output": "Package-level timeline and downloadable documents",
    },
]


RESEARCH_NOTES = [
    {
        "theme": "Post-order trust",
        "insight": "The buyer need is confidence that custom work is progressing, not only a status label.",
        "evidence_type": "Role requirement and public product support pattern",
    },
    {
        "theme": "Marketplace coordination",
        "insight": "The hardest moments occur at handoffs between buyer, supplier, operations, logistics, and support.",
        "evidence_type": "Marketplace workflow structure",
    },
    {
        "theme": "Product instrumentation",
        "insight": "A PM needs support reasons, SLA risk, and milestone freshness tied to order journey moments.",
        "evidence_type": "Roadmap and experimentation requirement",
    },
]


def score_stage(stage):
    return round(
        stage["pain_score"] * 0.32
        + stage["support_contacts_per_100"] * 1.2
        + stage["sla_risk"] * 0.24
        + stage["visibility_gap"] * 0.22
        + abs(stage["csat_delta"]) * 1.7,
        1,
    )


def score_feature(feature):
    return round((feature["reach"] * feature["impact"] * feature["confidence"]) / (feature["effort"] * 100), 1)


def write_csv(path, rows, fieldnames):
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    DATA.mkdir(exist_ok=True)
    OUTPUTS.mkdir(parents=True, exist_ok=True)

    stages = []
    for stage in JOURNEY_STAGES:
        row = dict(stage)
        row["priority_score"] = score_stage(stage)
        stages.append(row)

    features = []
    for feature in FEATURES:
        row = dict(feature)
        row["rice_score"] = score_feature(feature)
        features.append(row)

    stages.sort(key=lambda row: row["priority_score"], reverse=True)
    features.sort(key=lambda row: row["rice_score"], reverse=True)

    write_csv(DATA / "journey_health.csv", stages, list(stages[0].keys()))
    write_csv(DATA / "feature_backlog.csv", features, list(features[0].keys()))
    write_csv(DATA / "experiment_plan.csv", EXPERIMENTS, list(EXPERIMENTS[0].keys()))
    write_csv(DATA / "support_workflows.csv", WORKFLOWS, list(WORKFLOWS[0].keys()))
    write_csv(DATA / "research_notes.csv", RESEARCH_NOTES, list(RESEARCH_NOTES[0].keys()))
    write_csv(OUTPUTS / "priority_queue.csv", stages, list(stages[0].keys()))

    artifact = {
        "summary": {
            "title": "Post-Order Experience PRD Studio",
            "domain": "Custom manufacturing marketplace",
            "top_stage": stages[0]["stage"],
            "top_feature": features[0]["initiative"],
            "north_star": "Buyer confidence after checkout",
            "primary_metric": "Post-order support contacts per 100 active orders",
        },
        "journey": stages,
        "features": features,
        "experiments": EXPERIMENTS,
        "workflows": WORKFLOWS,
        "researchNotes": RESEARCH_NOTES,
    }

    (DATA / "artifact_data.json").write_text(json.dumps(artifact, indent=2) + "\n")

    (ANALYSIS / "executive_findings.md").write_text(
        "# Executive Findings\n\n"
        "## What I Analyzed\n\n"
        "I modeled the post-order journey for a custom manufacturing marketplace across six buyer moments: "
        "order confirmation, supplier kickoff, production progress, delay notification, shipment tracking, "
        "and support resolution. The output is a PRD-oriented prioritization artifact rather than a generic dashboard.\n\n"
        "## Findings\n\n"
        f"- Highest-priority journey moment: {stages[0]['stage']} with a priority score of {stages[0]['priority_score']}.\n"
        f"- Highest-ranked initiative: {features[0]['initiative']} with a RICE-style score of {features[0]['rice_score']}.\n"
        "- The strongest product opportunity is proactive communication before a buyer has to open a support ticket.\n"
        "- The operating workflow should connect supplier reason codes, SLA risk, support routing, and buyer-facing status copy.\n\n"
        "## Recommendation\n\n"
        "Start with proactive delay communication and line-item milestone clarity, then instrument support reason codes so future roadmap decisions are grounded in tagged buyer pain.\n"
    )

    (ANALYSIS / "analysis_plan.md").write_text(
        "# Analysis Plan\n\n"
        "1. Map the buyer journey after checkout into distinct moments where trust can rise or fall.\n"
        "2. Score each moment using buyer pain, support load, SLA risk, visibility gap, and CSAT-style sentiment change.\n"
        "3. Convert the highest-risk moments into PRD-ready initiatives with user stories, dependencies, acceptance criteria, and metrics.\n"
        "4. Define experiments that test proactive communication, milestone clarity, and support ownership before broad rollout.\n"
    )

    (ANALYSIS / "prd_brief.md").write_text(
        "# PRD Brief\n\n"
        "## Problem\n\n"
        "Custom manufacturing buyers need confidence after checkout, especially when supplier handoffs, production steps, delays, partial shipments, or support exceptions make the order feel opaque.\n\n"
        "## Proposed Product Bet\n\n"
        "Create a post-order experience layer that combines line-item milestones, proactive delay alerts, and exception ownership so buyers can understand what changed, what happens next, and who owns resolution.\n\n"
        "## Non Goals\n\n"
        "- This artifact does not model real company performance.\n"
        "- This artifact does not prescribe supplier-side compensation or pricing logic.\n"
        "- This artifact does not replace qualitative buyer research.\n"
    )

    (ANALYSIS / "experiment_plan.md").write_text(
        "# Experiment Plan\n\n"
        "## Primary Experiment\n\n"
        "Test whether an early delay alert that includes reason, revised ETA, confidence, and next update timing reduces delay-related support contacts.\n\n"
        "## Success Metric\n\n"
        "Delay support contacts per 100 affected orders.\n\n"
        "## Guardrails\n\n"
        "- Cancellation rate does not increase.\n"
        "- Negative CSAT comments about alert quality do not increase.\n"
        "- Support agent handle time remains within tolerance.\n"
    )

    print(f"Wrote {len(stages)} journey rows, {len(features)} feature rows, {len(EXPERIMENTS)} experiments, and {len(WORKFLOWS)} workflows.")
    print(f"Top journey: {stages[0]['stage']} ({stages[0]['priority_score']})")
    print(f"Top feature: {features[0]['initiative']} ({features[0]['rice_score']})")


if __name__ == "__main__":
    main()
