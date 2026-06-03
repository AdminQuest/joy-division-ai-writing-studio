const conceptsList = document.getElementById('concepts-list');
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

let concepts = [];
let sourceLabels = {};
let dedicatedType = '';
let renderedItems = [];

const T = v => DynamicRegisters.text(v);
const A = v => DynamicRegisters.array(v);
const U = v => DynamicRegisters.uniq(v);
const sourceIds = item => DynamicRegisters.sourceIds(item);
const sourceLabel = id => sourceLabels[id] || id || '';

// --- Helpers ---

/**
 * Extracts the canonical source ID (e.g. "S82") from a raw value that
 * might be a full label like "S82 — Parmar, Joy Division in Space, 2018".
 */
function extractSourceId(s) {
  const str = T(s);
  const m = /^(S\d+)\b/.exec(str);
  return m ? m[1] : str;
}

/**
 * Normalise chapter values to "Chapitre N" regardless of whether the
 * source file stored an integer (3) or a string ("Chapitre 3").
 */
function normalizeChapter(c) {
  const n = T(c).trim();
  if (/^\d+$/.test(n)) return 'Chapitre ' + n;
  const m = /^[Cc]hapitre\s+(\d+)$/.exec(n);
  if (m) return 'Chapitre ' + m[1];
  return n;
}

/**
 * Readable labels for the three canonical document types shown in the
 * type filter. Atom-level type_unite values are intentionally excluded.
 */
const TYPE_LABELS = { concept: 'Concept', motif: 'Motif', myth: 'Mythe', mythe: 'Mythe' };
const URL_TYPE_ALIASES = { concept: 'concept', motif: 'motif', myth: 'myth', mythe: 'myth' };
function typeLabel(t) { return TYPE_LABELS[T(t).toLowerCase()] || T(t); }

const VIEW_LABELS = {
  all: {
    documentTitle: 'Registre des concepts, motifs et mythes — Joy Division',
    title: 'Registre des concepts, motifs et mythes',
    resultsTitle: 'Concepts, motifs et mythes',
    singular: 'entrée',
    plural: 'entrées',
    exportName: 'joy_division_concepts_motifs_mythes_register.csv',
    subtitle: 'Vue documentaire dynamique reconstruite directement depuis les fichiers Markdown spécialisés et les atomes.',
    note: 'Ce registre lit directement les fichiers <code>registers/concepts/*.md</code>, <code>registers/myths/*.md</code>, <code>registers/motifs/*.md</code> et les concepts, motifs ou mythes déclarés dans les atomes.'
  },
  concept: {
    documentTitle: 'Registre des concepts — Joy Division',
    title: 'Registre des concepts',
    resultsTitle: 'Concepts',
    singular: 'concept',
    plural: 'concepts',
    exportName: 'joy_division_concepts_register.csv',
    subtitle: 'Vue documentaire dynamique des notions critiques reconstruites depuis les registres spécialisés et les atomes.',
    note: 'Cette vue affiche les entrées de type <code>concept</code> issues des données existantes du registre structurant.'
  },
  motif: {
    documentTitle: 'Registre des motifs — Joy Division',
    title: 'Registre des motifs',
    resultsTitle: 'Motifs',
    singular: 'motif',
    plural: 'motifs',
    exportName: 'joy_division_motifs_register.csv',
    subtitle: 'Vue documentaire dynamique des motifs récurrents, chaînes argumentatives et formes transversales du corpus.',
    note: 'Cette vue affiche les entrées de type <code>motif</code> issues des données existantes du registre structurant.'
  },
  myth: {
    documentTitle: 'Registre des mythes — Joy Division',
    title: 'Registre des mythes',
    resultsTitle: 'Mythes',
    singular: 'mythe',
    plural: 'mythes',
    exportName: 'joy_division_mythes_register.csv',
    subtitle: 'Vue documentaire dynamique des récits à déconstruire, nuancer ou documenter avec prudence historiographique.',
    note: 'Cette vue affiche les entrées de type <code>myth</code> issues des données existantes du registre structurant.'
  }
};

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
  if (registerNote) registerNote.innerHTML = labels.note;
  return labels;
}

function configureDedicatedMode(type) {
  dedicatedType = type || '';
  if (typeField) {
    if (dedicatedType) {
      typeField.hidden = true;
    } else {
      typeField.removeAttribute('hidden');
    }
  }
  if (typeFilter) {
    typeFilter.disabled = !!dedicatedType;
  }
}

function initialTypeFilter() {
  try {
    const raw = new URLSearchParams(window.location.search).get('type');
    return URL_TYPE_ALIASES[T(raw).toLowerCase()] || '';
  } catch (_) {
    return '';
  }
}

/**
 * Resolve the display name for a concept/motif/myth record.
 * Handles all naming conventions used across S62–S82 passes:
 *   - nom  (S62, S77, S78, S82-revised)
 *   - label (S63–S82)
 *   - name / concept / mythe / motif (legacy)
 *   - id  (fallback)
 */
const conceptName = d => T(d.nom || d.label || d.name || d.concept || d.mythe || d.motif || d.id);

/**
 * Extract the definition / functional description from any record,
 * regardless of the field name used by the pass that created it.
 */
function extractDefinition(d) {
  return T(d.definition || d.fonction_argumentative || d.correction || '');
}

const chaptersOf = d => A(d.chapitres || d.chapters).map(normalizeChapter);

async function loadConcepts() {
  try {
    sourceLabels = await DynamicRegisters.sourceLabels();
    const explicit = await DynamicRegisters.loadRecords({ prefixes: ['registers/concepts/', 'registers/myths/', 'registers/motifs/', 'registers/'], kinds: ['concept', 'myth', 'motif'] });
    const atoms = await DynamicRegisters.loadRecords({ prefixes: ['sources/', 'registers/'], kinds: ['atom'] });
    concepts = buildConcepts(explicit, atoms);
    hydrateFilters(concepts);
    const requestedType = initialTypeFilter();
    if (requestedType && [...typeFilter.options].some(option => option.value === requestedType)) {
      configureDedicatedMode(requestedType);
      typeFilter.value = requestedType;
      applyFilters();
    } else {
      configureDedicatedMode('');
      updateViewLabels('');
      render(concepts);
    }
  } catch (err) {
    console.error(err);
    statusCard.textContent = 'Erreur de chargement dynamique du registre : ' + err.message;
  }
}

function buildConcepts(explicitRecords, atoms) {
  const map = new Map();
  function ensure(key) {
    const clean = T(key).trim();
    if (!clean) return null;
    if (!map.has(clean)) {
      map.set(clean, { concept: clean, occurrences: 0, sources: new Set(), chapters: new Set(), types: new Set(), atoms: [], definitions: [], explicit: [] });
    }
    return map.get(clean);
  }

  // --- Explicit concept/motif/myth records ---
  explicitRecords.forEach(record => {
    const d = record.data || {};
    const key = conceptName(d);
    const entry = ensure(key);
    if (!entry) return;
    entry.explicit.push(record);
    entry.occurrences += 1;
    // Normalise sources: accept source_id, sources, or source_ids
    const srcs = A(d.sources || d.source_ids || d.source_id);
    srcs.map(extractSourceId).filter(Boolean).forEach(s => entry.sources.add(s));
    // Also try sourceIds() from DynamicRegisters
    sourceIds(record).map(extractSourceId).filter(Boolean).forEach(s => entry.sources.add(s));
    chaptersOf(d).forEach(c => entry.chapters.add(c));
    // Only record document-level types (concept / motif / myth), not atom type_unite
    entry.types.add(record.kind);
    const def = extractDefinition(d);
    if (def) entry.definitions.push(def);
  });

  // --- Atom records: harvest concepts/motifs/myths they reference ---
  atoms.forEach(atom => {
    const d = atom.data || {};
    const names = [
      ...A(d.concepts), ...A(d.concepts_derives), ...A(d.related_concepts),
      ...A(d.motifs), ...A(d.related_motifs),
      ...A(d.myths), ...A(d.related_myths)
    ];
    names.forEach(name => {
      const entry = ensure(name);
      if (!entry) return;
      entry.occurrences += 1;
      // Normalise source references from atoms
      sourceIds(atom).map(extractSourceId).filter(Boolean).forEach(s => entry.sources.add(s));
      if (d.source_id) entry.sources.add(extractSourceId(T(d.source_id)));
      chaptersOf(d).forEach(c => entry.chapters.add(c));
      // Do NOT push atom type_unite into entry.types — keeps the type filter clean
      entry.atoms.push({
        id: d.id || atom.id,
        heading: atom.heading || '',
        source: extractSourceId(T(d.source_id || sourceIds(atom)[0] || '')),
        type: d.type_unite || atom.kind,
        file: atom.file
      });
    });
  });

  return [...map.values()].sort((a, b) => b.occurrences - a.occurrences || a.concept.localeCompare(b.concept, undefined, { numeric: true }));
}

function hydrateFilters(items) {
  // Problem 2 — Source: one entry per source, format "SXX — Auteur, Titre"
  // Keep only canonical source IDs (S followed by digits) for a clean filter.
  const cleanSources = U(
    items.flatMap(i => [...i.sources]).filter(s => /^S\d+$/.test(s))
  );
  fill(sourceFilter, cleanSources, sourceLabel);

  // Problem 3 — Chapter: deduplicated, normalised "Chapitre N" strings
  const cleanChapters = U(items.flatMap(i => [...i.chapters]));
  fill(chapterFilter, cleanChapters);

  // Problem 4 — Type: only canonical document types with French labels
  const cleanTypes = U(items.flatMap(i => [...i.types]).filter(t => TYPE_LABELS[T(t).toLowerCase()]));
  fill(typeFilter, cleanTypes, typeLabel);
}

function fill(select, values, labeler = v => v) {
  select.innerHTML = '<option value="">Tous</option>';
  values.forEach(v => {
    const o = document.createElement('option');
    o.value = v;
    o.textContent = labeler(v);
    select.appendChild(o);
  });
}
function badges(values, labeler = v => v) {
  return [...values].map(x => '<span class="badge">' + labeler(x) + '</span>').join('');
}
function render(items) {
  renderedItems = items;
  const labels = activeViewLabels(typeFilter.value);
  conceptsList.innerHTML = '';
  const noun = items.length > 1 ? labels.plural : labels.singular;
  resultsMeta.textContent = items.length + ' ' + noun;
  statusCard.textContent = items.length + ' ' + noun + ' dans cette vue';
  items.forEach(c => {
    const card = document.createElement('article');
    card.className = 'concept-card';
    const defs = c.definitions.length
      ? '<div class="section-title">Définition</div><p>' + c.definitions.map(T).join('<br>') + '</p>'
      : '';
    const explicit = c.explicit.length
      ? '<div class="section-title">Entrées explicites</div><ul>'
        + c.explicit.map(e => '<li><strong>' + e.id + '</strong> — <code>' + e.file + '</code></li>').join('')
        + '</ul>'
      : '';
    card.innerHTML = '<h3>' + c.concept + '</h3>'
      + '<div class="occurrences">' + c.occurrences + ' occurrence(s)</div>'
      + defs
      + '<div class="section-title">Sources</div><div class="meta">' + badges(c.sources, sourceLabel) + '</div>'
      + '<div class="section-title">Chapitres</div><div class="meta">' + badges(c.chapters) + '</div>'
      + '<div class="section-title">Types</div><div class="meta">' + badges(c.types, typeLabel) + '</div>'
      + explicit
      + '<div class="section-title">Occurrences documentaires</div><ul>'
        + c.atoms.slice(0, 20).map(a =>
            '<li><strong>' + T(a.id) + '</strong> — ' + T(a.heading)
            + ' <em>(' + sourceLabel(a.source) + ')</em><br><code>' + a.file + '</code></li>'
          ).join('')
        + '</ul>';
    conceptsList.appendChild(card);
  });
}
function applyFilters() {
  updateViewLabels(typeFilter.value);
  const q = searchInput.value.toLowerCase();
  const filtered = concepts.filter(c => {
    const haystack = [
      c.concept,
      ...c.definitions,
      ...c.sources,
      ...[...c.sources].map(sourceLabel),
      ...c.chapters,
      ...c.types,
      ...c.atoms.map(a => a.heading),
      ...c.atoms.map(a => a.file),
      ...c.explicit.map(e => e.file)
    ].join(' ').toLowerCase();
    return (!q || haystack.includes(q))
      && (!sourceFilter.value || c.sources.has(sourceFilter.value))
      && (!chapterFilter.value || c.chapters.has(chapterFilter.value))
      && (!typeFilter.value || c.types.has(typeFilter.value));
  });
  render(filtered);
}
function exportCSV() {
  const labels = activeViewLabels(typeFilter.value);
  const rows = renderedItems.map(c => ({
    concept: c.concept,
    occurrences: c.occurrences,
    sources: [...c.sources].map(sourceLabel).join('; '),
    chapters: [...c.chapters].join('; '),
    types: [...c.types].map(typeLabel).join('; ')
  }));
  const header = Object.keys(rows[0] || {}).join(',');
  const body = rows.map(r => Object.values(r).map(v => '"' + String(v).replace(/"/g, '""') + '"').join(',')).join('\n');
  const blob = new Blob([header + '\n' + body], { type: 'text/csv;charset=utf-8;' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = labels.exportName;
  a.click();
  URL.revokeObjectURL(a.href);
}
[searchInput, sourceFilter, chapterFilter, typeFilter].forEach(el => el.addEventListener('input', applyFilters));
resetButton.addEventListener('click', () => {
  searchInput.value = '';
  sourceFilter.value = '';
  chapterFilter.value = '';
  typeFilter.value = dedicatedType;
  applyFilters();
});
downloadButton.addEventListener('click', exportCSV);
loadConcepts();
