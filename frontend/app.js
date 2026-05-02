// ============ CONFIG ============
const API_BASE = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
  ? "http://localhost:8000"
  : "/api";
let selectedFile = null;

// ============ INIT ============
document.addEventListener("DOMContentLoaded", () => {
  checkHealth();
  loadSampleReports();
  setupUpload();
  setupCharCount();
  setupNavLinks();
});

// ============ HEALTH CHECK ============
async function checkHealth() {
  const dot = document.getElementById("statusDot");
  const text = document.getElementById("statusText");
  try {
    const res = await fetch(`${API_BASE}/health`);
    if (res.ok) { dot.className = "status-dot online"; text.textContent = "API Online"; }
    else throw new Error();
  } catch { dot.className = "status-dot offline"; text.textContent = "API Offline"; }
}

// ============ TABS ============
function switchTab(tab) {
  document.getElementById("tabText").classList.toggle("active", tab === "text");
  document.getElementById("tabFile").classList.toggle("active", tab === "file");
  document.getElementById("textTab").classList.toggle("active", tab === "text");
  document.getElementById("fileTab").classList.toggle("active", tab === "file");
}

// ============ CHAR COUNT ============
function setupCharCount() {
  const ta = document.getElementById("reportText");
  const cc = document.getElementById("charCount");
  ta.addEventListener("input", () => { cc.textContent = ta.value.length; });
}

// ============ FILE UPLOAD ============
function setupUpload() {
  const zone = document.getElementById("uploadZone");
  const input = document.getElementById("fileInput");
  zone.addEventListener("click", () => input.click());
  zone.addEventListener("dragover", e => { e.preventDefault(); zone.classList.add("drag-over"); });
  zone.addEventListener("dragleave", () => zone.classList.remove("drag-over"));
  zone.addEventListener("drop", e => { e.preventDefault(); zone.classList.remove("drag-over"); if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]); });
  input.addEventListener("change", () => { if (input.files.length) handleFile(input.files[0]); });
}

function handleFile(file) {
  const valid = [".pdf", ".docx", ".doc", ".txt"];
  const ext = "." + file.name.split(".").pop().toLowerCase();
  if (!valid.includes(ext)) { alert("Unsupported format. Use PDF, DOCX, or TXT."); return; }
  selectedFile = file;
  document.getElementById("fileName").textContent = file.name;
  document.getElementById("fileSize").textContent = (file.size / 1024).toFixed(1) + " KB";
  document.getElementById("uploadZone").style.display = "none";
  document.getElementById("fileInfo").style.display = "block";
}

function removeFile() {
  selectedFile = null;
  document.getElementById("fileInput").value = "";
  document.getElementById("uploadZone").style.display = "block";
  document.getElementById("fileInfo").style.display = "none";
}

// ============ SAMPLE REPORTS ============
async function loadSampleReports() {
  const container = document.getElementById("sampleBtns");
  try {
    const res = await fetch(`${API_BASE}/sample-reports`);
    if (!res.ok) throw new Error();
    const data = await res.json();
    data.reports.forEach((r, i) => {
      const btn = document.createElement("button");
      btn.className = "sample-btn";
      btn.textContent = r.title;
      btn.onclick = () => { document.getElementById("reportText").value = r.text; document.getElementById("charCount").textContent = r.text.length; switchTab("text"); };
      container.appendChild(btn);
    });
  } catch {
    // Fallback samples
    ["Cardiology Report", "Emergency Discharge", "Oncology Note"].forEach(title => {
      const btn = document.createElement("button");
      btn.className = "sample-btn";
      btn.textContent = title;
      btn.onclick = () => alert("Start the backend server first: python app.py");
      container.appendChild(btn);
    });
  }
}

// ============ ANALYZE ============
async function analyzeReport() {
  const btn = document.getElementById("analyzeBtn");
  const btnContent = btn.querySelector(".btn-content");
  const btnLoader = btn.querySelector(".btn-loader");
  const textVal = document.getElementById("reportText").value.trim();
  const isFileMode = document.getElementById("tabFile").classList.contains("active");

  if (!isFileMode && !textVal) { alert("Please enter or paste a medical report."); return; }
  if (isFileMode && !selectedFile) { alert("Please upload a file first."); return; }

  // Show loading
  btn.disabled = true;
  btnContent.style.display = "none";
  btnLoader.style.display = "flex";
  document.getElementById("resultsPlaceholder").style.display = "none";
  document.getElementById("resultsContent").style.display = "none";

  try {
    const formData = new FormData();
    if (isFileMode && selectedFile) { formData.append("file", selectedFile); }
    else { formData.append("text", textVal); }
    formData.append("max_length", "250");
    formData.append("min_length", "50");

    const res = await fetch(`${API_BASE}/analyze`, { method: "POST", body: formData });
    if (!res.ok) { const err = await res.json(); throw new Error(err.detail || "Analysis failed"); }
    const data = await res.json();
    displayResults(data);
  } catch (err) {
    alert("Error: " + err.message);
    document.getElementById("resultsPlaceholder").style.display = "flex";
  } finally {
    btn.disabled = false;
    btnContent.style.display = "flex";
    btnLoader.style.display = "none";
  }
}

// ============ DISPLAY RESULTS ============
function displayResults(data) {
  document.getElementById("resultsContent").style.display = "flex";

  // Summary
  document.getElementById("summaryText").textContent = data.summary;
  document.getElementById("summaryModel").textContent = data.summary_model || "BART";
  document.getElementById("summaryMeta").textContent = `Input: ${data.input_length} chars → Summary: ${data.summary_length} chars | ${data.chunks_processed || 1} chunk(s) | ${data.processing_time}s`;

  // Entities
  const grid = document.getElementById("entitiesGrid");
  grid.innerHTML = "";
  const categories = [
    { key: "DISEASE", cls: "disease", icon: "🦠" },
    { key: "DRUG", cls: "drug", icon: "💊" },
    { key: "SYMPTOM", cls: "symptom", icon: "🩺" },
    { key: "TREATMENT", cls: "treatment", icon: "🏥" },
  ];
  categories.forEach(cat => {
    const items = (data.entities && data.entities[cat.key]) || [];
    const group = document.createElement("div");
    group.className = `entity-group ${cat.cls}`;
    group.innerHTML = `
      <div class="entity-label"><span class="entity-dot"></span>${cat.icon} ${cat.key} (${items.length})</div>
      <div class="entity-items">
        ${items.length ? items.slice(0, 15).map(e => `<span class="entity-tag">${escapeHtml(e)}</span>`).join("") : '<span class="entity-empty">None found</span>'}
      </div>
    `;
    grid.appendChild(group);
  });

  // ROUGE
  const rougeGrid = document.getElementById("rougeGrid");
  if (data.rouge_scores) {
    rougeGrid.innerHTML = "";
    [["rouge1", "ROUGE-1"], ["rouge2", "ROUGE-2"], ["rougeL", "ROUGE-L"]].forEach(([key, label]) => {
      const s = data.rouge_scores[key];
      const item = document.createElement("div");
      item.className = "rouge-item";
      item.innerHTML = `<span class="rouge-label">${label}</span><span class="rouge-value">${s.f1.toFixed(3)}</span><span class="rouge-sub">P: ${s.precision.toFixed(3)} | R: ${s.recall.toFixed(3)}</span>`;
      rougeGrid.appendChild(item);
    });
  } else { rougeGrid.innerHTML = '<div style="grid-column:1/-1;text-align:center;color:var(--text-muted);font-size:0.8rem;padding:12px;">ROUGE scores unavailable</div>'; }

  // Raw text
  document.getElementById("rawText").textContent = data.raw_text_snippet || data.raw_text?.substring(0, 500) || "";

  // Processing info
  document.getElementById("processingInfo").textContent = `Processed in ${data.processing_time}s | Model: ${data.summary_model} | Status: ${data.summary_status}`;

  // Scroll to results
  document.getElementById("resultsPanel").scrollIntoView({ behavior: "smooth", block: "start" });
}

function toggleRawText() {
  const el = document.getElementById("rawText");
  const label = document.getElementById("expandLabel");
  el.classList.toggle("collapsed");
  label.textContent = el.classList.contains("collapsed") ? "Show More" : "Show Less";
}

function escapeHtml(text) {
  const d = document.createElement("div"); d.textContent = text; return d.innerHTML;
}

// ============ NAV ============
function setupNavLinks() {
  document.querySelectorAll(".nav-link").forEach(link => {
    link.addEventListener("click", e => {
      document.querySelectorAll(".nav-link").forEach(l => l.classList.remove("active"));
      link.classList.add("active");
    });
  });
}
