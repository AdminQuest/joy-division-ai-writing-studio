const STOPWORDS = new Set([
  'a','an','and','are','as','at','be','by','for','from','in','is','it','of','on','or','that','the','to','with',
  'au','aux','ce','ces','dans','de','des','du','elle','en','et','il','la','le','les','pour','que','qui','sur','un','une',
  'avec','comme','par','plus','son','sa','ses','leur','leurs','est','sont','être','etre','fait','faites'
]);

const TOKEN_RE = /[\wÀ-ÿ']+/gu;
const SOURCE_ID_ALIASES = {
  'S-BROLL-JOY-001': 'S68',
  'S20': 'S72',
  'S35': 'S41',
  'S37': 'S45',
  'S41-HIST': 'S73'
};
const FALLBACK_SOURCE_LABELS = {
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

function currentFilters() {
  return {
    kind: $('kind')?.value || '',
    chapter: $('chapter-filter')?.value || '',
    source: $('source-filter')?.value || '',
    type: $('type-filter')?.value || '',
    importance: $('importance-filter')?.value || '',
    proof: $('proof-filter')?.value || '',
    concept: $('concept-filter')?.value || '',
    motif: $('motif-filter')?.value || ''
  };
}

function hasActiveFilters(filters) {
  return Object.values(filters).some(Boolean);
}

function matchesFilters(item, filters) {
  if (filters.kind && item.record.kind !== filters.kind) return false;
  if (filters.chapter && !item.chapters.includes(filters.chapter)) return false;
  if (filters.source && !item.sourceIds.includes(filters.source)) return false;
  if (filters.type && item.type !== filters.type) return false;
  if (filters.importance && item.importance !== filters.importance) return false;
  if (filters.proof && item.proof !== filters.proof) return false;
  if (filters.concept && !item.concepts.includes(filters.concept)) return false;
  if (filters.motif && !item.motifs.includes(filters.motif)) return false;
  return true;
}

function kindWeight(kind) {
  return {atom: 1.25, quote: 1.2, chronology: 1.1, concept: 1.05, myth: 1.05, motif: 1.05}[kind] || 1;
}

function scoreItem(item, terms, normalizedQuery, filters) {
  let score = normalizedQuery.length >= 4 && item.normalizedText.includes(normalizedQuery) ? 25 : 0;
  let matched = 0;
  const details = [];
  for (const term of terms) {
    const count = item.tokenCounts.get(term) || 0;
    const partial = count ? 0 : (item.normalizedText.includes(term) ? 1 : 0);
    const termScore = count * 6 + partial * 2;
    if (termScore > 0) {
      matched += 1;
      score += termScore;
      details.push(`${term}:${count || 'partial'}`);
    }
  }
  if (terms.length && matched === terms.length) score += 12;
  if (item.record.id && normalizeText(item.record.id).includes(normalizedQuery)) score += 20;
  if (hasActiveFilters(filters)) score += 5;
  return {score: Math.round(score * kindWeight(item.record.kind)), details};
}

function searchRecords(query, filters) {
  const terms = unique(tokenize(query));
  const normalizedQuery = normalizeText(query).trim();
  const filterOnly = !terms.length && normalizedQuery.length < 3 && hasActiveFilters(filters);
  if (!filterOnly && !terms.length && normalizedQuery.length < 3) return [];

  const results = [];
  for (const item of state.index) {
    if (!matchesFilters(item, filters)) continue;
    const scored = filterOnly ? {score: 1, details: ['filtre']} : scoreItem(item, terms, normalizedQuery, filters);
    if (scored.score > 0) results.push({score: scored.score, record: conciseRecord(item.record, scored.details.join(', ')), order: item.order});
  }
  return results.sort((a, b) => (b.score - a.score) || (a.order - b.order));
}

function conciseRecord(record, scoreDetails = '') {
  const data = recordData(record);
  const sourceId = data.source_id ? normalizeSourceId(data.source_id) : '';
  return {
    id: record.id,
    kind: record.kind,
    file: record.file,
    heading: record.heading,
    summary_fields: Object.fromEntries(Object.entries({
      titre: data.titre || recordTitle(record),
      source_id: sourceId,
      source_label: data.source_label || sourceLabel(sourceId),
      pages_pdf: data.pages_pdf,
      page_pdf: data.page_pdf,
      type_unite: data.type_unite,
      importance: data.importance,
      niveau_preuve: data.niveau_preuve,
      concepts: data.concepts,
      motifs: data.motifs,
      chapitres: data.chapitres || data.chapters,
      citation_originale: data.citation_originale,
      traduction_editoriale_fr: data.traduction_editoriale_fr,
      song: data.song,
      name: data.name,
      role: data.role,
      date: data.date,
      event: data.event,
      certainty: data.certainty,
      score_details: scoreDetails
    }).filter(([, value]) => value !== undefined && value !== null && value !== ''))
  };
}

function addField(dl, key, value) {
  if (!dl || value === undefined || value === null || value === '') return;
  const dt = document.createElement('dt');
  dt.textContent = key;
  const dd = document.createElement('dd');
  dd.textContent = typeof value === 'object' ? JSON.stringify(value, null, 2) : value;
  dl.appendChild(dt);
  dl.appendChild(dd);
}

function clearResults() {
  if ($('results')) $('results').innerHTML = '';
  if ($('results-meta')) $('results-meta').textContent = '';
  if ($('pagination')) $('pagination').innerHTML = '';
}

function renderPagination(totalPages) {
  const container = $('pagination');
  if (!container) return;
  container.innerHTML = '';
  if (totalPages <= 1) return;
  const button = (label, page, disabled = false, active = false) => {
    const node = document.createElement('button');
    node.textContent = label;
    node.disabled = disabled;
    if (active) node.classList.add('active');
    node.addEventListener('click', () => { state.page = page; renderCurrentPage(); });
    return node;
  };
  container.appendChild(button('←', Math.max(1, state.page - 1), state.page === 1));
  for (let page = Math.max(1, state.page - 3); page <= Math.min(totalPages, state.page + 3); page += 1) container.appendChild(button(String(page), page, false, page === state.page));
  container.appendChild(button('→', Math.min(totalPages, state.page + 1), state.page === totalPages));
}

function renderCurrentPage() {
  clearResults();
  const results = $('results');
  const meta = $('results-meta');
  const template = $('result-template');
  if (!results || !meta || !template) return;
  const total = state.results.length;
  const totalPages = Math.ceil(total / state.perPage) || 1;
  const start = (state.page - 1) * state.perPage;
  const pageItems = state.results.slice(start, start + state.perPage);
  meta.textContent = `${total} résultat(s) · page ${state.page}/${totalPages}`;
  if (!pageItems.length) {
    const empty = document.createElement('div');
    empty.className = 'status-card';
    empty.textContent = 'Aucun résultat.';
    results.appendChild(empty);
    return;
  }
  for (const item of pageItems) {
    const node = template.content.cloneNode(true);
    node.querySelector('.result-kind').textContent = item.record.kind || '';
    node.querySelector('.result-score').textContent = `score ${item.score}`;
    node.querySelector('.result-title').textContent = item.record.id || item.record.summary_fields?.titre || '(sans id)';
    node.querySelector('.result-file').textContent = item.record.file || '';
    const fields = node.querySelector('.result-fields');
    for (const [key, value] of Object.entries(item.record.summary_fields || {})) addField(fields, key, value);
    results.appendChild(node);
  }
  renderPagination(totalPages);
}

function renderResults(results, perPage = 10) {
  state.results = Array.isArray(results) ? results : [];
  state.perPage = Number(perPage) || 10;
  state.page = 1;
  renderCurrentPage();
}

function activeFilterLabel(filters) {
  const labels = [];
  if (filters.kind) labels.push(`type=${filters.kind}`);
  if (filters.chapter) labels.push(filters.chapter);
  if (filters.source) labels.push(`source=${filters.source}`);
  if (filters.type) labels.push(`type_unite=${filters.type}`);
  if (filters.importance) labels.push(`importance=${filters.importance}`);
  if (filters.proof) labels.push(`preuve=${filters.proof}`);
  if (filters.concept) labels.push(`concept=${filters.concept}`);
  if (filters.motif) labels.push(`motif=${filters.motif}`);
  return labels.join(' · ');
}

function performSearch() {
  const query = $('query')?.value.trim() || '';
  const filters = currentFilters();
  if ($('results-title')) $('results-title').textContent = activeFilterLabel(filters) || 'Résultats';
  if ($('results')) $('results').innerHTML = '<div class="status-card">Recherche en cours…</div>';
  renderResults(searchRecords(query, filters), $('top')?.value || 10);
}

function renderSources() {
  const container = $('sources-list');
  const count = $('sources-count');
  if (!container || !count) return;
  container.innerHTML = '';
  count.textContent = `${state.sources.length} source(s)`;
  for (const source of state.sources) {
    const wrapper = document.createElement('div');
    wrapper.className = 'source-entry';
    const button = document.createElement('button');
    button.innerHTML = `<div class="source-title">${source.source_label}</div><div class="source-meta">${source.counts.atom || 0} atomes · ${source.counts.quote || 0} citations · ${source.counts.chronology || 0} chronologies · ${source.records.length} enregistrements</div>`;
    button.addEventListener('click', () => {
      const select = $('source-filter');
      if (select) select.value = source.source_id;
      performSearch();
    });
    wrapper.appendChild(button);
    container.appendChild(wrapper);
  }
}

async function loadJson(path, fallback = []) {
  try {
    const response = await fetch(path, {cache: 'no-store'});
    if (!response.ok) throw new Error(`${path} ${response.status}`);
    return await response.json();
  } catch (error) {
    console.warn('Fallback', path, error);
    return fallback;
  }
}

async function loadText(path, fallback = '') {
  try {
    const response = await fetch(path, {cache: 'no-store'});
    if (!response.ok) throw new Error(`${path} ${response.status}`);
    return await response.text();
  } catch (error) {
    console.warn('Fallback', path, error);
    return fallback;
  }
}

function splitTableRow(line) {
  return line.trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map(value => String(value || '').trim().replace(/`/g, ''));
}

function inferSourceId(id, sourceCell) {
  const direct = String(id || '').match(/^(S\d{2})-Q\d+/);
  if (direct) return normalizeSourceId(direct[1]);
  const fromSource = String(sourceCell || '').match(/S\d{2}(?:-HIST)?/);
  return fromSource ? normalizeSourceId(fromSource[0]) : '';
}

function parseConsolidatedQuotesMarkdown(markdown) {
  const rows = [];
  let mode = '';
  for (const line of String(markdown || '').split(/\r?\n/)) {
    if (line.startsWith('## 1.1.')) { mode = 'historical'; continue; }
    if (line.startsWith('## 2.')) { mode = 'atomized'; continue; }
    if (!line.trim().startsWith('|') || line.includes('---')) continue;
    const cells = splitTableRow(line);
    if (!cells.length || /^ID/.test(cells[0]) || /^id$/i.test(cells[0])) continue;
    if (mode === 'historical' && cells.length >= 5) {
      const [id, source, type, entry, status] = cells;
      const sourceId = inferSourceId(id, source);
      rows.push({kind: 'quote', id, file: 'registers/quotes/master_quotes.md', heading: 'citation historique consolidée', data: {id, source_id: sourceId, citation_originale: entry, type_citation: type, statut_consolidation: status, statut_verification: status, chapitres: ['Chapitre 1']}});
    } else if (mode === 'atomized' && cells.length >= 4) {
      const [id, citation, status, usage] = cells;
      const sourceId = inferSourceId(id, '');
      rows.push({kind: 'quote', id, file: 'registers/quotes/master_quotes.md', heading: 'citation atomisée consolidée', data: {id, source_id: sourceId, citation_originale: citation, usage_recommande: usage, statut_consolidation: status, statut_verification: status}});
    }
  }
  return rows;
}

function mergeConsolidatedQuotes(records, quotes) {
  const existing = new Set(records.map(record => record.id));
  return records.concat(quotes.filter(record => !existing.has(record.id)));
}

function resetFilters() {
  for (const id of ['kind','chapter-filter','source-filter','type-filter','importance-filter','proof-filter','concept-filter','motif-filter']) {
    if ($(id)) $(id).value = '';
  }
  if ($('query')) $('query').value = '';
  clearResults();
  if ($('results-title')) $('results-title').textContent = 'Résultats';
}

function bindUi() {
  const form = $('search-form');
  if (form) form.addEventListener('submit', event => { event.preventDefault(); performSearch(); });
  const reset = $('reset-filters');
  if (reset) reset.addEventListener('click', resetFilters);
  for (const id of ['kind','chapter-filter','source-filter','type-filter','importance-filter','proof-filter','concept-filter','motif-filter','top']) {
    if ($(id)) $(id).addEventListener('change', () => {
      if (($('query')?.value || '').trim() || hasActiveFilters(currentFilters())) performSearch();
    });
  }
  for (const button of document.querySelectorAll('.example-query')) {
    button.addEventListener('click', () => {
      if ($('query')) $('query').value = button.dataset.query || '';
      performSearch();
    });
  }
}

async function init() {
  const card = $('status-card');
  try {
    const [records, registry, quotesMarkdown] = await Promise.all([
      loadJson('../../exports/generated/all_records.json', []),
      loadJson('../../data/registre.json', []),
      loadText('../../registers/quotes/master_quotes.md', '')
    ]);
    buildSourceLabels(registry, records);
    state.records = mergeConsolidatedQuotes(records, parseConsolidatedQuotesMarkdown(quotesMarkdown));
    buildIndex();
    buildSourcesIndex();
    buildFilterControls();
    renderSources();
    bindUi();
    const counts = {};
    for (const record of state.records) counts[record.kind || 'unknown'] = (counts[record.kind || 'unknown'] || 0) + 1;
    const summary = Object.entries(counts).sort().map(([kind, count]) => `${kind}: ${count}`).join(' · ');
    if (card) card.textContent = `RAG 2 chargé · ${state.records.length} enregistrements · ${summary} · filtres ${card.dataset.filters || ''}`;
  } catch (error) {
    if (card) card.textContent = `Erreur : ${error.message}`;
  }
}

window.rag2 = {state, searchRecords, currentFilters, performSearch};
window.addEventListener('error', event => console.error('RAG Studio error', event.error || event.message));
window.addEventListener('unhandledrejection', event => console.error('RAG Studio rejected promise', event.reason));

init();
