const timeline = document.getElementById('timeline');
const statusCard = document.getElementById('status-card');
const resultsMeta = document.getElementById('results-meta');
const searchInput = document.getElementById('search');
const yearFilter = document.getElementById('year-filter');
const typeFilter = document.getElementById('type-filter');
const locationFilter = document.getElementById('location-filter');
const sourceFilter = document.getElementById('source-filter');
const resetButton = document.getElementById('reset-filters');
const downloadButton = document.getElementById('download-csv');

let events = [];
let sourceLabels = {};

const T = v => DynamicRegisters.text(v);
const A = v => DynamicRegisters.array(v);
const sourceIds = item => DynamicRegisters.sourceIds(item);
const sourceLabel = id => sourceLabels[id] || id || '';
const eventDate = item => T(item && item.data && item.data.date);
const first = v => Array.isArray(v) ? T(v[0]) : T(v);
const li = values => A(values).map(v => '<li>' + T(v) + '</li>').join('') || '<li>—</li>';

async function loadChronology() {
  try {
    sourceLabels = await DynamicRegisters.sourceLabels();
    events = await DynamicRegisters.loadRecords({ prefixes: ['registers/chronology/', 'registers/', 'sources/'], kinds: ['chronology'] });
    events.sort((a, b) => eventDate(a).localeCompare(eventDate(b), undefined, { numeric: true }));
    populateFilters();
    renderEvents(events);
    statusCard.textContent = events.length + ' événement(s) chargé(s) depuis les fichiers Markdown spécialisés';
  } catch (error) {
    console.error(error);
    statusCard.textContent = 'Erreur lors du chargement dynamique de la chronologie : ' + error.message;
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
  addOptions(yearFilter, DynamicRegisters.uniq(events.map(e => eventDate(e).slice(0, 4))));
  addOptions(typeFilter, DynamicRegisters.uniq(events.flatMap(e => A(e.data && e.data.type))));
  addOptions(locationFilter, DynamicRegisters.uniq(events.flatMap(e => A(e.data && e.data.location))));
  addOptions(sourceFilter, DynamicRegisters.uniq(events.flatMap(sourceIds)), sourceLabel);
}

function renderEvents(items) {
  timeline.innerHTML = '';
  resultsMeta.textContent = items.length + ' résultat(s)';
  items.forEach(item => {
    const data = item.data || {};
    const block = document.createElement('article');
    block.className = 'timeline-item';
    const sources = sourceIds(item).map(s => '<span class="badge">' + sourceLabel(s) + '</span>').join('');
    block.innerHTML = '<div class="timeline-date">' + (eventDate(item) || 'Date inconnue') + '</div>'
      + '<div class="timeline-event">' + (data.event || data.evenement || '') + '</div>'
      + '<div class="timeline-meta"><span class="badge">' + (first(data.type) || 'type inconnu') + '</span><span class="badge">' + (first(data.location) || 'lieu inconnu') + '</span><span class="badge">' + (data.precision_date || 'précision inconnue') + '</span><span class="badge">certitude : ' + (data.certainty || data.statut || 'non précisée') + '</span></div>'
      + '<div class="timeline-meta">' + sources + '</div>'
      + '<div class="timeline-lists"><div><h4>Personnes</h4><ul>' + li(data.people) + '</ul></div><div><h4>Chansons</h4><ul>' + li(data.songs) + '</ul></div></div>';
    timeline.appendChild(block);
  });
}

function filterEvents() {
  const query = searchInput.value.toLowerCase();
  const year = yearFilter.value;
  const type = typeFilter.value;
  const location = locationFilter.value;
  const source = sourceFilter.value;
  renderEvents(events.filter(item => {
    const data = item.data || {};
    const date = eventDate(item);
    const ids = sourceIds(item);
    const types = A(data.type).map(T);
    const locations = A(data.location).map(T);
    const haystack = [item.id, date, data.event, data.evenement, ...types, ...locations, ...A(data.people), ...A(data.songs), ...ids, ...ids.map(sourceLabel), item.file].map(T).join(' ').toLowerCase();
    return (!query || haystack.includes(query)) && (!year || date.startsWith(year)) && (!type || types.includes(type)) && (!location || locations.includes(location)) && (!source || ids.includes(source));
  }));
}

function exportCSV() {
  const rows = [['id','date','event','type','location','people','songs','sources','file']];
  events.forEach(item => {
    const data = item.data || {};
    rows.push([item.id, eventDate(item), data.event || data.evenement || '', A(data.type).join(' | '), A(data.location).join(' | '), A(data.people).join(' | '), A(data.songs).join(' | '), sourceIds(item).map(sourceLabel).join(' | '), item.file]);
  });
  const csv = rows.map(row => row.map(v => '"' + String(v || '').replace(/"/g, '""') + '"').join(',')).join('\n');
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'registre_chronologique_dynamique.csv';
  link.click();
  URL.revokeObjectURL(link.href);
}

[searchInput, yearFilter, typeFilter, locationFilter, sourceFilter].forEach(el => el.addEventListener('input', filterEvents));
resetButton.addEventListener('click', () => { searchInput.value=''; yearFilter.value=''; typeFilter.value=''; locationFilter.value=''; sourceFilter.value=''; renderEvents(events); });
downloadButton.addEventListener('click', exportCSV);
loadChronology();
