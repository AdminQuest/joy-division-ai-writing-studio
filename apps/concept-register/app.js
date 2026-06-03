const listEl = document.getElementById('concepts-list');
const detailEl = document.getElementById('concept-detail');
const resultsMeta = document.getElementById('results-meta');
const statusCard = document.getElementById('status-card');
const searchInput = document.getElementById('search');
const sourceFilter = document.getElementById('source-filter');
const chapterFilter = document.getElementById('chapter-filter');
const typeField = document.getElementById('type-field');
const typeFilter = document.getElementById('type-filter');
const resetButton = document.getElementById('reset-filters');
const downloadButton = document.getElementById('download-csv');
const registerTitle = document.getElementById('register-title');
const registerSubtitle = document.getElementById('register-subtitle');
const registerNote = document.getElementById('register-note');
const resultsTitle = document.getElementById('results-title');

const T = value => value === null || value === undefined ? '' : String(value);
const A = value => Array.isArray(value) ? value : (value ? [value] : []);
const U = values => [...new Set(values.map(T).filter(Boolean))]
  .sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));
const esc = value => T(value)
  .replace(/&/g, '&amp;')
  .replace(/</g, '&lt;')
  .replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;');

const TYPE_LABELS = { concept: 'Concept', motif: 'Motif', myth: 'Mythe', mythe: 'Mythe' };
const URL_TYPE_ALIASES = { concept: 'concept', motif: 'motif', myth: 'myth', mythe: 'myth' };

const VIEW_LABELS = {
  all: {
    documentTitle: 'Registre des concepts, motifs et mythes — Joy Division',
    title: 'Registre des concepts, motifs et mythes',
    resultsTitle: 'Notions, motifs et mythes',
    singular: 'entrée',
    plural: 'entrées',
    exportName: 'joy_division_concepts_motifs_mythes_register.csv',
    subtitle: 'Entrées de lecture du corpus, enrichies par les sources, citations et points documentaires déjà reliés.',
    note: 'Cette vue réunit les notions critiques, motifs récurrents et mythes publics du corpus sans dupliquer les données.'
  },
  concept: {
    documentTitle: 'Registre des concepts — Joy Division',
    title: 'Registre des concepts',
    resultsTitle: 'Concepts',
    singular: 'concept',
    plural: 'concepts',
    exportName: 'joy_division_concepts_register.csv',
    subtitle: 'Une entrée publique pour comprendre comment plusieurs sources pensent le même objet.',
    note: 'Les fiches privilégient les sources, citations, points documentaires et relations utiles à la lecture du livre.'
  },
  motif: {
    documentTitle: 'Registre des motifs — Joy Division',
    title: 'Registre des motifs',
    resultsTitle: 'Motifs',
    singular: 'motif',
    plural: 'motifs',
    exportName: 'joy_division_motifs_register.csv',
    subtitle: 'Motifs récurrents et formes transversales observables dans le corpus public.',
    note: 'Les motifs sont reliés aux points documentaires et aux sources déjà présents dans le graphe public.'
  },
  myth: {
    documentTitle: 'Registre des mythes — Joy Division',
    title: 'Registre des mythes',
    resultsTitle: 'Mythes',
    singular: 'mythe',
    plural: 'mythes',
    exportName: 'joy_division_mythes_register.csv',
    subtitle: 'Récits, idées reçues et constructions critiques à examiner avec prudence documentaire.',
    note: 'Les mythes sont présentés comme des objets d’analyse, pas comme des conclusions automatiques.'
  }
};

let profiles = [];
let filtered = [];
let dedicatedType = '';
let activeId = '';
let sourceLabels = new Map();
let loadedIndex = {};

function generatedUrl(file) {
  return new URL('../../exports/generated/' + file, window.location.href);
}

async function loadGeneratedJSON(file) {
  const response = await fetch(generatedUrl(file), { cache: 'no-store' });
  if (!response.ok) throw new Error('Export statique ' + file + ' ' + response.status);
  return response.json();
}

function activeViewLabels(type) {
  return VIEW_LABELS[URL_TYPE_ALIASES[T(type).toLowerCase()]] || VIEW_LABELS.all;
}

function updateViewLabels(type) {
  const labels = activeViewLabels(type);
  const view = URL_TYPE_ALIASES[T(type).toLowerCase()] || 'all';
  document.title = labels.documentTitle;
  document.body.dataset.registerView = view;
  if (registerTitle) registerTitle.textContent = labels.title;
  if (registerSubtitle) registerSubtitle.textContent = labels.subtitle;
  if (resultsTitle) resultsTitle.textContent = labels.resultsTitle;
  if (registerNote) registerNote.textContent = labels.note;
  return labels;
}

function configureDedicatedMode(type) {
  dedicatedType = type || '';
  if (typeField) {
    if (dedicatedType) typeField.hidden = true;
    else typeField.removeAttribute('hidden');
  }
  if (typeFilter) typeFilter.disabled = !!dedicatedType;
}

function initialTypeFilter() {
  try {
    const raw = new URLSearchParams(window.location.search).get('type');
    return URL_TYPE_ALIASES[T(raw).toLowerCase()] || '';
  } catch (_) {
    return '';
  }
}

function cleanHeading(value) {
  return T(value).replace(/^[^—]+—\s*/, '').trim();
}

function sourceSortValue(id) {
  const match = /^S(\d+)$/.exec(T(id));
  return match ? Number(match[1]) : 10000;
}

function normalizeSourceId(value) {
  const text = T(value).trim();
  if (!text) return '';
  if (text === 'S-BROLL-JOY-001') return 'S68';
  const match = /^(S\d+)\b/.exec(text);
  return match ? match[1] : text;
}

function normalizeChapter(value) {
  const text = T(value).trim();
  if (!text) return '';
  const match = /chapitre\s+(\d+)/i.exec(text);
  if (match) return 'Chapitre ' + match[1];
  if (/^\d+$/.test(text)) return 'Chapitre ' + text;
  return text.charAt(0).toUpperCase() + text.slice(1);
}

function normalizeIdValue(value) {
  if (!value) return '';
  if (typeof value === 'object') return T(value.id || value.atom_id || value.source_id || value.target_id);
  return T(value).trim();
}

function normalizeLookupValue(value) {
  return T(value)
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/['’]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

function listFromFields(data, keys, normalizer = value => T(value).trim()) {
  const values = [];
  keys.forEach(key => {
    A(data && data[key]).forEach(value => {
      const clean = normalizer(normalizeIdValue(value));
      if (clean) values.push(clean);
    });
  });
  return U(values);
}

function recordId(record) {
  const data = record && (record.data || {});
  return T(record && (record.id || data.id));
}

function publicLabel(recordOrId, preferredKind = '') {
  const record = typeof recordOrId === 'string' ? loadedIndex[recordOrId] : recordOrId;
  const id = typeof recordOrId === 'string' ? recordOrId : recordId(recordOrId);
  const data = record && (record.data || {});
  if (preferredKind === 'concept') {
    return T(data.nom)
      || T(data.label)
      || T(data.name)
      || T(data.concept)
      || T(data.titre)
      || cleanHeading(record && record.heading)
      || id;
  }
  return T(data.nom)
    || T(data.label)
    || T(data.name)
    || T(data.concept)
    || T(data.motif)
    || T(data.mythe)
    || T(data.titre)
    || cleanHeading(record && record.heading)
    || id;
}

function definitionOf(record) {
  const data = record && (record.data || {});
  return T(data.definition || data.description || data.fonction_argumentative || data.position || data.correction);
}

function summaryOf(record) {
  const data = record && (record.data || {});
  return T(data.resume || data.résumé || data.synthese || data.usage_repo || data.statut || data.prudence);
}

function sourceLabel(id) {
  return sourceLabels.get(id) || id;
}

function makeCountMap() {
  return new Map();
}

function increment(map, id, amount = 1) {
  if (!id) return;
  map.set(id, (map.get(id) || 0) + amount);
}

function topEntries(map, limit = 12) {
  return [...map.entries()]
    .sort((a, b) => b[1] - a[1] || publicLabel(a[0]).localeCompare(publicLabel(b[0]), undefined, { numeric: true }))
    .slice(0, limit);
}

function profileKey(kind, id) {
  return kind + ':' + id;
}

function semanticHref(kind, id = '') {
  if (kind === 'source') return '../source-register/' + (id ? '?source=' + encodeURIComponent(id) : '');
  if (kind === 'concept') return '../concept-register/?type=concept';
  if (kind === 'motif') return '../concept-register/?type=motif';
  if (kind === 'myth') return '../concept-register/?type=myth';
  return '';
}

function typeLabel(type) {
  return TYPE_LABELS[T(type).toLowerCase()] || T(type);
}

function addToMapSet(map, key, value) {
  if (!key || !value) return;
  if (!map.has(key)) map.set(key, new Set());
  map.get(key).add(value);
}

function buildIndexes(edges) {
  const targetAtoms = new Map();
  const atomSources = new Map();
  const atomTargets = new Map();
  const sourceQuotes = new Map();
  const quotePeople = new Map();

  edges.forEach(edge => {
    if (edge.relation_type === 'indexed_by' && edge.source_kind === 'atom') {
      addToMapSet(targetAtoms, profileKey(edge.target_kind, edge.target_id), edge.source_id);
      if (!atomTargets.has(edge.source_id)) {
        atomTargets.set(edge.source_id, { concept: new Set(), motif: new Set(), myth: new Set() });
      }
      const bucket = atomTargets.get(edge.source_id)[edge.target_kind];
      if (bucket) bucket.add(edge.target_id);
    }
    if (edge.relation_type === 'documented_by' && edge.source_kind === 'atom' && edge.target_kind === 'source') {
      addToMapSet(atomSources, edge.source_id, edge.target_id);
    }
    if (edge.relation_type === 'documented_by' && edge.source_kind === 'quote' && edge.target_kind === 'source') {
      addToMapSet(sourceQuotes, edge.target_id, edge.source_id);
    }
    if (edge.relation_type === 'attributed_to' && edge.source_kind === 'quote' && edge.target_kind === 'person') {
      addToMapSet(quotePeople, edge.source_id, edge.target_id);
    }
  });

  return { targetAtoms, atomSources, atomTargets, sourceQuotes, quotePeople };
}

function atomFieldKeys(kind) {
  if (kind === 'concept') return ['concepts', 'concepts_derives', 'related_concepts'];
  if (kind === 'motif') return ['motifs', 'motifs_derives', 'related_motifs'];
  if (kind === 'myth') return ['mythes', 'mythes_derives', 'related_mythes', 'myths', 'myths_derives', 'related_myths'];
  return [];
}

function atomReferenceKeys(kind, record) {
  const id = recordId(record);
  const label = publicLabel(record, kind);
  return U([
    id,
    label,
    normalizeLookupValue(id),
    normalizeLookupValue(label)
  ]);
}

function buildAtomReferenceIndex(atoms) {
  const referenceIndex = {
    concept: new Map(),
    motif: new Map(),
    myth: new Map()
  };

  atoms.forEach(atom => {
    const atomId = recordId(atom);
    if (!atomId) return;
    const data = atom.data || {};
    ['concept', 'motif', 'myth'].forEach(kind => {
      atomFieldKeys(kind).forEach(field => {
        A(data[field]).forEach(rawValue => {
          const value = normalizeIdValue(rawValue);
          if (!value) return;
          addToMapSet(referenceIndex[kind], value, atomId);
          addToMapSet(referenceIndex[kind], normalizeLookupValue(value), atomId);
        });
      });
    });
  });

  return referenceIndex;
}

function buildProfiles(payload) {
  const { concepts, atoms, quotes, sources, edges, index } = payload;
  loadedIndex = index || {};
  const edgeIndex = buildIndexes(edges);
  const atomReferenceIndex = buildAtomReferenceIndex(atoms);
  const atomById = new Map();
  const quoteById = new Map();
  const quoteSourceFallback = new Map();
  sourceLabels = new Map();

  sources.forEach(source => {
    const id = normalizeSourceId(source.source_id || source.id);
    if (!id) return;
    const title = T(source.titre) || T(source.source_label).replace(/^S\d+\s+—\s*/, '');
    const label = [title, source.auteur, source.annee].filter(Boolean).join(' — ') || id;
    sourceLabels.set(id, label);
  });

  atoms.forEach(atom => {
    const id = recordId(atom);
    if (id) atomById.set(id, atom);
  });

  quotes.forEach(quote => {
    const id = recordId(quote);
    const data = quote.data || {};
    if (!id) return;
    quoteById.set(id, quote);
    const sid = normalizeSourceId(data.source_id);
    if (sid) {
      if (!quoteSourceFallback.has(sid)) quoteSourceFallback.set(sid, new Set());
      quoteSourceFallback.get(sid).add(id);
    }
  });

  const semanticRecords = [];
  concepts.forEach(record => semanticRecords.push({ kind: 'concept', record }));
  Object.values(index || {}).forEach(record => {
    const kind = T(record && record.kind);
    const id = recordId(record);
    if ((kind === 'motif' || kind === 'myth') && id) semanticRecords.push({ kind, record });
  });

  const seen = new Set();
  return semanticRecords.map(({ kind, record }) => {
    const id = recordId(record);
    if (!id) return null;
    const key = profileKey(kind, id);
    if (seen.has(key)) return null;
    seen.add(key);
    return buildProfile({
      kind,
      record,
      atomById,
      quoteById,
      quoteSourceFallback,
      edgeIndex,
      atomReferenceIndex
    });
  }).filter(Boolean).sort((a, b) => {
    if (a.kind !== b.kind) return a.kind.localeCompare(b.kind);
    return a.label.localeCompare(b.label, undefined, { numeric: true });
  });
}

function buildProfile(context) {
  const { kind, record, atomById, quoteById, quoteSourceFallback, edgeIndex, atomReferenceIndex } = context;
  const data = record.data || {};
  const id = recordId(record);
  const directSources = listFromFields(data, ['sources', 'source_ids', 'source_id'], normalizeSourceId);
  const directChapters = listFromFields(data, ['chapitres', 'usage_chapitres'], normalizeChapter);
  const directAtoms = listFromFields(data, ['atomes', 'atomes_lies', 'related_atoms']);
  const graphAtoms = edgeIndex.targetAtoms.get(profileKey(kind, id)) || new Set();
  const atomFieldAtoms = new Set();
  atomReferenceKeys(kind, record).forEach(key => {
    const refs = atomReferenceIndex[kind] && atomReferenceIndex[kind].get(key);
    if (refs) refs.forEach(atomId => atomFieldAtoms.add(atomId));
  });
  const atomIds = new Set([...graphAtoms, ...directAtoms, ...atomFieldAtoms].filter(atomId => atomById.has(atomId)));
  const sourceIds = new Set(directSources);
  const chapters = new Set(directChapters);
  const motifCounts = makeCountMap();
  const mythCounts = makeCountMap();
  const quoteIds = new Set();
  const personCounts = makeCountMap();

  atomIds.forEach(atomId => {
    const atom = atomById.get(atomId);
    const atomData = atom.data || {};
    const atomSourceIds = edgeIndex.atomSources.get(atomId) || new Set();
    atomSourceIds.forEach(sourceId => sourceIds.add(sourceId));
    listFromFields(atomData, ['source_id'], normalizeSourceId).forEach(sourceId => sourceIds.add(sourceId));
    listFromFields(atomData, ['usage_livre', 'chapitres', 'chapters'], normalizeChapter).forEach(chapter => chapters.add(chapter));
    const targets = edgeIndex.atomTargets.get(atomId);
    if (targets) {
      targets.motif.forEach(motifId => increment(motifCounts, motifId));
      targets.myth.forEach(mythId => increment(mythCounts, mythId));
    }
  });

  sourceIds.forEach(sourceId => {
    const graphQuotes = edgeIndex.sourceQuotes.get(sourceId) || new Set();
    const fallbackQuotes = quoteSourceFallback.get(sourceId) || new Set();
    [...graphQuotes, ...fallbackQuotes].forEach(quoteId => quoteIds.add(quoteId));
  });

  quoteIds.forEach(quoteId => {
    const people = edgeIndex.quotePeople.get(quoteId) || new Set();
    people.forEach(personId => increment(personCounts, personId));
  });

  const atoms = [...atomIds].map(atomId => atomById.get(atomId)).filter(Boolean)
    .sort((a, b) => T(recordId(a)).localeCompare(recordId(b), undefined, { numeric: true }));
  const quotes = [...quoteIds].map(quoteId => quoteById.get(quoteId)).filter(Boolean)
    .sort((a, b) => T(recordId(a)).localeCompare(recordId(b), undefined, { numeric: true }));
  const graphEnriched = graphAtoms.size > 0;
  const fallbackEnriched = !graphEnriched && (
    directAtoms.length > 0
    || directSources.length > 0
    || directChapters.length > 0
  );
  const definition = definitionOf(record);
  const summary = summaryOf(record);
  const label = publicLabel(record, kind);
  const searchText = [
    label,
    definition,
    summary,
    ...sourceIds,
    ...[...sourceIds].map(sourceLabel),
    ...chapters,
    ...atoms.map(atom => publicLabel(atom)),
    ...topEntries(motifCounts, 30).map(([motifId]) => publicLabel(motifId)),
    ...topEntries(mythCounts, 30).map(([mythId]) => publicLabel(mythId))
  ].join(' ').toLowerCase();

  return {
    id,
    kind,
    label,
    definition,
    summary,
    record,
    atoms,
    atomCount: atomIds.size,
    sourceIds: [...sourceIds].filter(Boolean).sort((a, b) => sourceSortValue(a) - sourceSortValue(b) || a.localeCompare(b)),
    chapters: [...chapters].filter(Boolean).sort((a, b) => a.localeCompare(b, undefined, { numeric: true })),
    quotes,
    motifCounts,
    mythCounts,
    personCounts,
    graphEnriched,
    fallbackEnriched,
    searchText
  };
}

function fillSelect(select, values, firstLabel, labeler = value => value) {
  const current = select.value;
  select.innerHTML = '<option value="">' + firstLabel + '</option>';
  values.forEach(value => {
    const option = document.createElement('option');
    option.value = value;
    option.textContent = labeler(value);
    select.appendChild(option);
  });
  if (values.includes(current)) select.value = current;
}

function hydrateFilters() {
  const visible = dedicatedType ? profiles.filter(profile => profile.kind === dedicatedType) : profiles;
  fillSelect(sourceFilter, U(visible.flatMap(profile => profile.sourceIds)), 'Toutes', sourceLabel);
  fillSelect(chapterFilter, U(visible.flatMap(profile => profile.chapters)), 'Tous');
  fillSelect(typeFilter, U(profiles.map(profile => profile.kind)), 'Tous', typeLabel);
}

function matches(profile) {
  const query = searchInput.value.trim().toLowerCase();
  if (query && !profile.searchText.includes(query)) return false;
  if (sourceFilter.value && !profile.sourceIds.includes(sourceFilter.value)) return false;
  if (chapterFilter.value && !profile.chapters.includes(chapterFilter.value)) return false;
  if (typeFilter.value && profile.kind !== typeFilter.value) return false;
  return true;
}

function applyFilters() {
  updateViewLabels(typeFilter.value);
  filtered = profiles.filter(matches);
  if (!filtered.some(profile => profile.id === activeId && profile.kind === activeKind())) {
    activeId = filtered[0] ? filtered[0].id : '';
  }
  renderList();
  renderDetail();
}

function activeKind() {
  const active = profiles.find(profile => profile.id === activeId && (!typeFilter.value || profile.kind === typeFilter.value));
  return active ? active.kind : typeFilter.value;
}

function countBadge(value, label) {
  return '<span class="count-badge"><strong>' + esc(value) + '</strong><span>' + esc(label) + '</span></span>';
}

function badge(label, href = '') {
  if (href) return '<a class="badge badge--link" href="' + esc(href) + '">' + esc(label) + '</a>';
  return '<span class="badge">' + esc(label) + '</span>';
}

function renderList() {
  const labels = activeViewLabels(typeFilter.value);
  const noun = filtered.length > 1 ? labels.plural : labels.singular;
  resultsMeta.textContent = filtered.length + ' ' + noun;
  statusCard.textContent = profiles.length + ' entrée' + (profiles.length > 1 ? 's' : '')
    + ' chargée' + (profiles.length > 1 ? 's' : '')
    + ' depuis les exports publics.';

  if (!filtered.length) {
    listEl.innerHTML = '<p class="empty-state">Aucun résultat pour ces filtres.</p>';
    return;
  }

  listEl.innerHTML = filtered.map(profile => {
    const active = profile.id === activeId ? ' is-active' : '';
    const definition = profile.definition || profile.summary || 'Aucune définition courte dans les exports publics actuels.';
    return '<button type="button" class="concept-row' + active + '" data-concept-id="' + esc(profile.id) + '">'
      + '<span class="concept-row__top"><span class="concept-row__type">' + esc(typeLabel(profile.kind)) + '</span></span>'
      + '<span class="concept-row__title">' + esc(profile.label) + '</span>'
      + '<span class="concept-row__definition">' + esc(definition) + '</span>'
      + '<span class="concept-row__counts">'
      + countBadge(profile.atomCount, 'atomes')
      + countBadge(profile.sourceIds.length, 'sources')
      + countBadge(profile.chapters.length, 'chapitres')
      + countBadge(profile.motifCounts.size, 'motifs')
      + countBadge(profile.mythCounts.size, 'mythes')
      + '</span>'
      + '</button>';
  }).join('');
}

function findActiveProfile() {
  return profiles.find(profile => profile.id === activeId && (!typeFilter.value || profile.kind === typeFilter.value))
    || filtered[0]
    || null;
}

function section(title, html, help = '') {
  return '<section class="concept-section"><h3>' + esc(title) + '</h3>'
    + (help ? '<p class="section-help">' + esc(help) + '</p>' : '')
    + html
    + '</section>';
}

function emptyText(text) {
  return '<p class="empty-state">' + esc(text) + '</p>';
}

function renderDefinition(profile) {
  if (!profile.definition) return emptyText('Aucune définition courte dans les exports publics actuels.');
  return '<p>' + esc(profile.definition) + '</p>';
}

function renderSummary(profile) {
  if (!profile.summary) {
    return emptyText('Aucun résumé éditorial distinct n’est disponible pour cette entrée.');
  }
  return '<p>' + esc(profile.summary) + '</p>';
}

function renderSources(profile) {
  if (!profile.sourceIds.length) return emptyText('Aucune source associée dans le graphe public ou les fallbacks directs.');
  return '<div class="badge-grid">'
    + profile.sourceIds.map(sourceId => badge(sourceLabel(sourceId), semanticHref('source', sourceId))).join('')
    + '</div>';
}

function renderQuotes(profile) {
  const quotes = profile.quotes.slice(0, 8);
  if (!quotes.length) return emptyText('Aucune citation associée via les sources reliées à cette entrée.');
  const items = quotes.map(quote => {
    const data = quote.data || {};
    const text = T(data.texte || data.citation_originale || data.citation || '(citation non transcrite)');
    const source = sourceLabel(normalizeSourceId(data.source_id));
    const speaker = T(data.locuteur);
    const meta = [speaker, source].filter(Boolean).join(' · ');
    return '<li class="concept-item"><p class="concept-item__meta">' + esc(meta) + '</p>'
      + '<blockquote>' + esc(text) + '</blockquote></li>';
  }).join('');
  const more = profile.quotes.length > quotes.length
    ? '<p class="more-note">Extrait : ' + quotes.length + ' citation(s) affichée(s) sur ' + profile.quotes.length + ' associée(s).</p>'
    : '';
  return '<ul class="concept-list">' + items + '</ul>' + more;
}

function atomTitle(atom) {
  const data = atom.data || {};
  return T(data.titre || data.resume || atom.heading || 'Point documentaire');
}

function renderAtoms(profile) {
  const atoms = profile.atoms.slice(0, 10);
  if (!atoms.length) return emptyText('Aucun atome associé dans le graphe public ou les fallbacks directs.');
  const items = atoms.map(atom => {
    const data = atom.data || {};
    const source = sourceLabel(normalizeSourceId(data.source_id));
    const chapters = listFromFields(data, ['usage_livre', 'chapitres', 'chapters'], normalizeChapter).join(', ');
    const meta = [source, chapters].filter(Boolean).join(' · ');
    return '<li class="concept-item"><p class="concept-item__title">' + esc(atomTitle(atom)) + '</p>'
      + '<p class="concept-item__meta">' + esc(meta || 'Contexte non renseigné') + '</p></li>';
  }).join('');
  const more = profile.atoms.length > atoms.length
    ? '<p class="more-note">Extrait : ' + atoms.length + ' atome(s) affiché(s) sur ' + profile.atoms.length + ' associé(s).</p>'
    : '';
  return '<ul class="concept-list">' + items + '</ul>' + more;
}

function renderSemanticBadges(map, kind, empty) {
  const entries = topEntries(map, 16);
  if (!entries.length) return emptyText(empty);
  return '<div class="badge-grid">'
    + entries.map(([id, count]) => badge(publicLabel(id, kind) + ' (' + count + ')', semanticHref(kind))).join('')
    + '</div>';
}

function renderPeople(profile) {
  const entries = topEntries(profile.personCounts, 16);
  if (!entries.length) return emptyText('Aucune personne indirectement liée via les citations associées.');
  return '<div class="badge-grid">' + entries.map(([id, count]) => badge(publicLabel(id) + ' (' + count + ')')).join('') + '</div>';
}

function renderChapters(profile) {
  if (!profile.chapters.length) return emptyText('Aucun chapitre concerné dans les exports publics actuels.');
  return '<div class="badge-grid">' + profile.chapters.map(chapter => badge(chapter)).join('') + '</div>';
}

function renderDetail() {
  const profile = findActiveProfile();
  if (!profile) {
    detailEl.innerHTML = '<p class="empty-state">Choisissez une entrée dans la liste.</p>';
    return;
  }
  activeId = profile.id;
  const enrichment = profile.graphEnriched
    ? 'Enrichi par le graphe public'
    : profile.fallbackEnriched
      ? 'Enrichi par les champs directs disponibles'
      : 'Fiche minimale';

  detailEl.innerHTML = '<div class="concept-detail__header">'
    + '<p class="concept-detail__eyebrow">' + esc(typeLabel(profile.kind)) + '</p>'
    + '<h2>' + esc(profile.label) + '</h2>'
    + '<p class="concept-detail__meta">' + esc(enrichment) + '</p>'
    + '<div class="concept-counts">'
    + countBadge(profile.atomCount, 'atomes')
    + countBadge(profile.sourceIds.length, 'sources')
    + countBadge(profile.quotes.length, 'citations')
    + countBadge(profile.chapters.length, 'chapitres')
    + countBadge(profile.motifCounts.size, 'motifs')
    + countBadge(profile.mythCounts.size, 'mythes')
    + '</div>'
    + '</div>'
    + section('Définition', renderDefinition(profile))
    + section('Résumé éditorial', renderSummary(profile))
    + section('Sources associées', renderSources(profile), 'Sources reliées par les points documentaires ou par les champs directs disponibles.')
    + section('Citations associées', renderQuotes(profile), 'Citations retrouvées via les sources associées.')
    + section('Atomes associés', renderAtoms(profile), 'Points documentaires qui relient cette entrée aux sources, chapitres et autres registres.')
    + section('Motifs associés', renderSemanticBadges(profile.motifCounts, 'motif', 'Aucun motif associé par atome partagé.'), 'Motifs reliés par points documentaires communs.')
    + section('Mythes associés', renderSemanticBadges(profile.mythCounts, 'myth', 'Aucun mythe associé par atome partagé.'), 'Mythes reliés par points documentaires communs.')
    + section('Personnes indirectement liées', renderPeople(profile), 'Personnes citées dans les citations des sources associées.')
    + section('Chapitres concernés', renderChapters(profile));
}

function exportCSV() {
  const labels = activeViewLabels(typeFilter.value);
  const headers = ['libelle', 'type', 'definition', 'atomes', 'sources', 'chapitres', 'motifs', 'mythes'];
  const rows = filtered.map(profile => [
    profile.label,
    typeLabel(profile.kind),
    profile.definition,
    profile.atomCount,
    profile.sourceIds.length,
    profile.chapters.length,
    profile.motifCounts.size,
    profile.mythCounts.size
  ]);
  const csv = [headers, ...rows].map(row => row.map(value => '"' + T(value).replace(/"/g, '""') + '"').join(',')).join('\n');
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = labels.exportName;
  link.click();
  URL.revokeObjectURL(link.href);
}

async function loadConceptRegister() {
  try {
    const [conceptRecords, atomRecords, quoteRecords, sourceRecords, edgePayload, index] = await Promise.all([
      loadGeneratedJSON('concepts.json'),
      loadGeneratedJSON('atoms.json'),
      loadGeneratedJSON('quotes.json'),
      loadGeneratedJSON('sources.json'),
      loadGeneratedJSON('edges.json'),
      loadGeneratedJSON('index_by_id.json')
    ]);
    profiles = buildProfiles({
      concepts: Array.isArray(conceptRecords) ? conceptRecords : [],
      atoms: Array.isArray(atomRecords) ? atomRecords : [],
      quotes: Array.isArray(quoteRecords) ? quoteRecords : [],
      sources: Array.isArray(sourceRecords) ? sourceRecords : [],
      edges: Array.isArray(edgePayload.edges) ? edgePayload.edges : [],
      index: index || {}
    });
    const requestedType = initialTypeFilter();
    configureDedicatedMode(requestedType);
    typeFilter.value = requestedType;
    hydrateFilters();
    applyFilters();
  } catch (error) {
    console.error(error);
    statusCard.textContent = 'Erreur de chargement du registre : ' + error.message;
    detailEl.innerHTML = '<p class="empty-state">Impossible de charger les exports publics.</p>';
  }
}

listEl.addEventListener('click', event => {
  const row = event.target.closest('[data-concept-id]');
  if (!row) return;
  activeId = row.dataset.conceptId;
  renderList();
  renderDetail();
});

[searchInput, sourceFilter, chapterFilter, typeFilter].forEach(element => {
  element.addEventListener('input', applyFilters);
});

resetButton.addEventListener('click', () => {
  searchInput.value = '';
  sourceFilter.value = '';
  chapterFilter.value = '';
  typeFilter.value = dedicatedType;
  applyFilters();
});

downloadButton.addEventListener('click', exportCSV);

loadConceptRegister();
