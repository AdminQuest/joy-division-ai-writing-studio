const conceptsList = document.getElementById('concepts-list');
const resultsMeta = document.getElementById('results-meta');
const statusCard = document.getElementById('status-card');
const searchInput = document.getElementById('search');
const sourceFilter = document.getElementById('source-filter');
const chapterFilter = document.getElementById('chapter-filter');
const typeFilter = document.getElementById('type-filter');
const resetButton = document.getElementById('reset-filters');
const downloadButton = document.getElementById('download-csv');

let concepts = [];
let sourceLabels = {};

const T = v => DynamicRegisters.text(v);
const A = v => DynamicRegisters.array(v);
const U = v => DynamicRegisters.uniq(v);
const sourceIds = item => DynamicRegisters.sourceIds(item);
const sourceLabel = id => sourceLabels[id] || id || '';
const chaptersOf = d => A(d.chapitres || d.chapters);
const conceptName = d => d.nom || d.name || d.concept || d.mythe || d.motif || d.id || '';

async function loadConcepts() {
  try {
    sourceLabels = await DynamicRegisters.sourceLabels();
    const explicit = await DynamicRegisters.loadRecords({ prefixes: ['registers/concepts/', 'registers/myths/', 'registers/motifs/'], kinds: ['concept', 'myth', 'motif'] });
    const atoms = await DynamicRegisters.loadRecords({ prefixes: ['sources/', 'registers/'], kinds: ['atom'] });
    concepts = buildConcepts(explicit, atoms);
    hydrateFilters(concepts);
    render(concepts);
    statusCard.textContent = concepts.length + ' concept(s) chargé(s) depuis les fichiers Markdown spécialisés et les atomes';
  } catch (err) {
    console.error(err);
    statusCard.textContent = 'Erreur de chargement dynamique du registre des concepts : ' + err.message;
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
  explicitRecords.forEach(record => {
    const d = record.data || {};
    const key = conceptName(d);
    const entry = ensure(key);
    if (!entry) return;
    entry.explicit.push(record);
    entry.occurrences += 1;
    sourceIds(record).forEach(s => entry.sources.add(s));
    chaptersOf(d).forEach(c => entry.chapters.add(c));
    entry.types.add(record.kind);
    if (d.definition) entry.definitions.push(d.definition);
    if (d.correction) entry.definitions.push(d.correction);
  });
  atoms.forEach(atom => {
    const d = atom.data || {};
    const names = [...A(d.concepts), ...A(d.concepts_derives), ...A(d.related_concepts), ...A(d.motifs), ...A(d.related_motifs), ...A(d.myths), ...A(d.related_myths)];
    names.forEach(name => {
      const entry = ensure(name);
      if (!entry) return;
      entry.occurrences += 1;
      sourceIds(atom).forEach(s => entry.sources.add(s));
      if (d.source_id) entry.sources.add(d.source_id);
      chaptersOf(d).forEach(c => entry.chapters.add(c));
      if (d.type_unite) entry.types.add(d.type_unite);
      entry.atoms.push({ id: d.id || atom.id, heading: atom.heading || '', source: d.source_id || sourceIds(atom)[0] || '', type: d.type_unite || atom.kind, file: atom.file });
    });
  });
  return [...map.values()].sort((a, b) => b.occurrences - a.occurrences || a.concept.localeCompare(b.concept, undefined, { numeric: true }));
}

function hydrateFilters(items) {
  fill(sourceFilter, U(items.flatMap(i => [...i.sources])), sourceLabel);
  fill(chapterFilter, U(items.flatMap(i => [...i.chapters])));
  fill(typeFilter, U(items.flatMap(i => [...i.types])));
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
  conceptsList.innerHTML = '';
  resultsMeta.textContent = items.length + ' résultat(s)';
  items.forEach(c => {
    const card = document.createElement('article');
    card.className = 'concept-card';
    const defs = c.definitions.length ? '<div class="section-title">Définition / correction</div><p>' + c.definitions.map(T).join('<br>') + '</p>' : '';
    const explicit = c.explicit.length ? '<div class="section-title">Entrées explicites</div><ul>' + c.explicit.map(e => '<li><strong>' + e.id + '</strong> — <code>' + e.file + '</code></li>').join('') + '</ul>' : '';
    card.innerHTML = '<h3>' + c.concept + '</h3>'
      + '<div class="occurrences">' + c.occurrences + ' occurrence(s)</div>'
      + defs
      + '<div class="section-title">Sources</div><div class="meta">' + badges(c.sources, sourceLabel) + '</div>'
      + '<div class="section-title">Chapitres</div><div class="meta">' + badges(c.chapters) + '</div>'
      + '<div class="section-title">Types</div><div class="meta">' + badges(c.types) + '</div>'
      + explicit
      + '<div class="section-title">Occurrences documentaires</div><ul>' + c.atoms.slice(0, 20).map(a => '<li><strong>' + T(a.id) + '</strong> — ' + T(a.heading) + ' <em>(' + sourceLabel(a.source) + ')</em><br><code>' + a.file + '</code></li>').join('') + '</ul>';
    conceptsList.appendChild(card);
  });
}
function applyFilters() {
  const q = searchInput.value.toLowerCase();
  const filtered = concepts.filter(c => {
    const haystack = [c.concept, ...c.definitions, ...c.sources, ...[...c.sources].map(sourceLabel), ...c.chapters, ...c.types, ...c.atoms.map(a => a.heading), ...c.atoms.map(a => a.file), ...c.explicit.map(e => e.file)].join(' ').toLowerCase();
    return (!q || haystack.includes(q))
      && (!sourceFilter.value || c.sources.has(sourceFilter.value))
      && (!chapterFilter.value || c.chapters.has(chapterFilter.value))
      && (!typeFilter.value || c.types.has(typeFilter.value));
  });
  render(filtered);
}
function exportCSV() {
  const rows = concepts.map(c => ({
    concept: c.concept,
    occurrences: c.occurrences,
    sources: [...c.sources].map(sourceLabel).join('; '),
    chapters: [...c.chapters].join('; '),
    types: [...c.types].join('; ')
  }));
  const header = Object.keys(rows[0] || {}).join(',');
  const body = rows.map(r => Object.values(r).map(v => '"' + String(v).replace(/"/g, '""') + '"').join(',')).join('\n');
  const blob = new Blob([header + '\n' + body], { type: 'text/csv;charset=utf-8;' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'joy_division_concepts_register_dynamic.csv';
  a.click();
  URL.revokeObjectURL(a.href);
}
[searchInput, sourceFilter, chapterFilter, typeFilter].forEach(el => el.addEventListener('input', applyFilters));
resetButton.addEventListener('click', () => { searchInput.value=''; sourceFilter.value=''; chapterFilter.value=''; typeFilter.value=''; render(concepts); });
downloadButton.addEventListener('click', exportCSV);
loadConcepts();
