const quotesBody = document.getElementById('quotes-body');
const statusCard = document.getElementById('status-card');
const resultsMeta = document.getElementById('results-meta');
const searchInput = document.getElementById('search');
const sourceFilter = document.getElementById('source-filter');
const statusFilter = document.getElementById('status-filter');
const importanceFilter = document.getElementById('importance-filter');
const chapterFilter = document.getElementById('chapter-filter');
const resetButton = document.getElementById('reset-filters');
const downloadButton = document.getElementById('download-csv');

let quotes = [];
let sourceLabels = {};

const T = v => DynamicRegisters.text(v);
const A = v => DynamicRegisters.array(v);
const sourceIds = item => DynamicRegisters.sourceIds(item);
const sourceLabel = id => sourceLabels[id] || id || '';
const normalizeStatus = status => !status ? '' : (typeof status === 'string' ? status : Object.values(status).join(' · '));
const chaptersOf = data => A(data.chapitres || data.chapters);

async function loadQuotes() {
  try {
    sourceLabels = await DynamicRegisters.sourceLabels();
    quotes = await DynamicRegisters.loadRecords({ prefixes: ['registers/quotes/', 'sources/'], kinds: ['quote'] });
    quotes.sort((a, b) => a.id.localeCompare(b.id, undefined, { numeric: true }));
    populateFilters();
    renderQuotes(quotes);
    statusCard.textContent = quotes.length + ' citation(s) chargée(s) depuis les fichiers Markdown spécialisés';
  } catch (error) {
    console.error(error);
    statusCard.textContent = 'Erreur lors du chargement dynamique des citations : ' + error.message;
  }
}

function uniqueValues(values) {
  return DynamicRegisters.uniq(values);
}

function populateSelect(select, values, labeler = v => v) {
  select.innerHTML = '<option value="">Toutes</option>';
  values.forEach(value => {
    const option = document.createElement('option');
    option.value = value;
    option.textContent = labeler(value);
    select.appendChild(option);
  });
}

function populateFilters() {
  populateSelect(sourceFilter, uniqueValues(quotes.flatMap(sourceIds)), sourceLabel);
  populateSelect(statusFilter, uniqueValues(quotes.map(q => normalizeStatus(q.data && (q.data.statut_verification || q.data.statut_consolidation || q.data.status)))));
  populateSelect(importanceFilter, uniqueValues(quotes.map(q => q.data && q.data.importance)));
  populateSelect(chapterFilter, uniqueValues(quotes.flatMap(q => chaptersOf(q.data || {}))));
}

function renderQuotes(items) {
  quotesBody.innerHTML = '';
  resultsMeta.textContent = items.length + ' résultat(s)';
  items.forEach(item => {
    const data = item.data || {};
    const ids = sourceIds(item);
    const row = document.createElement('tr');
    row.innerHTML = '<td><strong>' + item.id + '</strong></td>'
      + '<td>' + (ids.map(sourceLabel).join('<br>') || sourceLabel(data.source_id || '')) + '</td>'
      + '<td>' + (data.citation_originale || data.citation_directe || data.quote || data.citation || '') + '</td>'
      + '<td>' + (data.traduction_editoriale_fr || data.traduction_litterale_fr || data.usage_recommande || data.arbitrage || '') + '</td>'
      + '<td>' + (data.page_pdf || data.pages_pdf || '') + '</td>'
      + '<td>' + (data.importance || '') + '</td>'
      + '<td class="small">' + normalizeStatus(data.statut_verification || data.statut_consolidation || data.status) + '</td>'
      + '<td class="small">' + chaptersOf(data).join('<br>') + '</td>'
      + '<td class="small"><code>' + item.file + '</code></td>';
    quotesBody.appendChild(row);
  });
}

function filterQuotes() {
  const query = searchInput.value.toLowerCase();
  const source = sourceFilter.value;
  const status = statusFilter.value;
  const importance = importanceFilter.value;
  const chapter = chapterFilter.value;
  const filtered = quotes.filter(item => {
    const data = item.data || {};
    const ids = sourceIds(item);
    const st = normalizeStatus(data.statut_verification || data.statut_consolidation || data.status);
    const ch = chaptersOf(data);
    const haystack = [item.id, ...ids, ...ids.map(sourceLabel), data.citation_originale, data.citation_directe, data.quote, data.citation, data.traduction_editoriale_fr, data.usage_recommande, data.arbitrage, ...ch, item.file].map(T).join(' ').toLowerCase();
    return (!query || haystack.includes(query))
      && (!source || ids.includes(source))
      && (!status || st.includes(status))
      && (!importance || data.importance === importance)
      && (!chapter || ch.includes(chapter));
  });
  renderQuotes(filtered);
}

function exportCSV() {
  const rows = [['id','sources','citation_originale','traduction_editoriale_fr','page_pdf','importance','statut','chapitres','file']];
  quotes.forEach(item => {
    const data = item.data || {};
    rows.push([item.id, sourceIds(item).map(sourceLabel).join(' | '), data.citation_originale || data.citation_directe || data.quote || data.citation || '', data.traduction_editoriale_fr || data.traduction_litterale_fr || data.usage_recommande || data.arbitrage || '', data.page_pdf || data.pages_pdf || '', data.importance || '', normalizeStatus(data.statut_verification || data.statut_consolidation || data.status), chaptersOf(data).join(' | '), item.file]);
  });
  const csv = rows.map(row => row.map(v => '"' + String(v || '').replace(/"/g, '""') + '"').join(',')).join('\n');
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'registre_citations_dynamique.csv';
  link.click();
  URL.revokeObjectURL(link.href);
}

[searchInput, sourceFilter, statusFilter, importanceFilter, chapterFilter].forEach(element => element.addEventListener('input', filterQuotes));
resetButton.addEventListener('click', () => { searchInput.value=''; sourceFilter.value=''; statusFilter.value=''; importanceFilter.value=''; chapterFilter.value=''; renderQuotes(quotes); });
downloadButton.addEventListener('click', exportCSV);
loadQuotes();
