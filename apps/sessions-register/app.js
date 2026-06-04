const SESSIONS_JSON = "../../exports/generated/sessions.json";
const SESSIONS_CSV = "../../exports/generated/sessions.csv";

const TYPE_ORDER = ["rehearsal", "demo", "studio", "radio", "television"];
const TYPE_LABELS = {
  rehearsal: "Répétitions",
  demo: "Démos",
  studio: "Sessions studio",
  radio: "Sessions radio",
  television: "Sessions télévision",
};

const STATUS_LABELS = {
  etabli: "établi",
  probable: "probable",
  conteste: "contesté",
};

const MONTHS = [
  "",
  "janvier",
  "février",
  "mars",
  "avril",
  "mai",
  "juin",
  "juillet",
  "août",
  "septembre",
  "octobre",
  "novembre",
  "décembre",
];

const state = {
  sessions: [],
  filters: {
    query: "",
    type: "",
    status: "",
    place: "",
  },
};

const els = {
  search: document.getElementById("search"),
  type: document.getElementById("type-filter"),
  status: document.getElementById("status-filter"),
  place: document.getElementById("place-filter"),
  reset: document.getElementById("reset-filters"),
  download: document.getElementById("download-csv"),
  meta: document.getElementById("results-meta"),
  statusText: document.getElementById("sessions-status"),
  sections: document.getElementById("sessions-sections"),
};

init().catch((error) => {
  console.error(error);
  els.statusText.textContent = "Impossible de charger le registre sessions.";
});

async function init() {
  const response = await fetch(new URL(SESSIONS_JSON, window.location.href), { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Chargement impossible: ${response.status}`);
  }
  const records = await response.json();
  state.sessions = records.map(normalizeRecord).sort(compareSessions);
  populateFilters();
  bindEvents();
  render();
  focusHashTarget();
}

function normalizeRecord(record) {
  const data = record.data || record;
  const placeLabel = data.lieu || data.studio || data.place_id || "Lieu non renseigné";
  const searchText = [
    data.id,
    data.label,
    data.date,
    data.type_session,
    data.studio,
    data.lieu,
    data.place_id,
    data.ville,
    data.ere,
    data.producteur,
    data.ingenieur_son,
    data.statut_documentaire,
    data.notes,
    data.source,
    ...(data.sources || []),
    ...(data.urls || []),
    ...(data.participants || []),
    ...(data.titres || []),
    ...relationValues(data.relations),
  ].filter(Boolean).join(" ").toLowerCase();

  return {
    ...data,
    place_label: placeLabel,
    search_text: searchText,
  };
}

function relationValues(relations) {
  if (!relations || typeof relations !== "object") return [];
  return Object.values(relations).flatMap((value) => Array.isArray(value) ? value : [value]);
}

function compareSessions(a, b) {
  const dateA = sortableDate(a.date);
  const dateB = sortableDate(b.date);
  if (dateA !== dateB) return dateA.localeCompare(dateB);
  return String(a.numero || "").localeCompare(String(b.numero || ""), "fr", { numeric: true });
}

function sortableDate(value) {
  return String(value || "9999-99-99").replaceAll("-00", "-99");
}

function populateFilters() {
  fillSelect(
    els.type,
    unique(state.sessions.map((session) => session.type_session)).sort(byTypeOrder),
    (type) => TYPE_LABELS[type] || type
  );
  fillSelect(
    els.status,
    unique(state.sessions.map((session) => session.statut_documentaire)).sort(),
    (status) => STATUS_LABELS[status] || status
  );
  fillSelect(
    els.place,
    unique(state.sessions.map((session) => session.place_label)).sort((a, b) => a.localeCompare(b, "fr")),
    (place) => place
  );
}

function fillSelect(select, values, labelFor) {
  values.filter(Boolean).forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = labelFor(value);
    select.appendChild(option);
  });
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function byTypeOrder(a, b) {
  return TYPE_ORDER.indexOf(a) - TYPE_ORDER.indexOf(b);
}

function bindEvents() {
  els.search.addEventListener("input", () => {
    state.filters.query = els.search.value.trim().toLowerCase();
    render();
  });
  els.type.addEventListener("change", () => {
    state.filters.type = els.type.value;
    render();
  });
  els.status.addEventListener("change", () => {
    state.filters.status = els.status.value;
    render();
  });
  els.place.addEventListener("change", () => {
    state.filters.place = els.place.value;
    render();
  });
  els.reset.addEventListener("click", () => {
    state.filters = { query: "", type: "", status: "", place: "" };
    els.search.value = "";
    els.type.value = "";
    els.status.value = "";
    els.place.value = "";
    render();
    els.search.focus();
  });
  els.download.addEventListener("click", () => {
    const link = document.createElement("a");
    link.href = new URL(SESSIONS_CSV, window.location.href).href;
    link.download = "sessions.csv";
    link.click();
  });
}

function render() {
  const filtered = state.sessions.filter(matchesFilters);
  els.statusText.hidden = filtered.length > 0;
  els.statusText.textContent = filtered.length ? "" : "Aucune session ne correspond aux filtres.";
  els.meta.textContent = `${filtered.length} / ${state.sessions.length} sessions`;
  els.sections.innerHTML = "";

  const groups = groupByType(filtered);
  groups.forEach(([type, sessions]) => {
    const section = document.createElement("section");
    section.className = "sessions-section";
    section.innerHTML = `
      <div class="sessions-section__header">
        ${iconMarkup(type)}
        <div>
          <h2 class="sessions-section__title">${escapeHtml(TYPE_LABELS[type] || type || "Autres sessions")}</h2>
          <span class="sessions-section__count">${sessions.length} ${sessions.length > 1 ? "entrées" : "entrée"}</span>
        </div>
      </div>
      <div class="sessions-list">
        ${sessions.map(renderCard).join("")}
      </div>
    `;
    els.sections.appendChild(section);
  });

  document.querySelectorAll(".session-card__more").forEach((button) => {
    button.addEventListener("click", () => {
      const details = document.getElementById(button.getAttribute("aria-controls"));
      const expanded = button.getAttribute("aria-expanded") === "true";
      button.setAttribute("aria-expanded", String(!expanded));
      button.textContent = expanded ? "Voir plus" : "Réduire";
      details.hidden = expanded;
    });
  });
}

function matchesFilters(session) {
  if (state.filters.query && !session.search_text.includes(state.filters.query)) return false;
  if (state.filters.type && session.type_session !== state.filters.type) return false;
  if (state.filters.status && session.statut_documentaire !== state.filters.status) return false;
  if (state.filters.place && session.place_label !== state.filters.place) return false;
  return true;
}

function groupByType(sessions) {
  const groups = new Map();
  sessions.forEach((session) => {
    const type = session.type_session || "autre";
    if (!groups.has(type)) groups.set(type, []);
    groups.get(type).push(session);
  });
  return [...groups.entries()].sort(([typeA], [typeB]) => byTypeOrder(typeA, typeB));
}

function renderCard(session) {
  const detailsId = `details-${session.id}`;
  const targetClass = window.location.hash === `#${session.id}` ? " session-card--target" : "";
  return `
    <article class="session-card${targetClass}" id="${escapeAttr(session.id)}">
      <div class="session-card__header">
        ${iconMarkup(session.type_session)}
        <div class="session-card__heading">
          <h3 class="session-card__title">${escapeHtml(session.label || session.id)}</h3>
          <p class="session-card__meta">${escapeHtml(formatDate(session.date))}${session.ville ? ` · ${escapeHtml(session.ville)}` : ""}</p>
        </div>
      </div>
      <div class="session-card__badges">
        ${badge(TYPE_LABELS[session.type_session] || session.type_session || "Session")}
        ${badge(STATUS_LABELS[session.statut_documentaire] || session.statut_documentaire || "statut non renseigné", "muted")}
        ${session.place_id ? badge(session.place_id, "muted") : ""}
      </div>
      ${line("Lieu", placeText(session))}
      ${line("Titres", listPreview(session.titres, 4))}
      ${line("Participants", listPreview(session.participants, 4))}
      <button class="session-card__more" type="button" aria-expanded="false" aria-controls="${detailsId}">Voir plus</button>
      <div class="session-card__details" id="${detailsId}" hidden>
        ${detail("Producteur", session.producteur)}
        ${detail("Ingénieur", session.ingenieur_son)}
        ${detail("Ère", session.ere)}
        ${detail("Sources", listTags(session.sources || [session.source]))}
        ${detail("URLs", linkTags(session.urls))}
        ${detail("Relations", relationTags(session.relations))}
        ${detail("Sortie officielle", releaseText(session.premiere_sortie_officielle))}
        ${detail("Notes", session.notes)}
        <p class="session-card__id"><code>${escapeHtml(session.id)}</code></p>
      </div>
    </article>
  `;
}

function placeText(session) {
  const parts = [session.lieu || session.studio, session.place_id].filter(Boolean);
  return parts.join(" · ");
}

function line(label, value) {
  if (!value) return "";
  return `<p class="session-card__line"><strong>${escapeHtml(label)} :</strong> ${value}</p>`;
}

function detail(label, value) {
  if (!value) return "";
  return `
    <div class="session-detail">
      <p class="session-detail__label">${escapeHtml(label)}</p>
      <div class="session-detail__value">${typeof value === "string" ? escapeHtml(value) : value}</div>
    </div>
  `;
}

function listPreview(values, limit) {
  if (!Array.isArray(values) || values.length === 0) return "";
  const visible = values.slice(0, limit).map(escapeHtml).join(", ");
  const extra = values.length > limit ? ` +${values.length - limit}` : "";
  return `${visible}${extra}`;
}

function listTags(values) {
  const items = Array.isArray(values) ? values.filter(Boolean) : [values].filter(Boolean);
  if (!items.length) return "";
  return `<div class="session-tags">${items.map((item) => `<span class="session-tag">${escapeHtml(item)}</span>`).join("")}</div>`;
}

function linkTags(urls) {
  if (!Array.isArray(urls) || urls.length === 0) return "";
  return `<div class="session-tags">${urls.map((url) => `<a class="session-tag session-tag--link" href="${escapeAttr(url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(shortUrl(url))}</a>`).join("")}</div>`;
}

function relationTags(relations) {
  if (!relations || typeof relations !== "object") return "";
  const tags = Object.entries(relations).flatMap(([kind, values]) => {
    const list = Array.isArray(values) ? values : [values];
    return list.filter(Boolean).map((value) => `${kind}: ${value}`);
  });
  return listTags(tags);
}

function releaseText(release) {
  if (!release || typeof release !== "object" || Object.keys(release).length === 0) return "";
  return listTags(Object.entries(release).map(([key, value]) => `${key}: ${value}`));
}

function badge(text, tone = "default") {
  const className = tone === "muted" ? "session-badge session-badge--muted" : "session-badge";
  return `<span class="${className}">${escapeHtml(text)}</span>`;
}

function formatDate(value) {
  const text = String(value || "Date non renseignée");
  const match = text.match(/^(\d{4})-(\d{2})-(\d{2})$/);
  if (!match) return text;
  const [, year, month, day] = match;
  if (month === "00") return year;
  if (day === "00") return `${MONTHS[Number(month)] || month} ${year}`;
  return `${Number(day)} ${MONTHS[Number(month)] || month} ${year}`;
}

function shortUrl(url) {
  try {
    const parsed = new URL(url);
    return parsed.hostname.replace(/^www\./, "");
  } catch {
    return url;
  }
}

function iconMarkup(type) {
  const common = 'xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"';
  if (type === "rehearsal") {
    return `<svg ${common}><path d="M4 14a8 8 0 0 1 16 0"/><path d="M6 14v4"/><path d="M18 14v4"/><path d="M10 18h4"/></svg>`;
  }
  if (type === "demo") {
    return `<svg ${common}><rect width="18" height="14" x="3" y="5" rx="2"/><path d="M8 12h8"/><path d="M8 15h4"/><circle cx="8" cy="9" r="1"/></svg>`;
  }
  if (type === "radio") {
    return `<svg ${common}><path d="M4 11a8 8 0 0 1 16 0"/><path d="M8 11a4 4 0 0 1 8 0"/><path d="M12 11v8"/><path d="M8 19h8"/></svg>`;
  }
  if (type === "television") {
    return `<svg ${common}><rect width="18" height="12" x="3" y="6" rx="2"/><path d="m8 3 4 3 4-3"/><path d="M9 21h6"/></svg>`;
  }
  return `<svg ${common}><path d="M4 12h16"/><path d="M4 18h16"/><path d="M4 6h16"/><path d="M8 6v12"/><path d="M16 6v12"/></svg>`;
}

function focusHashTarget() {
  if (!window.location.hash) return;
  const target = document.querySelector(window.location.hash);
  if (!target) return;
  target.scrollIntoView({ block: "center" });
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function escapeAttr(value) {
  return escapeHtml(value).replaceAll("`", "&#96;");
}
