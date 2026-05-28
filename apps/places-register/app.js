const listEl = document.getElementById('items-list');
const statusCard = document.getElementById('status-card');
const resultsMeta = document.getElementById('results-meta');
const searchInput = document.getElementById('search');
const sourceFilter = document.getElementById('source-filter');
const typeFilter = document.getElementById('type-filter');
const chapterFilter = document.getElementById('chapter-filter');
const resetButton = document.getElementById('reset-filters');
const downloadButton = document.getElementById('download-csv');

let items = [];
let sourceLabels = {};
const T = v => DynamicRegisters.text(v);
const A = v => DynamicRegisters.array(v);
const U = v => DynamicRegisters.uniq(v);
const sourceIds = item => DynamicRegisters.sourceIds(item);
const sourceLabel = id => sourceLabels[id] || id || '';
const chaptersOf = data => A(data.chapters || data.chapitres);
const labelOf = data => data.label || data.nom || data.name || data.id || '';
const typeOf = data => data.type || data.type_lieu || data.category || '';
const resolveUsage = place => {
  if (place.usage) return place.usage;
  const usageKeys = Object.keys(place).filter(k => k.startsWith('usage_'));
  for (const key of usageKeys) {
    if (place[key]) return place[key];
  }
  return place.description || place.note || '';
};

async function loadItems() {
  sourceLabels = await DynamicRegisters.sourceLabels();
  items = await DynamicRegisters.loadRecords({ prefixes: ['registers/places/', 'registers/'], kinds: ['place'] });
  items.sort((a, b) => T(labelOf(a.data || {})).localeCompare(T(labelOf(b.data || {})), undefined, { numeric: true }));
  populateFilters();
  render(items);
  statusCard.textContent = items.length + ' lieu(x) chargé(s) depuis registers/places/';
}
function addOptions(select, values, labeler = v => v) {
  select.innerHTML = '<option value="">Tous</option>';
  values.forEach(value => { const o = document.createElement('option'); o.value = value; o.textContent = labeler(value); select.appendChild(o); });
}
function populateFilters() {
  addOptions(sourceFilter, U(items.flatMap(sourceIds)), sourceLabel);
  addOptions(typeFilter, U(items.map(i => typeOf(i.data || {}))));
  addOptions(chapterFilter, U(items.flatMap(i => chaptersOf(i.data || {}))));
}
function badges(values) { return A(values).map(v => '<span class="badge">' + T(v) + '</span>').join(''); }
function sourceBadges(item) { return sourceIds(item).map(v => '<span class="badge">' + sourceLabel(v) + '</span>').join(''); }
function list(values) { const arr = A(values); return arr.length ? arr.map(v => '<li>' + T(v) + '</li>').join('') : '<li>—</li>'; }
function render(rows) {
  listEl.innerHTML = '';
  resultsMeta.textContent = rows.length + ' résultat(s)';
  rows.forEach(item => {
    const data = item.data || {};
    const card = document.createElement('article');
    card.className = 'person-card';
    const usage = resolveUsage(data);
    card.innerHTML = '<div class="person-header"><div><div class="person-name">' + T(labelOf(data)) + '</div><div class="person-period">' + T(typeOf(data)) + '</div></div><div><code>' + T(item.id) + '</code></div></div>'
      + '<div class="badges">' + sourceBadges(item) + '</div>'
      + '<div class="columns"><div><h4>Usage</h4><ul>' + list(usage) + '</ul><h4>Sources</h4><div class="badges">' + sourceBadges(item) + '</div></div><div><h4>Prudences</h4><ul>' + list(data.prudence || data.methodological_warnings) + '</ul><h4>Chapitres</h4><ul>' + list(chaptersOf(data)) + '</ul></div></div>'
      + '<div class="notes"><code>' + item.file + '</code></div>';
    listEl.appendChild(card);
  });
}
function filterItems() {
  const q = searchInput.value.toLowerCase();
  const filtered = items.filter(item => {
    const data = item.data || {};
    const ids = sourceIds(item);
    const chapters = chaptersOf(data);
    const haystack = [item.id, labelOf(data), typeOf(data), data.usage, data.usage_s02, data.usage_s05, data.usage_s20, data.description, data.prudence, ...ids, ...ids.map(sourceLabel), ...chapters, item.file].map(T).join(' ').toLowerCase();
    return (!q || haystack.includes(q)) && (!sourceFilter.value || ids.includes(sourceFilter.value)) && (!typeFilter.value || typeOf(data) === typeFilter.value) && (!chapterFilter.value || chapters.includes(chapterFilter.value));
  });
  render(filtered);
}
function exportCSV() {
  const rows = [['id','label','type','sources','chapters','file']];
  items.forEach(item => { const data = item.data || {}; rows.push([item.id, labelOf(data), typeOf(data), sourceIds(item).map(sourceLabel).join(' | '), chaptersOf(data).join(' | '), item.file]); });
  const csv = rows.map(r => r.map(v => '"' + String(v || '').replace(/"/g, '""') + '"').join(',')).join('\n');
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'registre_lieux.csv'; a.click(); URL.revokeObjectURL(a.href);
}
[searchInput, sourceFilter, typeFilter, chapterFilter].forEach(el => el.addEventListener('input', filterItems));
resetButton.addEventListener('click', () => { searchInput.value=''; sourceFilter.value=''; typeFilter.value=''; chapterFilter.value=''; render(items); });
downloadButton.addEventListener('click', exportCSV);
loadItems().catch(err => { console.error(err); statusCard.textContent = 'Erreur : ' + err.message; });
