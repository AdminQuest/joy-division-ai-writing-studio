const RAG2_STOPWORDS = new Set([
  'a','an','and','are','as','at','be','by','for','from','in','is','it','of','on','or','that','the','to','with',
  'au','aux','ce','ces','dans','de','des','du','elle','en','et','il','la','le','les','pour','que','qui','sur','un','une',
  'avec','comme','par','plus','son','sa','ses','leur','leurs','est','sont','être','etre','fait','faites'
]);

const SOURCE_ALIASES = {
  'S-BROLL-JOY-001': 'S68',
  'S20': 'S72',
  'S35': 'S41',
  'S37': 'S45',
  'S41-HIST': 'S73'
};

const FALLBACK_SOURCES = {
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
  sourceLabels: {...FALLBACK_SOURCES},
  sources: [],
  results: [],
  page: 1,
  perPage: 10
};

const $ = id => document.getElementById(id);

function normalizeText(value) {
  return String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
}

function normalizeSourceId(value) {
  const id = String(value || '').trim();
  return SOURCE_ALIASES[id] || id;
}

function flatten(value) {
  if (value === undefined || value === null) return '';
  if (typeof value === 'string') return value;
  if (typeof value === 'number' || typeof value === 'boolean') return String(value);
  if (Array.isArray(value)) return value.map(flatten).join(' ');
  if (typeof value === 'object') return Object.entries(value).map(([key, val]) => `${key} ${flatten(val)}`).join(' ');
  return String(value);
}

function values(value) {
  if (value === undefined || value === null || value === '') return [];
  if (Array.isArray(value)) return value.flatMap(values);
  if (typeof value === 'object') {
    const preferred = ['niveau', 'statut', 'confiance', 'value', 'id', 'name', 'label'];
    for (const key of preferred) {
      if (value[key] !== undefined) return values(value[key]);
    }
    return [];
  }
  return [String(value).trim()].filter(Boolean);
}

function uniq(input) {
  return [...new Set(values(input).filter(Boolean))];
}

function uniqMany(items) {
  return [...new Set(items.flatMap(values).filter(Boolean))];
}

function dataOf(record) {
  return record?.data || record?.summary_fields || {};
}

function valueAt(obj, path) {
  let cursor = obj;
  for (const part of path.split('.')) {
    if (!cursor || typeof cursor !== 'object' || !(part in cursor)) return '';
    cursor = cursor[part];
  }
  return cursor;
}

function titleOf(record) {
  const data = dataOf(record);
  return data.titre || data.event || data.name || data.full_name || data.song || data.citation_originale || record.heading || record.id || '(sans titre)';
}

function sourceIdsOf(record) {
  const data = dataOf(record);
  const ids = [];
  ids.push(...values(data.source_id).map(normalizeSourceId));
  for (const source of values(data.sources)) {
    const match = String(source).match(/S\d{2}/);
    ids.push(normalizeSourceId(match ? match[0] : source));
  }
  const labelMatch = String(data.source_label || '').match(/S\d{2}/);
  if (labelMatch) ids.push(labelMatch[0]);
  const fallback = flatten(data).match(/\bS\d{2}\b/g) || [];
  ids.push(...fallback.map(normalizeSourceId));
  return [...new Set(ids.filter(Boolean))];
}

function chaptersOf(record) {
  const data = dataOf(record);
  const explicit = uniqMany([data.chapitres, data.chapters, data.chapitre]);
  const fallback = flatten(data).match(/Chapitre\s+\d+/g) || [];
  return [...new Set([...explicit, ...fallback])];
}

function typeOf(record) {
  return values(dataOf(record).type_unite)[0] || '';
}

function importanceOf(record) {
  const data = dataOf(record);
  return values(valueAt(data, 'importance.niveau') || data.importance)[0] || '';
}

function proofOf(record) {
  const data = dataOf(record);
  return values(valueAt(data, 'niveau_preuve.statut') || valueAt(data, 'niveau_preuve.confiance') || data.fiabilite || data.certainty)[0] || '';
}

function conceptsOf(record) {
  return uniq(dataOf(record).concepts);
}

function motifsOf(record) {
  return uniq(dataOf(record).motifs);
}

function sourceLabel(id) {
  const sourceId = normalizeSourceId(id);
  return state.sourceLabels[sourceId] || sourceId;
}

function compactSourceLabel(id, entry = {}) {
  if (entry.source_label) return entry.source_label;
  const author = entry.auteur || entry.author || '';
  const title = entry.titre || entry.title || '';
  const year = entry.annee || entry.source_year || '';
  const label = [author, title, year].filter(Boolean).join(', ');
  return label ? `${id} — ${label}` : (FALLBACK_SOURCES[id] || id);
}

function buildSourceLabels(registry) {
  state.sourceLabels = {...FALLBACK_SOURCES};
  for (const entry of registry || []) {
    const id = normalizeSourceId(entry.id || entry.source_id);
    if (!id) continue;
    state.sourceLabels[id] = compactSourceLabel(id, entry);
    for (const alias of values(entry.legacy_id || entry.legacy_ids)) state.sourceLabels[alias] = state.sourceLabels[id];
  }
}

function tokenize(query) {
  return (normalizeText(query).match(/[\wÀ-ÿ']+/gu) || [])
    .map(token => token.replace(/^'+|'+$/g, ''))
    .filter(token => token.length > 2 && !RAG2_STOPWORDS.has(token));
}

function recordText(record) {
  const data = dataOf(record);
  return [record.id, record.kind, record.heading, record.file, titleOf(record), data.source_label, sourceIdsOf(record).map(sourceLabel).join(' '), flatten(data)].join('\n');
}

function buildIndex() {
  state.index = state.records.map((record, order) => {
    const rawText = recordText(record);
    const tokenCounts = new Map();
    for (const token of tokenize(rawText)) tokenCounts.set(token, (tokenCounts.get(token) || 0) + 1);
    return {
      order,
      record,
      normalizedText: normalizeText(rawText),
      tokenCounts,
      sourceIds: sourceIdsOf(record),
      chapters: chaptersOf(record),
      type: typeOf(record),
      importance: importanceOf(record),
      proof: proofOf(record),
      concepts: conceptsOf(record),
      motifs: motifsOf(record)
    };
  });
}

function buildSources() {
  const grouped = new Map();
  for (const record of state.records) {
    for (const id of sourceIdsOf(record)) {
      if (!grouped.has(id)) grouped.set(id, {source_id: id, source_label: sourceLabel(id), records: [], counts: {}});
      const entry = grouped.get(id);
      entry.records.push(record);
      entry.counts[record.kind] = (entry.counts[record.kind] || 0) + 1;
    }
  }
  state.sources = [...grouped.values()].sort((a, b) => a.source_id.localeCompare(b.source_id, undefined, {numeric: true}));
}

function fillSelect(id, list, labelFn = value => value) {
  const select = $(id);
  if (!select) return;
  const first = select.querySelector('option')?.cloneNode(true);
  select.innerHTML = '';
  if (first) select.appendChild(first);
  for (const value of list) {
    const option = document.createElement('option');
    option.value = value;
    option.textContent = labelFn(value);
    select.appendChild(option);
  }
}

function shortLabel(value, max = 78) {
  const label = String(value || '');
  return label.length > max ? label.slice(0, max) + '…' : label;
}

function buildFilters() {
  const chapters = uniqMany(state.index.map(item => item.chapters)).sort((a, b) => a.localeCompare(b, undefined, {numeric: true}));
  const sources = uniqMany([state.sources.map(source => source.source_id), state.index.map(item => item.sourceIds)]).sort((a, b) => a.localeCompare(b, undefined, {numeric: true}));
  const types = uniqMany(state.index.map(item => item.type)).sort();
  const importances = uniqMany(state.index.map(item => item.importance)).sort();
  const proofs = uniqMany(state.index.map(item => item.proof)).sort();
  const concepts = uniqMany(state.index.map(item => item.concepts)).sort();
  const motifs = uniqMany(state.index.map(item => item.motifs)).sort();

  fillSelect('chapter-filter', chapters);
  fillSelect('source-filter', sources, id => `${id} — ${sourceLabel(id).replace(/^S\d+\s+—\s+/, '')}`);
  fillSelect('type-filter', types);
  fillSelect('importance-filter', importances);
  fillSelect('proof-filter', proofs);
  fillSelect('concept-filter', concepts, shortLabel);
  fillSelect('motif-filter', motifs, shortLabel);

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

function activeFilters(filters) {
  return Object.values(filters).some(Boolean);
}

function itemMatches(item, filters) {
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

function scoreKind(kind) {
  return {atom: 1.25, quote: 1.2, chronology: 1.1, concept: 1.05, myth: 1.05, motif: 1.05}[kind] || 1;
}

function scoreItem(item, terms, phrase, filters) {
  let score = phrase.length >= 4 && item.normalizedText.includes(phrase) ? 25 : 0;
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
  if (item.record.id && normalizeText(item.record.id).includes(phrase)) score += 20;
  if (activeFilters(filters)) score += 5;
  return {score: Math.round(score * scoreKind(item.record.kind)), details};
}

function search(query, filters) {
  const terms = uniq(tokenize(query));
  const phrase = normalizeText(query).trim();
  const filterOnly = !terms.length && phrase.length < 3 && activeFilters(filters);
  if (!filterOnly && !terms.length && phrase.length < 3) return [];

  const results = [];
  for (const item of state.index) {
    if (!itemMatches(item, filters)) continue;
    const scored = filterOnly ? {score: 1, details: ['filtre']} : scoreItem(item, terms, phrase, filters);
    if (scored.score > 0) results.push({score: scored.score, record: summarize(item.record, scored.details.join(', ')), order: item.order});
  }
  return results.sort((a, b) => (b.score - a.score) || (a.order - b.order));
}

function summarize(record, scoreDetails = '') {
  const data = dataOf(record);
  const sourceId = normalizeSourceId(data.source_id || sourceIdsOf(record)[0] || '');
  return {
    id: record.id,
    kind: record.kind,
    file: record.file,
    heading: record.heading,
    summary_fields: Object.fromEntries(Object.entries({
      titre: data.titre || titleOf(record),
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

function renderResults(results, perPage = 10) {
  state.results = Array.isArray(results) ? results : [];
  state.perPage = Number(perPage) || 10;
  state.page = 1;
  renderPage();
}

function renderPage() {
  const results = $('results');
  const meta = $('results-meta');
  const template = $('result-template');
  const pagination = $('pagination');
  if (!results || !meta || !template || !pagination) return;
  results.innerHTML = '';
  pagination.innerHTML = '';
  const total = state.results.length;
  const pages = Math.ceil(total / state.perPage) || 1;
  const start = (state.page - 1) * state.perPage;
  const pageItems = state.results.slice(start, start + state.perPage);
  meta.textContent = `${total} résultat(s) · page ${state.page}/${pages}`;

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
    for (const [key, value] of Object.entries(item.record.summary_fields || {})) {
      if (value === undefined || value === null || value === '') continue;
      const dt = document.createElement('dt');
      dt.textContent = key;
      const dd = document.createElement('dd');
      dd.textContent = typeof value === 'object' ? JSON.stringify(value, null, 2) : value;
      fields.appendChild(dt);
      fields.appendChild(dd);
    }
    results.appendChild(node);
  }

  if (pages > 1) {
    const makeButton = (label, page, disabled = false, active = false) => {
      const button = document.createElement('button');
      button.textContent = label;
      button.disabled = disabled;
      if (active) button.classList.add('active');
      button.addEventListener('click', () => { state.page = page; renderPage(); });
      return button;
    };
    pagination.appendChild(makeButton('←', Math.max(1, state.page - 1), state.page === 1));
    for (let page = Math.max(1, state.page - 3); page <= Math.min(pages, state.page + 3); page += 1) pagination.appendChild(makeButton(String(page), page, false, page === state.page));
    pagination.appendChild(makeButton('→', Math.min(pages, state.page + 1), state.page === pages));
  }
}

function filterLabel(filters) {
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
  if ($('results-title')) $('results-title').textContent = filterLabel(filters) || 'Résultats';
  if ($('results')) $('results').innerHTML = '<div class="status-card">Recherche en cours…</div>';
  renderResults(search(query, filters), $('top')?.value || 10);
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
      if ($('source-filter')) $('source-filter').value = source.source_id;
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

function resetFilters() {
  for (const id of ['kind','chapter-filter','source-filter','type-filter','importance-filter','proof-filter','concept-filter','motif-filter']) if ($(id)) $(id).value = '';
  if ($('query')) $('query').value = '';
  if ($('results')) $('results').innerHTML = '';
  if ($('results-meta')) $('results-meta').textContent = '';
  if ($('pagination')) $('pagination').innerHTML = '';
  if ($('results-title')) $('results-title').textContent = 'Résultats';
}

function bindUi() {
  const form = $('search-form');
  if (form) form.addEventListener('submit', event => { event.preventDefault(); performSearch(); });
  if ($('reset-filters')) $('reset-filters').addEventListener('click', resetFilters);
  for (const id of ['kind','chapter-filter','source-filter','type-filter','importance-filter','proof-filter','concept-filter','motif-filter','top']) {
    if ($(id)) $(id).addEventListener('change', () => {
      if (($('query')?.value || '').trim() || activeFilters(currentFilters())) performSearch();
    });
  }
  for (const button of document.querySelectorAll('.example-query')) {
    button.addEventListener('click', () => {
      if ($('query')) $('query').value = button.dataset.query || '';
      performSearch();
    });
  }
}

async function initRag2() {
  const card = $('status-card');
  try {
    const [records, registry] = await Promise.all([
      loadJson('../../exports/generated/all_records.json', []),
      loadJson('../../data/registre.json', [])
    ]);
    buildSourceLabels(registry || []);
    state.records = Array.isArray(records) ? records : [];
    buildIndex();
    buildSources();
    buildFilters();
    renderSources();
    bindUi();
    const counts = {};
    for (const record of state.records) counts[record.kind || 'unknown'] = (counts[record.kind || 'unknown'] || 0) + 1;
    const summary = Object.entries(counts).sort().map(([kind, count]) => `${kind}: ${count}`).join(' · ');
    if (card) card.textContent = `RAG 2 chargé · ${state.records.length} enregistrements · ${summary} · filtres ${card.dataset.filters || ''}`;
  } catch (error) {
    console.error(error);
    if (card) card.textContent = `Erreur : ${error.message}`;
  }
}

window.rag2 = {state, search, currentFilters, performSearch};
initRag2();
