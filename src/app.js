const state = {
  data: null,
  stageId: null,
  featureId: null,
};

const money = new Intl.NumberFormat("en-US", { maximumFractionDigits: 1 });

function byId(id) {
  return document.getElementById(id);
}

function setText(id, value) {
  byId(id).textContent = value;
}

function activateTab(tabName) {
  document.querySelectorAll(".tab").forEach((button) => {
    button.classList.toggle("active", button.dataset.tab === tabName);
  });
  document.querySelectorAll(".surface").forEach((surface) => {
    surface.classList.toggle("active", surface.id === tabName);
  });
}

function renderSummary(data) {
  setText("northStar", data.summary.north_star);
  setText("topStage", data.summary.top_stage);
  setText("primaryMetric", data.summary.primary_metric);
  setText("topFeature", data.summary.top_feature);
}

function renderJourneyCards(data) {
  const container = byId("journeyCards");
  container.innerHTML = "";
  data.journey.forEach((stage) => {
    const button = document.createElement("button");
    button.className = "journey-button";
    button.type = "button";
    button.dataset.stageId = stage.stage_id;
    button.innerHTML = `
      <div class="journey-topline">
        <strong>${stage.stage}</strong>
        <span class="pill">${stage.priority_score}</span>
      </div>
      <div class="bar" aria-hidden="true"><span style="width:${Math.min(stage.priority_score, 100)}%"></span></div>
      <p>${stage.buyer_need}</p>
    `;
    button.addEventListener("click", () => selectStage(stage.stage_id));
    container.appendChild(button);
  });
}

function selectStage(stageId) {
  state.stageId = stageId;
  const stage = state.data.journey.find((item) => item.stage_id === stageId);
  document.querySelectorAll(".journey-button").forEach((button) => {
    button.classList.toggle("active", button.dataset.stageId === stageId);
  });
  setText("stageTitle", stage.stage);
  setText("stageSignal", stage.primary_signal);
  setText("stageSupport", `${stage.support_contacts_per_100} per 100`);
  setText("stageRisk", stage.sla_risk);
  setText("stageGap", stage.visibility_gap);
  setText("stageOpportunity", stage.prd_opportunity);
}

function renderFeatureList(data) {
  const container = byId("featureList");
  container.innerHTML = "";
  data.features.forEach((feature) => {
    const button = document.createElement("button");
    button.className = "feature-button";
    button.type = "button";
    button.dataset.featureId = feature.feature_id;
    button.innerHTML = `
      <div class="feature-topline">
        <strong>${feature.initiative}</strong>
        <span class="pill">${feature.rice_score}</span>
      </div>
      <p>${feature.metric}</p>
    `;
    button.addEventListener("click", () => selectFeature(feature.feature_id));
    container.appendChild(button);
  });
}

function selectFeature(featureId) {
  state.featureId = featureId;
  const feature = state.data.features.find((item) => item.feature_id === featureId);
  document.querySelectorAll(".feature-button").forEach((button) => {
    button.classList.toggle("active", button.dataset.featureId === featureId);
  });
  setText("featureTitle", feature.initiative);
  setText("featureProblem", feature.problem);
  setText("featureStory", feature.user_story);
  setText("featureCriteria", feature.acceptance_criteria);
  setText("featureScore", money.format(feature.rice_score));
  setText("featureDependency", feature.dependency);
  setText("featureMetric", feature.metric);
}

function renderExperiments(data) {
  const primary = data.experiments[0];
  byId("primaryExperiment").innerHTML = `
    <p class="label">Primary experiment</p>
    <h3>${primary.name}</h3>
    <p>${primary.hypothesis}</p>
    <div class="experiment-meta">
      <div><span>Population</span><strong>${primary.population}</strong></div>
      <div><span>Primary metric</span><strong>${primary.primary_metric}</strong></div>
      <div><span>Guardrail</span><strong>${primary.guardrail}</strong></div>
      <div><span>Ship decision</span><strong>${primary.ship_decision}</strong></div>
    </div>
  `;

  const workflowList = byId("workflowList");
  workflowList.innerHTML = "";
  data.workflows.forEach((workflow) => {
    const card = document.createElement("article");
    card.className = "workflow-card";
    card.innerHTML = `
      <h3>${workflow.trigger}</h3>
      <p><strong>System action:</strong> ${workflow.system_action}</p>
      <p><strong>Owner:</strong> ${workflow.human_owner}</p>
      <p><strong>Buyer output:</strong> ${workflow.buyer_output}</p>
    `;
    workflowList.appendChild(card);
  });
}

async function init() {
  const response = await fetch("data/artifact_data.json");
  state.data = await response.json();
  renderSummary(state.data);
  renderJourneyCards(state.data);
  renderFeatureList(state.data);
  renderExperiments(state.data);
  selectStage(state.data.journey[0].stage_id);
  selectFeature(state.data.features[0].feature_id);
  document.querySelectorAll(".tab").forEach((button) => {
    button.addEventListener("click", () => activateTab(button.dataset.tab));
  });
}

init();
