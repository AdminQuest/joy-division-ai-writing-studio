const peopleList = document.getElementById('people-list');
const statusCard = document.getElementById('status-card');
const resultsMeta = document.getElementById('results-meta');
const searchInput = document.getElementById('search');
const sourceFilter = document.getElementById('source-filter');
const roleFilter = document.getElementById('role-filter');
const entityFilter = document.getElementById('entity-filter');
const chapterFilter = document.getElementById('chapter-filter');
const resetButton = document.getElementById('reset-filters');
const downloadButton = document.getElementById('download-csv');

let people = [];
let sourceLabels = {};

const T = v => DynamicRegisters.text(v);
const A = v => DynamicRegisters.array(v);
const U = v => DynamicRegisters.uniq(v);
const sourceIds = item => DynamicRegisters.sourceIds(item);
const sourceLabel = id => sourceLabels[id] || id || '';
const chaptersOf = data => A(data.chapters || data.chapitres);
const nameOf = data => data.name || data.nom || data.full_name || data.person || '';

async function loadPeople() {
  try {
    sourceLabels = await DynamicRegisters.sourceLabels();
    people = await DynamicRegisters.loadRecords({ prefixes: ['registers/people/', 'registers/', 'sources/'], kinds: ['person'] });
    people.sort((a, b) => T(nameOf(a.data || {})).localeCompare(T(nameOf(b.data || {})), undefined, { numeric: true }));
    populateFilters();
    renderPeople(people);
    statusCard.textContent = people.length + ' acteur(s) chargé(s) depuis les fichiers Markdown spécialisés';
  } catch (error) {
    console.error(error);
    statusCard.textContent = 'Erreur lors du chargement dynamique des acteurs : ' + error.message;
  }
}

function addOptions(select, values, labeler = v => v) {
  select.innerHTML = '<option value="">Tous</option>';
  values.forEach(value => {
    const option = document.createElement('option');
    option.value = value;
    option.textContent = labeler(value);
    select.appendChild(option);
  });
}

function populateFilters() {
  addOptions(sourceFilter, U(people.flatMap(sourceIds)), sourceLabel);
  addOptions(roleFilter, U(people.flatMap(p => A((p.data || {}).role))));
  addOptions(entityFilter, U(people.flatMap(p => A((p.data || {}).associated_entities))));
  addOptions(chapterFilter, U(people.flatMap(p => chaptersOf(p.data || {}))));
}

function badges(values) {
  return A(values).map(v => '<span class="badge">' + T(v) + '</span>').join('');
}
function sourceBadges(item) {
  return sourceIds(item).map(v => '<span class="badge">' + sourceLabel(v) + '</span>').join('');
}
function list(values) {
  const arr = A(values);
  return arr.length ? arr.map(v => '<li>' + T(v) + '</li>').join('') : '<li>—</li>';
}
function notesOf(data) {
  if (data.notes) return data.notes;
  if (data.portraits_by_source) return Object.values(data.portraits_by_source).join('<br>');
  return '';
}

function renderPeople(items) {
  peopleList.innerHTML = '';
  resultsMeta.textContent = items.length + ' résultat(s)';
  items.forEach(item => {
    const data = item.data || {};
    const card = document.createElement('article');
    card.className = 'person-card';
    card.innerHTML = '<div class="person-header"><div><div class="person-name">' + T(nameOf(data)) + '</div><div class="person-period">' + T(data.full_name || '') + ' · ' + T(data.period || '') + '</div></div><div><code>' + T(item.id) + '</code></div></div>'
      + '<div class="badges">' + badges(data.role) + '</div>'
      + '<div class="badges">' + sourceBadges(item) + '</div>'
      + '<div class="columns"><div><h4>Entités associées</h4><ul>' + list(data.associated_entities) + '</ul><h4>Chansons liées</h4><ul>' + list(data.related_songs) + '</ul><h4>Événements liés</h4><ul>' + list(data.related_events) + '</ul></div><div><h4>Contradictions</h4><ul>' + list(data.contradictions) + '</ul><h4>Précautions méthodologiques</h4><ul>' + list(data.methodological_warnings) + '</ul><h4>Chapitres</h4><ul>' + list(chaptersOf(data)) + '</ul></div></div>'
      + '<div class="notes"><strong>Notes :</strong><br>' + T(notesOf(data)) + '<br><code>' + item.file + '</code></div>';
    peopleList.appendChild(card);
  });
}

function filterPeople() {
  const query = searchInput.value.toLowerCase();
  const source = sourceFilter.value;
  const role = roleFilter.value;
  const entity = entityFilter.value;
  const chapter = chapterFilter.value;
  const filtered = people.filter(item => {
    const data = item.data || {};
    const ids = sourceIds(item);
    const chapters = chaptersOf(data);
    const haystack = [item.id, nameOf(data), data.full_name, data.period, notesOf(data), ...A(data.role), ...ids, ...ids.map(sourceLabel), ...A(data.associated_entities), ...A(data.related_songs), ...chapters, ...A(data.contradictions), item.file].map(T).join(' ').toLowerCase();
    return (!query || haystack.includes(query))
      && (!source || ids.includes(source))
      && (!role || A(data.role).includes(role))
      && (!entity || A(data.associated_entities).includes(entity))
      && (!chapter || chapters.includes(chapter));
  });
  renderPeople(filtered);
}

function exportCSV() {
  const rows = [['id','name','full_name','period','roles','sources','entities','songs','chapters','file']];
  people.forEach(item => {
    const data = item.data || {};
    rows.push([item.id, T(nameOf(data)), T(data.full_name), T(data.period), A(data.role).join(' | '), sourceIds(item).map(sourceLabel).join(' | '), A(data.associated_entities).join(' | '), A(data.related_songs).join(' | '), chaptersOf(data).join(' | '), item.file]);
  });
  const csv = rows.map(r => r.map(v => '"' + String(v || '').replace(/"/g, '""') + '"').join(',')).join('\n');
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'registre_acteurs_dynamique.csv';
  link.click();
  URL.revokeObjectURL(link.href);
}

[searchInput, sourceFilter, roleFilter, entityFilter, chapterFilter].forEach(el => el.addEventListener('input', filterPeople));
resetButton.addEventListener('click', () => { searchInput.value=''; sourceFilter.value=''; roleFilter.value=''; entityFilter.value=''; chapterFilter.value=''; renderPeople(people); });
downloadButton.addEventListener('click', exportCSV);
loadPeople();
