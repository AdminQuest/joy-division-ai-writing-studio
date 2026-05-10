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

const SOURCE_ID_ALIASES = {'S-BROLL-JOY-001':'S68'};
const FALLBACK_SOURCE_LABELS = {
  S41:'S41 — Hook, Unknown Pleasures, 2012',
  S45:'S45 — Curtis, Touching from a Distance, 1995',
  S46:'S46 — Johnson, An Ideal for Living, 1984',
  S47:'S47 — West, Joy Division, 1983',
  S68:'S68 — Broll, Joy Division, s.d.'
};
function normalizeSourceId(id){return SOURCE_ID_ALIASES[id] || id || ''}
async function loadJson(path,fallback){try{const r=await fetch(path,{cache:'no-store'});if(!r.ok)throw new Error(`${path} ${r.status}`);return await r.json()}catch(e){console.warn('Fallback',path,e);return fallback||[]}}
function buildSourceLabels(registry){const labels={...FALLBACK_SOURCE_LABELS};registry.forEach(entry=>{const id=normalizeSourceId(entry.id||entry.source_id);if(!id)return;labels[id]=entry.source_label||labels[id]||id;if(entry.legacy_id)labels[entry.legacy_id]=labels[id]});return labels}
function sourceLabel(id){const normalized=normalizeSourceId(id);return sourceLabels[normalized] || sourceLabels[id] || normalized}

async function loadQuotes() {
  try {
    const [loadedQuotes, registry] = await Promise.all([
      loadJson('../../exports/generated/quotes.json', []),
      loadJson('../../data/registre.json', [])
    ]);
    quotes = loadedQuotes;
    sourceLabels = buildSourceLabels(registry);

    populateFilters();
    renderQuotes(quotes);

    statusCard.textContent = `${quotes.length} citation(s) chargée(s)`;
  } catch (error) {
    console.error(error);
    statusCard.textContent = 'Erreur lors du chargement du registre des citations.';
  }
}

function uniqueValues(values) {
  return [...new Set(values.filter(Boolean))].sort((a,b)=>a.localeCompare(b,undefined,{numeric:true}));
}

function populateSelect(select, values, labeler=(v)=>v) {
  select.innerHTML = select.querySelector('option') ? '<option value="">Toutes</option>' : '';
  values.forEach(value => {
    const option = document.createElement('option');
    option.value = value;
    option.textContent = labeler(value);
    select.appendChild(option);
  });
}

function populateFilters() {
  populateSelect(sourceFilter, uniqueValues(quotes.map(q => normalizeSourceId(q.data?.source_id))), sourceLabel);
  populateSelect(statusFilter, uniqueValues(quotes.map(q => normalizeStatus(q.data?.statut_verification))));
  populateSelect(importanceFilter, uniqueValues(quotes.map(q => q.data?.importance)));

  const chapters = uniqueValues(quotes.flatMap(q => q.data?.chapitres || []));
  populateSelect(chapterFilter, chapters);
}

function normalizeStatus(status) {
  if (!status) return '';
  if (typeof status === 'string') return status;
  return Object.values(status).join(' · ');
}

function renderQuotes(items) {
  quotesBody.innerHTML = '';
  resultsMeta.textContent = `${items.length} résultat(s)`;

  items.forEach(item => {
    const data = item.data || {};
    const sourceId = normalizeSourceId(data.source_id);
    const row = document.createElement('tr');

    row.innerHTML = `
      <td><strong>${item.id}</strong></td>
      <td>${sourceLabel(sourceId)}</td>
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
    const sourceId = normalizeSourceId(data.source_id);
    const haystack = [
      item.id,
      sourceId,
      sourceLabel(sourceId),
      data.citation_originale,
      data.traduction_editoriale_fr,
      data.auteur_citation,
      data.source_citation,
      ...(data.chapitres || [])
    ].join(' ').toLowerCase();

    return (!query || haystack.includes(query))
      && (!source || sourceId === source)
      && (!status || normalizeStatus(data.statut_verification).includes(status))
      && (!importance || data.importance === importance)
      && (!chapter || (data.chapitres || []).includes(chapter));
  });

  renderQuotes(filtered);
}

function exportCSV() {
  const rows = [['id','source','citation_originale','traduction_editoriale_fr','page_pdf','importance','statut_verification']];
  document.querySelectorAll('#quotes-body tr').forEach(tr => {
    const cols = [...tr.querySelectorAll('td')].map(td => td.innerText.replace(/\n/g,' | '));
    rows.push(cols.slice(0,7));
  });
  const csv = rows.map(row => row.map(value => `"${String(value).replace(/"/g,'""')}"`).join(',')).join('\n');
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = 'registre_citations.csv';
  link.click();
  URL.revokeObjectURL(url);
}

[searchInput, sourceFilter, statusFilter, importanceFilter, chapterFilter].forEach(element => element.addEventListener('input', filterQuotes));
resetButton.addEventListener('click', () => {searchInput.value='';sourceFilter.value='';statusFilter.value='';importanceFilter.value='';chapterFilter.value='';renderQuotes(quotes);});
downloadButton.addEventListener('click', exportCSV);
loadQuotes();
