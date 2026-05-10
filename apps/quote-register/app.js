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

async function loadQuotes() {
  try {
    const response = await fetch('../../exports/generated/quotes.json');
    quotes = await response.json();

    populateFilters();
    renderQuotes(quotes);

    statusCard.textContent = `${quotes.length} citation(s) chargée(s)`;
  } catch (error) {
    console.error(error);
    statusCard.textContent = 'Erreur lors du chargement du registre des citations.';
  }
}

function uniqueValues(values) {
  return [...new Set(values.filter(Boolean))].sort();
}

function populateSelect(select, values) {
  values.forEach(value => {
    const option = document.createElement('option');
    option.value = value;
    option.textContent = value;
    select.appendChild(option);
  });
}

function populateFilters() {
  populateSelect(sourceFilter, uniqueValues(quotes.map(q => q.data?.source_id)));
  populateSelect(statusFilter, uniqueValues(quotes.map(q => normalizeStatus(q.data?.statut_verification))));
  populateSelect(importanceFilter, uniqueValues(quotes.map(q => q.data?.importance)));

  const chapters = uniqueValues(
    quotes.flatMap(q => q.data?.chapitres || [])
  );

  populateSelect(chapterFilter, chapters);
}

function normalizeStatus(status) {
  if (!status) return '';

  if (typeof status === 'string') {
    return status;
  }

  return Object.values(status).join(' · ');
}

function renderQuotes(items) {
  quotesBody.innerHTML = '';

  resultsMeta.textContent = `${items.length} résultat(s)`;

  items.forEach(item => {
    const data = item.data || {};

    const row = document.createElement('tr');

    row.innerHTML = `
      <td><strong>${item.id}</strong></td>
      <td>${data.source_id || ''}</td>
      <td>${data.citation_originale || ''}</td>
      <td>${data.traduction_editoriale_fr || ''}</td>
      <td>${data.page_pdf || ''}</td>
      <td>${data.importance || ''}</td>
      <td class="small">${normalizeStatus(data.statut_verification)}</td>
      <td class="small">${(data.chapitres || []).join('<br>')}</td>
      <td class="small"><code>${item.file}</code></td>
    `;

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

    const haystack = [
      item.id,
      data.source_id,
      data.citation_originale,
      data.traduction_editoriale_fr,
      data.auteur_citation,
      data.source_citation,
      ...(data.chapitres || [])
    ]
      .join(' ')
      .toLowerCase();

    const matchesQuery = !query || haystack.includes(query);
    const matchesSource = !source || data.source_id === source;
    const matchesStatus = !status || normalizeStatus(data.statut_verification).includes(status);
    const matchesImportance = !importance || data.importance === importance;
    const matchesChapter = !chapter || (data.chapitres || []).includes(chapter);

    return matchesQuery && matchesSource && matchesStatus && matchesImportance && matchesChapter;
  });

  renderQuotes(filtered);
}

function exportCSV() {
  const rows = [
    ['id','source','citation_originale','traduction_editoriale_fr','page_pdf','importance','statut_verification']
  ];

  document.querySelectorAll('#quotes-body tr').forEach(tr => {
    const cols = [...tr.querySelectorAll('td')].map(td => td.innerText.replace(/\n/g,' | '));
    rows.push(cols.slice(0,7));
  });

  const csv = rows
    .map(row => row.map(value => `"${String(value).replace(/"/g,'""')}"`).join(','))
    .join('\n');

  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);

  const link = document.createElement('a');
  link.href = url;
  link.download = 'registre_citations.csv';
  link.click();

  URL.revokeObjectURL(url);
}

[searchInput, sourceFilter, statusFilter, importanceFilter, chapterFilter]
  .forEach(element => element.addEventListener('input', filterQuotes));

resetButton.addEventListener('click', () => {
  searchInput.value = '';
  sourceFilter.value = '';
  statusFilter.value = '';
  importanceFilter.value = '';
  chapterFilter.value = '';
  renderQuotes(quotes);
});

downloadButton.addEventListener('click', exportCSV);

loadQuotes();
