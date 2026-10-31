const $ = (selector) => document.querySelector(selector);
const riskClass = (risk) => (risk || "unknown").toLowerCase();
let allItems = [];

async function getJson(url) {
  const response = await fetch(url, { headers: { Accept: "application/json" } });
  const body = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(body.detail || "The request could not be completed.");
  return body;
}

function renderSummary(summary) {
  $("#stat-total").textContent = summary.total;
  $("#stat-high").textContent = summary.high_risk;
  $("#stat-medium").textContent = summary.medium_risk;
  $("#stat-low").textContent = summary.low_risk;
  $("#donut-total").textContent = summary.total;
  $("#legend-high").textContent = summary.high_risk;
  $("#legend-medium").textContent = summary.medium_risk;
  $("#legend-low").textContent = summary.low_risk;
  $("#nav-count").textContent = String(summary.total).padStart(2, "0");
  const total = Math.max(summary.total, 1);
  const high = summary.high_risk / total * 360;
  const medium = summary.medium_risk / total * 360;
  $("#donut").style.background = `conic-gradient(#e96875 0deg ${high}deg,#edb75e ${high}deg ${high + medium}deg,#40bb91 ${high + medium}deg 360deg)`;
}

function safeText(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[char]);
}

function renderRows() {
  const search = $("#table-search").value.trim().toLowerCase();
  const kind = $("#type-filter").value;
  const filtered = allItems.filter((item) => (kind === "all" || item.type === kind) && `${item.value} ${item.category} ${item.risk}`.toLowerCase().includes(search));
  const tbody = $("#indicator-rows");
  if (!filtered.length) {
    tbody.innerHTML = '<tr><td colspan="6" class="empty-state">No indicators match your filters.</td></tr>';
  } else {
    tbody.innerHTML = filtered.map((item) => `<tr>
      <td><div class="indicator-cell"><span class="indicator-type-icon">${item.type === "ip" ? "⌘" : item.type === "domain" ? "◎" : "▧"}</span><span><span class="indicator-value">${safeText(item.value)}</span><span class="indicator-id">${safeText(item.id)}</span></span></div></td>
      <td><span class="type-pill">${safeText(item.type.toUpperCase())}</span></td>
      <td><span class="risk-text ${riskClass(item.risk)}">${safeText(item.risk)}</span></td>
      <td>${safeText(item.category)}</td><td>${safeText(item.last_seen)}</td>
      <td><button class="row-view" type="button" title="Check this indicator" aria-label="Check ${safeText(item.value)}" data-lookup="${safeText(item.value)}">↗</button></td>
    </tr>`).join("");
    tbody.querySelectorAll("[data-lookup]").forEach((button) => button.addEventListener("click", () => lookup(button.dataset.lookup)));
  }
  $("#table-count").textContent = `Showing ${filtered.length} of ${allItems.length} indicators`;
}

function showLookup(data) {
  const result = $("#lookup-result");
  const level = riskClass(data.risk);
  result.innerHTML = `<div class="result-head"><strong>${safeText(data.value)}</strong><span class="risk-pill ${level}">${safeText(data.risk)} risk</span></div><div>${safeText(data.summary)}</div><div class="result-meta">${safeText(data.type.toUpperCase())} · ${safeText(data.category)} · Confidence ${safeText(data.confidence)}% · ${safeText(data.source)}</div>`;
  result.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

async function lookup(value) {
  const input = $("#indicator-input");
  const button = $(".primary-button");
  input.value = value;
  button.disabled = true;
  button.querySelector("span:first-child").textContent = "Checking…";
  try {
    showLookup(await getJson(`/api/lookup?value=${encodeURIComponent(value)}`));
  } catch (error) {
    $("#lookup-result").innerHTML = `<span class="error-text">${safeText(error.message)}</span>`;
  } finally {
    button.disabled = false;
    button.querySelector("span:first-child").textContent = "Analyze indicator";
  }
}

async function init() {
  try {
    const [summary, listing] = await Promise.all([getJson("/api/summary"), getJson("/api/indicators")]);
    renderSummary(summary);
    allItems = listing.items;
    renderRows();
  } catch (error) {
    $("#indicator-rows").innerHTML = `<tr><td colspan="6" class="empty-state error-text">Could not load the local dataset: ${safeText(error.message)}</td></tr>`;
  }
}

$("#lookup-form").addEventListener("submit", (event) => {
  event.preventDefault();
  lookup($("#indicator-input").value.trim());
});
$("#clear-input").addEventListener("click", () => { $("#indicator-input").value = ""; $("#indicator-input").focus(); $("#lookup-result").replaceChildren(); });
document.querySelectorAll("[data-sample]").forEach((button) => button.addEventListener("click", () => lookup(button.dataset.sample)));
$("#table-search").addEventListener("input", renderRows);
$("#type-filter").addEventListener("change", renderRows);
$("#menu-toggle").addEventListener("click", () => $("#sidebar").classList.toggle("open"));
document.querySelectorAll(".nav-item").forEach((item) => item.addEventListener("click", () => $("#sidebar").classList.remove("open")));
init();
