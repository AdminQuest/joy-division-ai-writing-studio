const STOPWORDS = new Set([
  'a','an','and','are','as','at','be','by','for','from','in','is','it','of','on','or','that','the','to','with',
  'au','aux','ce','ces','dans','de','des','du','elle','en','et','il','la','le','les','pour','que','qui','sur','un','une',
  'avec','comme','par','plus','son','sa','ses','leur','leurs','est','sont','être','etre','fait','faites'
]);

const TOKEN_RE = /[\wÀ-ÿ']+/gu;
const SOURCE_ID_ALIASES = {
  'S-BROLL-JOY-001': 'S68',
  'S41-HIST': 'S73'
};
const FALLBACK_SOURCE_LABELS = {
  S20: 'S20 — Dodge, Mapping Manchester’s housing problems, Manchester Geographies, s.d.',
  S41: 'S41 — Hook, Unknown Pleasures, 2012',
  S45: 'S45 — Curtis, Touching from a Distance, 1995',
  S46: 'S46 — Johnson, An Ideal for Living, 1984',
  S47: 'S47 — West, Joy Division, 1984',
  S68: 'S68 — Broll, Joy Division, 1988',
  S69: 'S69 — Greig & Strong, But We Remember When We Were Young, 2014',
  S70: 'S70 — Suatoni, Dal cuore della città / From the Centre of the City, 1990',
  S71: 'S71 — Flowers, Dreams Never End, 1995/2012',
  S72: 'S72 — Reynolds, Rip It Up and Start Again, 2005/2006',
  S73: 'S73 — Blue Orchids, entrée historique à consolider, s.d.',
  S74: 'S74 — Middles, From Joy Division to New Order, 1996'
};

const state = {
  records: [],
  index: [],
  sources: [],
  sourceLabels: {...FALLBACK_SOURCE_LABELS},
  results: [],
  page: 1,
  perPage: 10
};

const $ = id => document.getElementById(id);

function normalizeSourceId(value) {
  return SOURCE_ID_ALIASES[String(value || '')] || String(value || '');
}

function normalizeText(value) {
  return String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
}

function normalizeValues(value) {
  if (value === undefined || value === null || value === '') return [];
  if (Array.isArray(value)) return value.flatMap(normalizeValues);
  if (typeof value === 'object') {
    for (const key of ['niveau', 'statut', 'confiance', 'value', 'id', 'name']) {
      if (value[key] !== undefined) return normalizeValues(value[key]);
    }
    return [];
  }
  return [String(value).trim()].filter(Boolean);
}

function unique(values) {
  return [...new Set(values.flatMap(normalizeValues).filter(Boolean))];
}

function flatten(value) {
  if (value === null || value === undefined) return '';
  if (typeof value === 'string') return value;
  if (typeof value === 'number' || typeof value === 'boolean') return String(value);
  if (Array.isArray(value)) return value.map(flatten).join(' ');
  if (typeof value === 'object') return Object.entries(value).map(([k, v]) => `${k} ${flatten(v)}`).join(' ');
  return String(value);
}

function tokenize(value) {
  return (normalizeText(value).match(TOKEN_RE) || [])
    .map(token => token.replace(/^'+|'+$/g, ''))
    .filter(token => token.length > 2 && !STOPWORDS.has(token));
}

function valueAt(obj, path) {
  let cursor = obj;
  for (const part of path.split('.')) {
    if (!cursor || typeof cursor !== 'object' || !(part in cursor)) return '';
    cursor = cursor[part];
  }
  return cursor;
}

function recordData(record) {
  return record.data || record.summary_fields || {};
}

function recordTitle(record) {
  const data = recordData(record);
  return data.titre || data.event || data.name || data.full_name || data.song || data.citation_originale || record.heading || record.id || '(sans titre)';
}

function sourceLabel(sourceId) {
  const id = normalizeSourceId(sourceId);
  return state.sourceLabels[id] || state.sourceLabels[sourceId] || id || '';
}

function compactTitle(title) {
  return String(title || '')
    .replace('Unknown Pleasures: Inside Joy Division', 'Unknown Pleasures')
    .replace('Touching from a Distance: Ian Curtis and Joy Division', 'Touching from a Distance')
    .replace('An Ideal for Living: An History of Joy Division', 'An Ideal for Living')
    .slice(0, 80);
}

function makeSourceLabel(id, data = {}) {
  const sourceId = normalizeSourceId(id);
  if (data.source_label) return data.source_label;
  const author = data.auteur || data.author || '';
  const title = compactTitle(data.titre || data.title || '');
  const year = data.annee || data.source_year || '';
  const label = [author, title, year].filter(Boolean).join(', ');
  return label ? `${sourceId} — ${label}` : (FALLBACK_SOURCE_LABELS[sourceId] || sourceId);
}

function buildSourceLabels(registry, records) {
  const labels = {...FALLBACK_SOURCE_LABELS};
  for (const entry of registry || []) {
    const id = normalizeSourceId(entry.id || entry.source_id);
    if (!id) continue;
    labels[id] = makeSourceLabel(id, entry);
    for (const alias of normalizeValues(entry.legacy_id || entry.legacy_ids)) labels[alias] = labels[id];
  }
  for (const record of records) {
    const data = recordData(record);
    for (const id of sourceIdsForRecord(record)) {
      if (!labels[id]) labels[id] = makeSourceLabel(id, data);
    }
  }
  state.sourceLabels = labels;
}

function sourceIdsForRecord(record) {
  const data = recordData(record);
  const ids = [];
  ids.push(...normalizeValues(data.source_id).map(normalizeSourceId));
  ids.push(...normalizeValues(data.sources).map(value => normalizeSourceId(String(value).match(/S\d{2}/)?.[0] || value)));
  const labelMatch = String(data.source_label || '').match(/S\d{2}/);
  if (labelMatch) ids.push(labelMatch[0]);
  const fallback = flatten(data).match(/\bS\d{2}\b/g) || [];
  ids.push(...fallback.map(normalizeSourceId));
  return unique(ids);
}

function chaptersForRecord(record) {
  const data = recordData(record);
  const explicit = unique([data.chapitres, data.chapters, data.chapitre]);
  const fallback = flatten(data).match(/Chapitre\s+\d+/g) || [];
  return unique([...explicit, ...fallback]);
}

function typeValue(record) {
  return normalizeValues(recordData(record).type_unite)[0] || '';
}

function importanceValue(record) {
  const data = recordData(record);
  return normalizeValues(valueAt(data, 'importance.niveau') || data.importance)[0] || '';
}

function proofValue(record) {
  const data = recordData(record);
  return normalizeValues(valueAt(data, 'niveau_preuve.statut') || valueAt(data, 'niveau_preuve.confiance') || data.fiabilite || data.certainty)[0] || '';
}

function conceptsForRecord(record) {
  return unique(recordData(record).concepts);
}

function motifsForRecord(record) {
  return unique(recordData(record).motifs);
}

function recordText(record) {
  const data = recordData(record);
  return [
    record.id || '', record.kind || '', record.heading || '', record.file || '', recordTitle(record),
    data.source_label || '', sourceIdsForRecord(record).map(sourceLabel).join(' '), flatten(data)
  ].join('\n');
}

function buildIndex() {
  state.index = state.records.map((record, order) => {
    const rawText = recordText(record);
    const tokens = tokenize(rawText);
    const tokenCounts = new Map();
    for (const token of tokens) tokenCounts.set(token, (tokenCounts.get(token) || 0) + 1);
    return {
      order,
      record,
      rawText,
      normalizedText: normalizeText(rawText),
      tokenCounts,
      sourceIds: sourceIdsForRecord(record),
      chapters: chaptersForRecord(record),
      type: typeValue(record),
      importance: importanceValue(record),
      proof: proofValue(record),
      concepts: conceptsForRecord(record),
      motifs: motifsForRecord(record)
    };
  });
}

function buildSourcesIndex() {
  const grouped = new Map();
  for (const record of state.records) {
    for (const id of sourceIdsForRecord(record)) {
      if (!grouped.has(id)) grouped.set(id, {source_id: id, source_label: sourceLabel(id), records: [], counts: {}});
      const entry = grouped.get(id);
      entry.records.push(record);
      entry.counts[record.kind] = (entry.counts[record.kind] || 0) + 1;
    }
  }
  state.sources = [...grouped.values()].sort((a, b) => a.source_id.localeCompare(b.source_id, undefined, {numeric: true}));
}

function fillSelect(id, values, labelFn = value => value) {
  const select = $(id);
  if (!select) return;
  const first = select.querySelector('option')?.cloneNode(true);
  select.innerHTML = '';
  if (first) select.appendChild(first);
  for (const value of values) {
    const option = document.createElement('option');
    option.value = value;
    option.textContent = labelFn(value);
    select.appendChild(option);
  }
}

function optionLabel(value, max = 78) {
  const label = String(value || '');
  return label.length > max ? label.slice(0, max) + '…' : label;
}

function buildFilterControls() {
  const chapters = unique(state.index.flatMap(item => item.chapters)).sort((a, b) => a.localeCompare(b, undefined, {numeric: true}));
  const sources = unique([...state.sources.map(source => source.source_id), ...state.index.flatMap(item => item.sourceIds)]).sort((a, b) => a.localeCompare(b, undefined, {numeric: true}));
  const types = unique(state.index.map(item => item.type)).sort();
  const importances = unique(state.index.map(item => item.importance)).sort();
  const proofs = unique(state.index.map(item => item.proof)).sort();
  const concepts = unique(state.index.flatMap(item => item.concepts)).sort();
  const motifs = unique(state.index.flatMap(item => item.motifs)).sort();

  fillSelect('chapter-filter', chapters);
  fillSelect('source-filter', sources, id => `${id} — ${sourceLabel(id).replace(/^S\d+\s+—\s+/, '')}`);
  fillSelect('type-filter', types);
  fillSelect('importance-filter', importances);
  fillSelect('proof-filter', proofs);
  fillSelect('concept-filter', concepts, optionLabel);
  fillSelect('motif-filter', motifs, optionLabel);

  const card = $('status-card');
  if (card) card.dataset.filters = `chapitres:${chapters.length}; sources:${sources.length}; types:${types.length}; importances:${importances.length}; preuves:${proofs.length}; concepts:${concepts.length}; motifs:${motifs.length}`;
}

function scoreItem(item, queryTokens, rawQuery) {
  let score = 0;
  for (const token of queryTokens) score += (item.tokenCounts.get(token) || 0) * 3;
  if (rawQuery && item.normalizedText.includes(rawQuery)) score += 20;
  if (item.record.kind === 'atom') score += 2;
  if (item.importance.toLowerCase().includes('critique')) score += 4;
  if (item.importance.toLowerCase().includes('majeure')) score += 2;
  return score;
}

function passesFilters(item) {
  const chapter = $('chapter-filter')?.value || '';
  const source = $('source-filter')?.value || '';
  const type = $('type-filter')?.value || '';
  const importance = $('importance-filter')?.value || '';
  const proof = $('proof-filter')?.value || '';
  const concept = $('concept-filter')?.value || '';
  const motif = $('motif-filter')?.value || '';
  if (chapter && !item.chapters.includes(chapter)) return false;
  if (source && !item.sourceIds.includes(source)) return false;
  if (type && item.type !== type) return false;
  if (importance && item.importance !== importance) return false;
  if (proof && item.proof !== proof) return false;
  if (concept && !item.concepts.includes(concept)) return false;
  if (motif && !item.motifs.includes(motif)) return false;
  return true;
}

function runSearch() {
  const raw = normalizeText($('search-input')?.value || '');
  const queryTokens = tokenize(raw);
  const hasQuery = raw.length > 0 || queryTokens.length > 0;
  const results = [];
  for (const item of state.index) {
    if (!passesFilters(item)) continue;
    const score = hasQuery ? scoreItem(item, queryTokens, raw) : 1;
    if (!hasQuery || score > 0) results.push({...item, score});
  }
  results.sort((a, b) => b.score - a.score || a.order - b.order);
  state.results = results;
  state.page = 1;
  renderResults();
}

function renderBadges(values, cls = '') {
  return unique(values).slice(0, 8).map(value => `<span class="badge ${cls}">${escapeHtml(value)}</span>`).join('');
}

function escapeHtml(value) {
  return String(value || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function renderRecord(item) {
  const record = item.record;
  const data = recordData(record);
  const sources = item.sourceIds.map(id => sourceLabel(id));
  const chapters = item.chapters;
  const title = recordTitle(record);
  const body = data.resume || data.contenu || data.note || data.extrait || data.definition || data.usage || data.arbitrage || data.reference_complete || '';
  const path = record.file || '';
  return `
    <article class="result-card">
      <div class="result-meta">
        <span>${escapeHtml(record.kind || 'record')}</span>
        <span>${escapeHtml(record.id || '')}</span>
        ${item.score ? `<span>score ${Math.round(item.score)}</span>` : ''}
      </div>
      <h3>${escapeHtml(title)}</h3>
      <div class="badges">
        ${renderBadges(chapters, 'chapter')}
        ${renderBadges(sources, 'source')}
        ${item.type ? `<span class="badge">${escapeHtml(item.type)}</span>` : ''}
        ${item.importance ? `<span class="badge importance">${escapeHtml(item.importance)}</span>` : ''}
        ${item.proof ? `<span class="badge proof">${escapeHtml(item.proof)}</span>` : ''}
      </div>
      ${body ? `<p>${escapeHtml(flatten(body)).slice(0, 900)}</p>` : ''}
      ${path ? `<div class="path">${escapeHtml(path)}</div>` : ''}
    </article>
  `;
}

function renderResults() {
  const list = $('results-list');
  const count = $('results-count');
  const pageInfo = $('page-info');
  const total = state.results.length;
  const pages = Math.max(1, Math.ceil(total / state.perPage));
  state.page = Math.min(state.page, pages);
  const start = (state.page - 1) * state.perPage;
  const current = state.results.slice(start, start + state.perPage);
  if (count) count.textContent = `${total} résultat${total > 1 ? 's' : ''}`;
  if (pageInfo) pageInfo.textContent = `Page ${state.page} / ${pages}`;
  if (list) list.innerHTML = current.map(renderRecord).join('') || '<p class="muted">Aucun résultat.</p>';
  const status = $('status-card');
  if (status) status.innerHTML = `<strong>Corpus chargé.</strong> ${state.records.length} enregistrements, ${state.sources.length} sources, ${total} résultats affichables.`;
}

async function loadJson(path, fallback) {
  const response = await fetch(path);
  if (!response.ok) return fallback;
  return response.json();
}

async function init() {
  try {
    const [records, registry] = await Promise.all([
      loadJson('../../exports/generated/source_records.json', []),
      loadJson('../../data/registre.json', [])
    ]);
    state.records = records;
    buildSourceLabels(registry, records);
    buildIndex();
    buildSourcesIndex();
    buildFilterControls();
    runSearch();
  } catch (error) {
    const status = $('status-card');
    if (status) status.textContent = `Erreur de chargement: ${error.message}`;
  }
}

for (const id of ['search-input','chapter-filter','source-filter','type-filter','importance-filter','proof-filter','concept-filter','motif-filter']) {
  const element = $(id);
  if (element) element.addEventListener('input', runSearch);
}

$('reset-btn')?.addEventListener('click', () => {
  for (const id of ['search-input','chapter-filter','source-filter','type-filter','importance-filter','proof-filter','concept-filter','motif-filter']) {
    const element = $(id);
    if (element) element.value = '';
  }
  runSearch();
});

$('prev-page')?.addEventListener('click', () => {
  state.page = Math.max(1, state.page - 1);
  renderResults();
});

$('next-page')?.addEventListener('click', () => {
  const pages = Math.max(1, Math.ceil(state.results.length / state.perPage));
  state.page = Math.min(pages, state.page + 1);
  renderResults();
});

init();
