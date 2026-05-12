const STOPWORDS = new Set([
  'a','an','and','are','as','at','be','by','for','from','in','is','it','of','on','or','that','the','to','with',
  'au','aux','ce','ces','dans','de','des','du','elle','en','et','il','la','le','les','pour','que','qui','sur','un','une',
  'avec','comme','par','plus','son','sa','ses','leur','leurs','est','sont','être','etre','fait','faites'
]);

const TOKEN_RE = /[\wÀ-ÿ']+/gu;
const SOURCE_ID_ALIASES = {'S-BROLL-JOY-001':'S68','S20':'S72','S35':'S41','S37':'S45','S41-HIST':'S73'};
const FALLBACK_SOURCE_LABELS = {
  S01:'S01 — Blakeley & Evans, The Regeneration of East Manchester, 2013',
  S02:'S02 — Sueur, Villes du futur, futur des villes, 2011',
  S03:'S03 — Demographia, England Largest Cities, s.d.',
  S04:'S04 — Kidd, Manchester: A History, 2006',
  S05:'S05 — Jeffery, Tufail & Jackson, Policing and the Reproduction of Local Social Order, 2015',
  S06:'S06 — Carter, Youth, race and the inner-city estate, 2023',
  S41:'S41 — Hook, Unknown Pleasures, 2012',
  S45:'S45 — Curtis, Touching from a Distance, 1995',
  S46:'S46 — Johnson, An Ideal for Living, 1984',
  S47:'S47 — West, Joy Division, 1984',
  S68:'S68 — Broll, Joy Division, 1988',
  S69:'S69 — Greig & Strong, But We Remember When We Were Young, 2014',
  S70:'S70 — Suatoni, Dal cuore della città / From the Centre of the City, 1990',
  S71:'S71 — Flowers, Dreams Never End, 1995/2012',
  S72:'S72 — Reynolds, Rip It Up and Start Again, 2005/2006',
  S73:'S73 — Blue Orchids, entrée historique à consolider, s.d.',
  S74:'S74 — Middles, From Joy Division to New Order, 1996'
};

let ALL_RECORDS = [];
let SEARCH_INDEX = [];
let SOURCES_INDEX = [];
let SOURCE_LABELS = {};
let LAST_RESULTS = [];
let CURRENT_PAGE = 1;
let RESULTS_PER_PAGE = 10;

function $(id) {
  return document.getElementById(id);
}

function showError(message, error = null) {
  console.error(message, error || '');
  const results = $('results');
  const meta = $('results-meta');
  if (meta) meta.textContent = 'Erreur de rendu';
  if (results) {
    results.innerHTML = `<div class="status-card"><strong>Erreur RAG 1</strong><br>${String(message)}${error ? `<br><code>${String(error.message || error)}</code>` : ''}</div>`;
  }
}

window.addEventListener('error', event => {
  showError('Erreur JavaScript dans le RAG Studio.', event.error || event.message);
});

window.addEventListener('unhandledrejection', event => {
  showError('Promesse rejetée dans le RAG Studio.', event.reason);
});

function normalizeSourceId(id) {
  return SOURCE_ID_ALIASES[id] || id;
}

function normalizeText(value) {
  return String(value || '')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase();
}

function flatten(value) {
  if (value === null || value === undefined) return '';
  if (typeof value === 'string') return value;
  if (typeof value === 'number' || typeof value === 'boolean') return String(value);
  if (Array.isArray(value)) return value.map(flatten).join(' ');
  if (typeof value === 'object') return Object.entries(value).map(([k, v]) => `${k} ${flatten(v)}`).join(' ');
  return String(value);
}

function tokenize(input) {
  return (normalizeText(input).match(TOKEN_RE) || [])
    .map(token => token.replace(/^'+|'+$/g, ''))
    .filter(token => token.length > 2 && !STOPWORDS.has(token));
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function compactAuthor(author) {
  return String(author || '')
    .replace('Peter Hook', 'Hook')
    .replace('Deborah Curtis', 'Curtis')
    .replace('Mike West', 'West')
    .replace('Marco Broll', 'Broll')
    .replace('Mark Johnson', 'Johnson')
    .slice(0, 40);
}

function compactTitle(title) {
  return String(title || '')
    .replace('Unknown Pleasures: Inside Joy Division', 'Unknown Pleasures')
    .replace('Touching from a Distance: Ian Curtis and Joy Division', 'Touching from a Distance')
    .replace('An Ideal for Living: An History of Joy Division', 'An Ideal for Living')
    .slice(0, 70);
}

function makeSourceLabel(id, data = {}) {
  const normalized = normalizeSourceId(id);
  if (data.source_label) return data.source_label;
  const author = compactAuthor(data.auteur || data.author);
  const title = compactTitle(data.titre || data.title);
  const year = data.annee || data.source_year || 's.d.';
  const detail = [author, title, year].filter(Boolean).join(', ');
  return detail ? `${normalized} — ${detail}` : (FALLBACK_SOURCE_LABELS[normalized] || normalized);
}

function buildSourceLabels(registry, records) {
  const labels = {...FALLBACK_SOURCE_LABELS};
  registry.forEach(entry => {
    const id = normalizeSourceId(entry.id || entry.source_id);
    if (!id) return;
    labels[id] = makeSourceLabel(id, entry);
    const aliases = Array.isArray(entry.legacy_id) ? entry.legacy_id : (entry.legacy_id ? [entry.legacy_id] : []);
    aliases.forEach(alias => { labels[alias] = labels[id]; });
  });
  records.forEach(record => {
    const data = record.data || {};
    const ids = [];
    if (data.source_id) ids.push(data.source_id);
    if (Array.isArray(data.sources)) ids.push(...data.sources);
    ids.forEach(raw => {
      const id = normalizeSourceId(raw);
      if (id && !labels[id]) labels[id] = makeSourceLabel(id, data);
    });
  });
  return labels;
}

function sourceLabel(sourceId) {
  const normalized = normalizeSourceId(sourceId);
  return SOURCE_LABELS[normalized] || SOURCE_LABELS[sourceId] || normalized || '';
}

function stripMd(value) {
  return String(value || '')
    .trim()
    .replace(/^«\s*/, '')
    .replace(/\s*»$/, '')
    .replace(/`/g, '')
    .replace(/<br\s*\/?>/gi, ' | ');
}

function splitTableRow(line) {
  return line.trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map(stripMd);
}

function inferSourceId(id, sourceCell) {
  const direct = String(id || '').match(/^(S\d{2})-Q\d+/);
  if (direct) return normalizeSourceId(direct[1]);
  const fromSource = String(sourceCell || '').match(/S\d{2}(?:-HIST)?/);
  return fromSource ? normalizeSourceId(fromSource[0]) : '';
}

async function loadJson(path, fallback) {
  try {
    const response = await fetch(path, {cache: 'no-store'});
    if (!response.ok) throw new Error(`${path} ${response.status}`);
    return await response.json();
  } catch (error) {
    console.warn('Fallback', path, error);
    return fallback || [];
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

function parseConsolidatedQuotesMarkdown(markdown) {
  const rows = [];
  const lines = String(markdown || '').split(/\r?\n/);
  let mode = '';

  for (const line of lines) {
    if (line.startsWith('## 1.1.')) { mode = 'historical'; continue; }
    if (line.startsWith('## 2.')) { mode = 'atomized'; continue; }
    if (!line.trim().startsWith('|') || line.includes('---')) continue;

    const cells = splitTableRow(line);
    if (!cells.length || /^ID/.test(cells[0]) || /^id$/i.test(cells[0])) continue;

    if (mode === 'historical' && cells.length >= 5) {
      const [id, source, type, entry, status] = cells;
      const sourceId = inferSourceId(id, source);
      rows.push({kind: 'quote', id, file: 'registers/quotes/master_quotes.md', heading: 'citation historique consolidée', data: {id, source_id: sourceId, source_label: sourceLabel(sourceId), citation_originale: entry, type_citation: type, statut_consolidation: status, statut_verification: status, chapitres: ['Chapitre 1'], source_origin: ['registre historique', 'master_quotes.md']}});
    } else if (mode === 'atomized' && cells.length >= 4) {
      const [id, citation, status, usage] = cells;
      const sourceId = inferSourceId(id, '');
      rows.push({kind: 'quote', id, file: 'registers/quotes/master_quotes.md', heading: 'citation atomisée consolidée', data: {id, source_id: sourceId, source_label: sourceLabel(sourceId), citation_originale: citation, usage_recommande: usage, statut_consolidation: status, statut_verification: status, source_origin: ['atomisation', 'master_quotes.md']}});
    }
  }
  return rows;
}

function mergeConsolidatedQuotes(records, consolidated) {
  const existing = new Set(records.map(record => record.id));
  return records.concat(consolidated.filter(record => !existing.has(record.id)));
}

function sourceIdsForRecord(record) {
  const ids = [];
  const data = record.data || {};
  if (data.source_id) ids.push(normalizeSourceId(data.source_id));
  if (Array.isArray(data.sources)) {
    for (const source of data.sources) {
      if (typeof source === 'string' && /^S(\d+|-[A-Z])/.test(source)) ids.push(normalizeSourceId(source));
    }
  }
  return unique(ids);
}

function chaptersForRecord(record) {
  const data = record.data || {};
  return unique([...(Array.isArray(data.chapitres) ? data.chapitres : []), ...(Array.isArray(data.chapters) ? data.chapters : [])].map(String));
}

function recordTitle(record) {
  const data = record.data || {};
  return data.titre || data.event || data.name || data.full_name || data.song || data.citation_originale || record.heading || record.id || '(sans titre)';
}

function recordTextParts(record) {
  const data = record.data || {};
  return [record.id || '', record.kind || '', record.heading || '', record.file || '', recordTitle(record), data.source_label || '', sourceIdsForRecord(record).map(sourceLabel).join(' '), flatten(data)];
}

function buildSearchIndex(records) {
  SEARCH_INDEX = records.map((record, order) => {
    const rawText = recordTextParts(record).join('\n');
    const normalizedText = normalizeText(rawText);
    const tokens = tokenize(rawText);
    const tokenCounts = new Map();
    tokens.forEach(token => tokenCounts.set(token, (tokenCounts.get(token) || 0) + 1));
    return {order, record, rawText, normalizedText, tokens, tokenCounts, sourceIds: sourceIdsForRecord(record), chapters: chaptersForRecord(record)};
  });
}

function conciseRecord(record, scoreDetails = null) {
  const data = record.data || {};
  const sourceId = data.source_id ? normalizeSourceId(data.source_id) : data.source_id;
  const sources = Array.isArray(data.sources) ? data.sources.map(normalizeSourceId) : data.sources;
  const sourceTitles = Array.isArray(sources) ? sources.map(sourceLabel) : undefined;

  return {
    id: record.id,
    kind: record.kind,
    file: record.file,
    heading: record.heading,
    summary_fields: Object.fromEntries(Object.entries({
      titre: data.titre || recordTitle(record),
      source_id: sourceId,
      source_label: data.source_label || sourceLabel(sourceId),
      source_short_title: data.source_short_title,
      sources,
      source_titles: sourceTitles,
      auteur: data.auteur,
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
      usage_recommande: data.usage_recommande,
      statut_consolidation: data.statut_consolidation,
      song: data.song,
      themes: data.themes,
      name: data.name,
      role: data.role,
      date: data.date,
      event: data.event,
      certainty: data.certainty,
      score_details: scoreDetails
    }).filter(([, value]) => value !== undefined && value !== null && value !== ''))
  };
}

function buildSourcesIndex() {
  const grouped = new Map();
  for (const record of ALL_RECORDS) {
    for (const sourceId of sourceIdsForRecord(record)) {
      if (!grouped.has(sourceId)) grouped.set(sourceId, {source_id: sourceId, source_label: sourceLabel(sourceId), records: [], counts: {atom: 0, quote: 0, chronology: 0, person: 0, song: 0, concept: 0, myth: 0, motif: 0, source: 0, metadata: 0}});
      const entry = grouped.get(sourceId);
      entry.records.push(record);
      entry.counts[record.kind] = (entry.counts[record.kind] || 0) + 1;
    }
  }
  SOURCES_INDEX = [...grouped.values()].sort((a, b) => a.source_id.localeCompare(b.source_id, undefined, {numeric: true}));
}

function renderSources() {
  const container = $('sources-list');
  const count = $('sources-count');
  if (!container || !count) return;
  container.innerHTML = '';
  count.textContent = `${SOURCES_INDEX.length} source(s)`;
  for (const source of SOURCES_INDEX) {
    const wrapper = document.createElement('div');
    wrapper.className = 'source-entry';
    const button = document.createElement('button');
    button.innerHTML = `<div class="source-title">${source.source_label}</div><div class="source-meta">${source.counts.atom || 0} atomes · ${source.counts.quote || 0} citations · ${source.counts.chronology || 0} chronologies · ${source.records.length} enregistrements</div>`;
    button.addEventListener('click', () => openSource(source.source_id));
    wrapper.appendChild(button);
    container.appendChild(wrapper);
  }
}

function clearResults() {
  if ($('results')) $('results').innerHTML = '';
  if ($('results-meta')) $('results-meta').textContent = '';
  if ($('pagination')) $('pagination').innerHTML = '';
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

function renderPagination(totalPages) {
  const container = $('pagination');
  if (!container) return;
  container.innerHTML = '';
  if (totalPages <= 1) return;

  const makeButton = (label, page, disabled = false, active = false) => {
    const button = document.createElement('button');
    button.textContent = label;
    button.disabled = disabled;
    if (active) button.classList.add('active');
    button.addEventListener('click', () => { CURRENT_PAGE = page; renderCurrentPage(); });
    return button;
  };

  container.appendChild(makeButton('←', Math.max(1, CURRENT_PAGE - 1), CURRENT_PAGE === 1));
  const start = Math.max(1, CURRENT_PAGE - 3);
  const end = Math.min(totalPages, CURRENT_PAGE + 3);
  for (let page = start; page <= end; page += 1) container.appendChild(makeButton(String(page), page, false, page === CURRENT_PAGE));
  container.appendChild(makeButton('→', Math.min(totalPages, CURRENT_PAGE + 1), CURRENT_PAGE === totalPages));
}

function renderCurrentPage() {
  try {
    clearResults();
    const results = $('results');
    const meta = $('results-meta');
    const template = $('result-template');
    if (!results || !meta || !template) throw new Error('Élément HTML manquant : results, results-meta ou result-template.');

    const total = LAST_RESULTS.length;
    const totalPages = Math.ceil(total / RESULTS_PER_PAGE) || 1;
    const start = (CURRENT_PAGE - 1) * RESULTS_PER_PAGE;
    const pageResults = LAST_RESULTS.slice(start, start + RESULTS_PER_PAGE);
    meta.textContent = `${total} résultat(s) · page ${CURRENT_PAGE}/${totalPages}`;

    if (!pageResults.length) {
      const empty = document.createElement('div');
      empty.className = 'status-card';
      empty.textContent = 'Aucun résultat.';
      results.appendChild(empty);
      return;
    }

    for (const item of pageResults) {
      if (!item || !item.record) continue;
      const node = template.content.cloneNode(true);
      const kind = node.querySelector('.result-kind');
      const score = node.querySelector('.result-score');
      const title = node.querySelector('.result-title');
      const file = node.querySelector('.result-file');
      const fields = node.querySelector('.result-fields');
      if (kind) kind.textContent = item.record.kind || '';
      if (score) score.textContent = `score ${item.score}`;
      if (title) title.textContent = item.record.id || item.record.summary_fields?.titre || '(sans id)';
      if (file) file.textContent = item.record.file || '';
      for (const [key, value] of Object.entries(item.record.summary_fields || {})) addField(fields, key, value);
      results.appendChild(node);
    }
    renderPagination(totalPages);
  } catch (error) {
    showError('Erreur pendant le rendu des résultats.', error);
  }
}

function renderResults(scored, perPage = 10) {
  LAST_RESULTS = Array.isArray(scored) ? scored : [];
  RESULTS_PER_PAGE = Number(perPage) || 10;
  CURRENT_PAGE = 1;
  renderCurrentPage();
}

function exactPhraseBonus(normalizedText, normalizedQuery) {
  if (!normalizedQuery || normalizedQuery.length < 4) return 0;
  return normalizedText.includes(normalizedQuery) ? 25 : 0;
}

function kindWeight(kind) {
  return {atom: 1.25, quote: 1.2, chronology: 1.1, person: 1, song: 1, concept: 1.05, myth: 1.05, motif: 1.05}[kind] || 1;
}

function scoreIndexedRecord(indexed, terms, normalizedQuery) {
  let score = exactPhraseBonus(indexed.normalizedText, normalizedQuery);
  let matchedTerms = 0;
  const details = [];
  for (const term of terms) {
    const count = indexed.tokenCounts.get(term) || 0;
    const partial = count ? 0 : (indexed.normalizedText.includes(term) ? 1 : 0);
    const termScore = (count * 6) + (partial * 2);
    if (termScore > 0) {
      matchedTerms += 1;
      score += termScore;
      details.push(`${term}:${count || 'partial'}`);
    }
  }
  if (terms.length && matchedTerms === terms.length) score += 12;
  if (indexed.record.id && normalizeText(indexed.record.id).includes(normalizedQuery)) score += 20;
  return {score: Math.round(score * kindWeight(indexed.record.kind)), matchedTerms, details};
}

function scoreRecords(query, kind) {
  const terms = unique(tokenize(query));
  const normalizedQuery = normalizeText(query).trim();
  if (!terms.length && normalizedQuery.length < 3) return [];

  const results = [];
  for (const indexed of SEARCH_INDEX) {
    if (kind && indexed.record.kind !== kind) continue;
    const scored = scoreIndexedRecord(indexed, terms, normalizedQuery);
    if (scored.score > 0) results.push({score: scored.score, record: conciseRecord(indexed.record, scored.details.join(', ')), order: indexed.order});
  }
  return results.sort((a, b) => (b.score - a.score) || (a.order - b.order));
}

function openSource(sourceId) {
  const source = SOURCES_INDEX.find(item => item.source_id === sourceId);
  if (!source) return;
  $('results-title').textContent = source.source_label;
  renderResults(source.records.map((record, index) => ({score: 'source', record: conciseRecord(record), order: index})), $('top')?.value || 10);
}

async function performSearch(query, kind, top) {
  try {
    $('results-title').textContent = 'Résultats';
    $('results').innerHTML = '<div class="status-card">Recherche en cours…</div>';
    const scored = scoreRecords(query, kind);
    renderResults(scored, top);
  } catch (error) {
    showError('Erreur pendant la recherche.', error);
  }
}

async function loadCorpus() {
  const card = $('status-card');
  try {
    const [records, registry, quotesMd] = await Promise.all([
      loadJson('../../exports/generated/all_records.json', []),
      loadJson('../../data/registre.json', []),
      loadText('../../registers/quotes/master_quotes.md', '')
    ]);
    SOURCE_LABELS = buildSourceLabels(registry, records);
    ALL_RECORDS = mergeConsolidatedQuotes(records, parseConsolidatedQuotesMarkdown(quotesMd));
    buildSearchIndex(ALL_RECORDS);
    buildSourcesIndex();
    renderSources();
    const counts = {};
    for (const record of ALL_RECORDS) counts[record.kind || 'unknown'] = (counts[record.kind || 'unknown'] || 0) + 1;
    const summary = Object.entries(counts).sort().map(([kind, count]) => `${kind}: ${count}`).join(' · ');
    if (card) card.textContent = `RAG 1 lexical chargé · ${ALL_RECORDS.length} enregistrements · ${summary}`;
  } catch (error) {
    if (card) card.textContent = `Erreur : ${error.message}`;
  }
}

function bindExamples() {
  for (const button of document.querySelectorAll('.example-query')) {
    button.addEventListener('click', () => {
      const query = button.dataset.query;
      $('query').value = query;
      performSearch(query, '', $('top')?.value || 10);
    });
  }
}

function bindForm() {
  const form = $('search-form');
  if (!form) return;
  form.addEventListener('submit', async event => {
    event.preventDefault();
    const query = $('query').value.trim();
    const kind = $('kind').value;
    const top = $('top').value;
    if (!query) return;
    await performSearch(query, kind, top);
  });
}

window.scoreRecords = scoreRecords;
window.renderResults = renderResults;
window.performSearch = performSearch;

loadCorpus();
bindExamples();
bindForm();
