const statusEl = document.getElementById('status');
const listEl = document.getElementById('sources-list');
const detailEl = document.getElementById('source-detail');
const resultsMeta = document.getElementById('results-meta');
const searchInput = document.getElementById('search');
const yearFilter = document.getElementById('year-filter');
const statusFilter = document.getElementById('status-filter');
const densityFilter = document.getElementById('density-filter');
const resetButton = document.getElementById('reset-filters');
const downloadButton = document.getElementById('download-csv');

const T = value => value === null || value === undefined ? '' : String(value);
const A = value => Array.isArray(value) ? value : (value ? [value] : []);
const U = values => [...new Set(values.map(T).filter(Boolean))].sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));
const esc = value => T(value)
  .replace(/&/g, '&amp;')
  .replace(/</g, '&lt;')
  .replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;');

let profiles = [];
let filtered = [];
let activeId = '';

function generatedUrl(file) {
  return new URL('../../exports/generated/' + file, window.location.href);
}

async function loadGeneratedJSON(file) {
  const response = await fetch(generatedUrl(file), { cache: 'no-store' });
  if (!response.ok) throw new Error('Export statique ' + file + ' ' + response.status);
  return response.json();
}

function sourceKey(record) {
  const data = record && (record.data || record);
  return T(data && (data.source_id || data.id)) || T(record && record.id);
}

function normalizeChapter(value) {
  const text = T(value).trim();
  if (!text) return '';
  const match = /chapitre\s+(\d+)/i.exec(text);
  if (match) return 'Chapitre ' + match[1];
  return text.charAt(0).toUpperCase() + text.slice(1);
}

function sourceSortValue(id) {
  const match = /^S(\d+)$/.exec(T(id));
  return match ? Number(match[1]) : 10000;
}

function compareSources(a, b) {
  const rank = sourceSortValue(a.id) - sourceSortValue(b.id);
  if (rank) return rank;
  return a.id.localeCompare(b.id, undefined, { numeric: true });
}

function countMap(values) {
  const counter = new Map();
  values.forEach(value => {
    const key = T(value);
    if (key) counter.set(key, (counter.get(key) || 0) + 1);
  });
  return counter;
}

function topEntries(counter, limit = 10) {
  return [...counter.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], undefined, { numeric: true }))
    .slice(0, limit);
}

function recordLabel(index, id) {
  const record = index[id] || {};
  const data = record.data || {};
  return T(data.name)
    || T(data.label)
    || T(data.concept)
    || T(data.motif)
    || T(data.mythe)
    || T(data.titre)
    || T(data.song)
    || T(record.heading).replace(/^[^—]+—\s*/, '')
    || id;
}

function sourceTitle(source, records) {
  const first = records[0] && (records[0].data || records[0]);
  return T(source.titre) || T(first && first.titre) || T(source.source_label).replace(/^S\d+\s+—\s*/, '') || source.source_id;
}

function sourceAuthor(source, records) {
  const first = records[0] && (records[0].data || records[0]);
  return T(source.auteur) || T(first && first.auteur) || 'Auteur non renseigné';
}

function sourceYear(source, records) {
  const first = records[0] && (records[0].data || records[0]);
  return T(source.annee) || T(first && (first.annee || first.source_year)) || '';
}

function atomizationStatus(profile) {
  if (profile.atomCount && profile.quoteCount) return 'atomisée avec citations';
  if (profile.atomCount) return 'atomisée';
  if (profile.quoteCount) return 'citée sans atomes';
  if (profile.recordCount) return 'référencée';
  return 'non atomisée';
}

function importanceRank(atom) {
  const data = atom.data || {};
  const level = T(data.importance && data.importance.niveau || data.importance).toLowerCase();
  if (level.includes('critique')) return 0;
  if (level.includes('majeur')) return 1;
  if (level.includes('important')) return 2;
  return 5;
}

function buildProfiles(payload) {
  const { sources, sourceRecords, quotes, atoms, edges, index } = payload;
  const recordsBySource = new Map();
  sourceRecords.forEach(record => {
    const id = sourceKey(record);
    if (!id) return;
    if (!recordsBySource.has(id)) recordsBySource.set(id, []);
    recordsBySource.get(id).push(record);
  });

  const quotesBySource = new Map();
  quotes.forEach(record => {
    const data = record.data || {};
    const id = T(data.source_id);
    if (!id) return;
    if (!quotesBySource.has(id)) quotesBySource.set(id, []);
    quotesBySource.get(id).push(record);
  });

  const atomsBySource = new Map();
  atoms.forEach(record => {
    const data = record.data || {};
    const id = T(data.source_id);
    if (!id) return;
    if (!atomsBySource.has(id)) atomsBySource.set(id, []);
    atomsBySource.get(id).push(record);
  });

  const quoteToSource = new Map();
  const atomToSource = new Map();
  const quotePeople = new Map();
  const atomIndexes = new Map();

  edges.forEach(edge => {
    if (edge.relation_type === 'documented_by' && edge.source_kind === 'quote' && edge.target_kind === 'source') {
      quoteToSource.set(edge.source_id, edge.target_id);
    }
    if (edge.relation_type === 'documented_by' && edge.source_kind === 'atom' && edge.target_kind === 'source') {
      atomToSource.set(edge.source_id, edge.target_id);
    }
    if (edge.relation_type === 'attributed_to' && edge.source_kind === 'quote' && edge.target_kind === 'person') {
      if (!quotePeople.has(edge.source_id)) quotePeople.set(edge.source_id, []);
      quotePeople.get(edge.source_id).push(edge.target_id);
    }
    if (edge.relation_type === 'indexed_by' && edge.source_kind === 'atom') {
      if (!atomIndexes.has(edge.source_id)) atomIndexes.set(edge.source_id, []);
      atomIndexes.get(edge.source_id).push({ kind: edge.target_kind, id: edge.target_id });
    }
  });

  const edgeStats = new Map();
  function ensureEdgeStats(id) {
    if (!edgeStats.has(id)) {
      edgeStats.set(id, {
        quoteEdges: 0,
        atomEdges: 0,
        people: new Map(),
        concepts: new Map(),
        motifs: new Map(),
        myths: new Map()
      });
    }
    return edgeStats.get(id);
  }

  quoteToSource.forEach((sourceId, quoteId) => {
    const stats = ensureEdgeStats(sourceId);
    stats.quoteEdges += 1;
    A(quotePeople.get(quoteId)).forEach(personId => {
      stats.people.set(personId, (stats.people.get(personId) || 0) + 1);
    });
  });

  atomToSource.forEach((sourceId, atomId) => {
    const stats = ensureEdgeStats(sourceId);
    stats.atomEdges += 1;
    A(atomIndexes.get(atomId)).forEach(target => {
      const bucket = target.kind === 'concept' ? stats.concepts
        : target.kind === 'motif' ? stats.motifs
        : target.kind === 'myth' ? stats.myths
        : null;
      if (bucket) bucket.set(target.id, (bucket.get(target.id) || 0) + 1);
    });
  });

  return sources.map(source => {
    const id = T(source.source_id);
    const records = recordsBySource.get(id) || [];
    const sourceQuotes = quotesBySource.get(id) || [];
    const sourceAtoms = atomsBySource.get(id) || [];
    const graph = edgeStats.get(id) || {
      quoteEdges: 0,
      atomEdges: 0,
      people: new Map(),
      concepts: new Map(),
      motifs: new Map(),
      myths: new Map()
    };
    const chapters = new Set();
    sourceAtoms.forEach(atom => {
      const data = atom.data || {};
      A(data.usage_livre || data.chapters || data.chapitres).map(normalizeChapter).filter(Boolean).forEach(chapter => chapters.add(chapter));
    });
    records.forEach(record => {
      const data = record.data || {};
      A(data.chapitres || data.chapters).map(normalizeChapter).filter(Boolean).forEach(chapter => chapters.add(chapter));
    });
    const recordData = records.map(record => record.data || record);
    const statusValues = U(recordData.flatMap(data => [data.statut, data.nature]).filter(Boolean));
    return {
      id,
      title: sourceTitle(source, records),
      author: sourceAuthor(source, records),
      year: sourceYear(source, records),
      label: T(source.source_label) || id,
      records,
      recordData,
      recordCount: Number(source.records || records.length || 0),
      atomCount: Number(source.atoms || sourceAtoms.length || 0),
      quoteCount: Number(source.quotes || sourceQuotes.length || 0),
      chronologyCount: Number(source.chronology || 0),
      files: A(source.files),
      quotes: sourceQuotes,
      atoms: sourceAtoms,
      graph,
      chapters: [...chapters].sort((a, b) => a.localeCompare(b, undefined, { numeric: true })),
      statusValues,
      atomization: '',
      searchText: '',
      index
    };
  }).map(profile => {
    profile.atomization = atomizationStatus(profile);
    profile.searchText = [
      profile.id,
      profile.label,
      profile.title,
      profile.author,
      profile.year,
      profile.atomization,
      ...profile.statusValues,
      ...profile.chapters
    ].join(' ').toLowerCase();
    return profile;
  }).sort(compareSources);
}

function fillSelect(select, values, firstLabel) {
  const current = select.value;
  select.innerHTML = '<option value="">' + firstLabel + '</option>';
  values.forEach(value => {
    const option = document.createElement('option');
    option.value = value;
    option.textContent = value;
    select.appendChild(option);
  });
  if (values.includes(current)) select.value = current;
}

function hydrateFilters() {
  fillSelect(yearFilter, U(profiles.map(profile => profile.year).filter(Boolean)), 'Toutes');
  fillSelect(statusFilter, U(profiles.map(profile => profile.atomization)), 'Tous');
}

function matches(profile) {
  const query = searchInput.value.trim().toLowerCase();
  if (query && !profile.searchText.includes(query)) return false;
  if (yearFilter.value && profile.year !== yearFilter.value) return false;
  if (statusFilter.value && profile.atomization !== statusFilter.value) return false;
  if (densityFilter.value === 'quotes' && !profile.quoteCount) return false;
  if (densityFilter.value === 'atoms' && !profile.atomCount) return false;
  if (densityFilter.value === 'semantic' && !(profile.graph.concepts.size || profile.graph.motifs.size || profile.graph.myths.size)) return false;
  return true;
}

function applyFilters() {
  filtered = profiles.filter(matches);
  if (!filtered.some(profile => profile.id === activeId)) activeId = filtered[0] ? filtered[0].id : '';
  renderList();
  renderDetail();
}

function badge(label, className = '') {
  return '<span class="badge' + (className ? ' ' + className : '') + '">' + esc(label) + '</span>';
}

function countBadge(value, label) {
  return '<span class="badge badge--muted">' + esc(value) + ' ' + esc(label) + '</span>';
}

function renderList() {
  resultsMeta.textContent = filtered.length + ' source' + (filtered.length > 1 ? 's' : '');
  if (!filtered.length) {
    listEl.innerHTML = '<p class="source-detail__empty">Aucune source pour ces filtres.</p>';
    return;
  }
  listEl.innerHTML = filtered.map(profile => {
    const active = profile.id === activeId ? ' is-active' : '';
    return '<button type="button" class="source-row' + active + '" data-source-id="' + esc(profile.id) + '">'
      + '<span class="source-row__top"><span class="source-row__id">' + esc(profile.id) + '</span><span class="source-row__year">' + esc(profile.year || 'sans date') + '</span></span>'
      + '<span class="source-row__title">' + esc(profile.title) + '</span>'
      + '<span class="source-row__author">' + esc(profile.author) + '</span>'
      + '<span class="source-row__counts">'
      + countBadge(profile.quoteCount, 'cit.')
      + countBadge(profile.atomCount, 'atomes')
      + countBadge(profile.graph.concepts.size, 'concepts')
      + countBadge(profile.graph.motifs.size, 'motifs')
      + countBadge(profile.graph.myths.size, 'mythes')
      + '</span>'
      + '</button>';
  }).join('');
}

function sourceById(id) {
  return profiles.find(profile => profile.id === id);
}

function firstData(profile, keys) {
  for (const record of profile.recordData) {
    for (const key of keys) {
      const value = record[key];
      if (value) return Array.isArray(value) ? value.join(', ') : T(value);
    }
  }
  return '';
}

function fact(label, value) {
  if (!T(value)) return '';
  return '<div class="source-fact"><span>' + esc(label) + '</span><strong>' + esc(value) + '</strong></div>';
}

function countCard(value, label) {
  return '<div class="source-count"><strong>' + esc(value) + '</strong><span>' + esc(label) + '</span></div>';
}

function graphCoverage(profile) {
  const direct = [];
  if (profile.graph.quoteEdges) direct.push(profile.graph.quoteEdges + ' citation(s) reliée(s)');
  if (profile.graph.atomEdges) direct.push(profile.graph.atomEdges + ' atome(s) relié(s)');
  if (profile.graph.concepts.size || profile.graph.motifs.size || profile.graph.myths.size) {
    direct.push('liens sémantiques disponibles');
  }
  return direct.length ? direct.join(' · ') : 'source non encore reliée par le graphe public';
}

function section(title, html) {
  return '<section class="source-section"><h3>' + esc(title) + '</h3>' + html + '</section>';
}

function renderQuotes(profile) {
  const quotes = profile.quotes.slice().sort((a, b) => T(a.id).localeCompare(T(b.id), undefined, { numeric: true })).slice(0, 8);
  if (!quotes.length) return '<p class="source-note">Aucune citation publique associée à cette source.</p>';
  const items = quotes.map(quote => {
    const data = quote.data || {};
    const text = T(data.texte || data.citation_originale || data.citation || '(non transcrit)');
    const meta = [quote.id, data.locuteur, data.type, data.page_pdf ? 'p. ' + data.page_pdf : '', data.statut_verification].filter(Boolean).join(' · ');
    return '<li class="source-item"><p class="source-item__title">' + esc(meta) + '</p><blockquote>' + esc(text) + '</blockquote></li>';
  }).join('');
  const more = profile.quotes.length > quotes.length ? '<p class="source-more">+' + (profile.quotes.length - quotes.length) + ' citation(s) supplémentaires dans les données.</p>' : '';
  return '<ul class="source-list">' + items + '</ul>' + more;
}

function renderAtoms(profile) {
  const atoms = profile.atoms.slice()
    .sort((a, b) => importanceRank(a) - importanceRank(b) || T(a.id).localeCompare(T(b.id), undefined, { numeric: true }))
    .slice(0, 10);
  if (!atoms.length) return '<p class="source-note">Aucun atome public associé à cette source.</p>';
  const items = atoms.map(atom => {
    const data = atom.data || {};
    const title = T(data.titre || atom.heading || atom.id);
    const importance = T(data.importance && data.importance.niveau || data.importance);
    const proof = T(data.niveau_preuve && data.niveau_preuve.statut || data.niveau_preuve);
    const meta = [atom.id, importance, proof].filter(Boolean).join(' · ');
    return '<li class="source-item"><p class="source-item__title">' + esc(title) + '</p><p class="source-item__text">' + esc(meta) + '</p></li>';
  }).join('');
  const more = profile.atoms.length > atoms.length ? '<p class="source-more">+' + (profile.atoms.length - atoms.length) + ' atome(s) supplémentaires dans les données.</p>' : '';
  return '<ul class="source-list">' + items + '</ul>' + more;
}

function renderTopGraph(profile, bucket, emptyText) {
  const entries = topEntries(bucket, 12);
  if (!entries.length) return '<p class="source-note">' + esc(emptyText) + '</p>';
  return '<div class="badges">' + entries.map(([id, count]) => badge(recordLabel(profile.index, id) + ' (' + count + ')')).join('') + '</div>';
}

function renderChapters(profile) {
  if (!profile.chapters.length) return '<p class="source-note">Aucun chapitre public calculé pour cette source.</p>';
  return '<div class="badges">' + profile.chapters.map(chapter => badge(chapter)).join('') + '</div>';
}

function renderDetail() {
  const profile = sourceById(activeId);
  if (!profile) {
    detailEl.innerHTML = '<p class="source-detail__empty">Choisissez une source dans la liste.</p>';
    return;
  }
  const reference = firstData(profile, ['reference_complete', 'source_short_title', 'source_label']) || profile.label;
  const nature = firstData(profile, ['nature', 'type_unite']);
  const status = firstData(profile, ['statut']);
  const reliability = firstData(profile, ['fiabilite']);
  const bibliography = '<div class="source-grid">'
    + fact('Auteur', profile.author)
    + fact('Titre', profile.title)
    + fact('Année', profile.year)
    + fact('Nature', nature)
    + fact('Statut', status)
    + fact('Fiabilité', reliability)
    + '</div>'
    + '<p class="source-item__text">' + esc(reference) + '</p>';
  detailEl.innerHTML = '<div class="source-detail__header">'
    + '<p class="source-detail__eyebrow">' + esc(profile.id) + '</p>'
    + '<h2>' + esc(profile.title) + '</h2>'
    + '<p class="source-detail__meta">' + esc([profile.author, profile.year, profile.atomization].filter(Boolean).join(' · ')) + '</p>'
    + '<div class="source-counts">'
    + countCard(profile.quoteCount, 'citations')
    + countCard(profile.atomCount, 'atomes')
    + countCard(profile.graph.concepts.size, 'concepts')
    + countCard(profile.graph.motifs.size, 'motifs')
    + countCard(profile.graph.myths.size, 'mythes')
    + '</div>'
    + '</div>'
    + section('Notice bibliographique', bibliography)
    + section('Statut d’atomisation', '<p>' + esc(profile.atomization) + '</p><p class="source-item__text">' + esc(graphCoverage(profile)) + '</p>')
    + section('Citations associées', renderQuotes(profile))
    + section('Atomes structurants', renderAtoms(profile))
    + section('Concepts associés', renderTopGraph(profile, profile.graph.concepts, 'Aucun concept relié par le graphe public pour cette source.'))
    + section('Motifs associés', renderTopGraph(profile, profile.graph.motifs, 'Aucun motif relié par le graphe public pour cette source.'))
    + section('Mythes associés', renderTopGraph(profile, profile.graph.myths, 'Aucun mythe relié par le graphe public pour cette source.'))
    + section('Personnes les plus citées', renderTopGraph(profile, profile.graph.people, 'Aucune personne attribuée via les citations de cette source.'))
    + section('Chapitres concernés', renderChapters(profile));
}

function exportCSV() {
  const headers = ['source_id', 'titre', 'auteur', 'annee', 'statut_atomisation', 'citations', 'atomes', 'concepts', 'motifs', 'mythes', 'chapitres'];
  const rows = filtered.map(profile => [
    profile.id,
    profile.title,
    profile.author,
    profile.year,
    profile.atomization,
    profile.quoteCount,
    profile.atomCount,
    profile.graph.concepts.size,
    profile.graph.motifs.size,
    profile.graph.myths.size,
    profile.chapters.join(' | ')
  ]);
  const csv = [headers, ...rows].map(row => row.map(value => '"' + T(value).replace(/"/g, '""') + '"').join(',')).join('\n');
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'joy_division_sources_register.csv';
  link.click();
  URL.revokeObjectURL(link.href);
}

async function loadSources() {
  try {
    const [sources, sourceRecords, quotes, atoms, edgePayload, index] = await Promise.all([
      loadGeneratedJSON('sources.json'),
      loadGeneratedJSON('source_records.json'),
      loadGeneratedJSON('quotes.json'),
      loadGeneratedJSON('atoms.json'),
      loadGeneratedJSON('edges.json'),
      loadGeneratedJSON('index_by_id.json')
    ]);
    profiles = buildProfiles({
      sources: Array.isArray(sources) ? sources : [],
      sourceRecords: Array.isArray(sourceRecords) ? sourceRecords : [],
      quotes: Array.isArray(quotes) ? quotes : [],
      atoms: Array.isArray(atoms) ? atoms : [],
      edges: Array.isArray(edgePayload.edges) ? edgePayload.edges : [],
      index: index || {}
    });
    const requested = new URLSearchParams(window.location.search).get('source');
    activeId = profiles.some(profile => profile.id === requested) ? requested : (profiles[0] && profiles[0].id) || '';
    hydrateFilters();
    applyFilters();
    statusEl.textContent = profiles.length + ' source' + (profiles.length > 1 ? 's' : '') + ' chargée' + (profiles.length > 1 ? 's' : '') + ' depuis les exports publics.';
  } catch (error) {
    console.error(error);
    statusEl.textContent = 'Erreur lors du chargement du registre des sources : ' + error.message;
    detailEl.innerHTML = '<p class="source-detail__empty">Impossible de charger les exports publics.</p>';
  }
}

listEl.addEventListener('click', event => {
  const row = event.target.closest('[data-source-id]');
  if (!row) return;
  activeId = row.dataset.sourceId;
  const url = new URL(window.location.href);
  url.searchParams.set('source', activeId);
  window.history.replaceState({}, '', url);
  renderList();
  renderDetail();
});

[searchInput, yearFilter, statusFilter, densityFilter].forEach(element => {
  element.addEventListener('input', applyFilters);
});

resetButton.addEventListener('click', () => {
  searchInput.value = '';
  yearFilter.value = '';
  statusFilter.value = '';
  densityFilter.value = '';
  applyFilters();
});

downloadButton.addEventListener('click', exportCSV);

loadSources();
