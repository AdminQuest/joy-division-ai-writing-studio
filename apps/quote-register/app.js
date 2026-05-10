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

const SOURCE_ID_ALIASES = {'S-BROLL-JOY-001':'S68','S20':'S72','S35':'S41','S37':'S45','S41-HIST':'S73'};
const FALLBACK_SOURCE_LABELS = {
  S01:'S01 — Blakeley & Evans, The Regeneration of East Manchester, 2013',
  S02:'S02 — Sueur, Villes du futur, futur des villes, 2011',
  S03:'S03 — Demographia, England Largest Cities, s.d.',
  S04:'S04 — Kidd, Manchester: A History, 2006',
  S05:'S05 — Jeffery, Tufail & Jackson, Policing and the Reproduction of Local Social Order, 2015',
  S06:'S06 — Carter, Youth, race and the inner-city estate, 2023',
  S41:'S41 — Hook, Unknown Pleasures, 2012',
  S45:'S45 — Curtis, Touching from a Distance, 1995',
  S46:'S46 — Johnson, An Ideal for Living, 1984',
  S47:'S47 — West, Joy Division, 1984',
  S68:'S68 — Broll, Joy Division, 1988',
  S69:'S69 — Greig & Strong, But We Remember When We Were Young, 2014',
  S70:'S70 — Suatoni, Dal cuore della città / From the Centre of the City, 1990',
  S71:'S71 — Flowers, Dreams Never End, 1995/2012',
  S72:'S72 — Reynolds, Rip It Up and Start Again, 2005/2006',
  S73:'S73 — Blue Orchids, entrée historique à consolider, s.d.'
};
function normalizeSourceId(id){return SOURCE_ID_ALIASES[id] || id || ''}
async function loadJson(path,fallback){try{const r=await fetch(path,{cache:'no-store'});if(!r.ok)throw new Error(`${path} ${r.status}`);return await r.json()}catch(e){console.warn('Fallback',path,e);return fallback||[]}}
async function loadText(path,fallback=''){try{const r=await fetch(path,{cache:'no-store'});if(!r.ok)throw new Error(`${path} ${r.status}`);return await r.text()}catch(e){console.warn('Fallback',path,e);return fallback}}
function buildSourceLabels(registry){const labels={...FALLBACK_SOURCE_LABELS};registry.forEach(entry=>{const id=normalizeSourceId(entry.id||entry.source_id);if(!id)return;labels[id]=entry.source_label||labels[id]||id;if(entry.legacy_id){const aliases=Array.isArray(entry.legacy_id)?entry.legacy_id:[entry.legacy_id];aliases.forEach(alias=>labels[alias]=labels[id]);}});return labels}
function sourceLabel(id){const normalized=normalizeSourceId(id);return sourceLabels[normalized] || sourceLabels[id] || normalized}
function stripMd(value){return String(value||'').trim().replace(/^«\s*/,'').replace(/\s*»$/,'').replace(/`/g,'').replace(/<br\s*\/?>/gi,' | ')}
function splitTableRow(line){return line.trim().replace(/^\|/,'').replace(/\|$/,'').split('|').map(stripMd)}
function inferSourceId(id, sourceCell){const direct=String(id||'').match(/^(S\d{2})-Q\d+/);if(direct)return normalizeSourceId(direct[1]);const fromSource=String(sourceCell||'').match(/S\d{2}(?:-HIST)?/);return fromSource?normalizeSourceId(fromSource[0]):''}
function parseConsolidatedQuotesMarkdown(text){
  const rows=[];const lines=String(text||'').split(/\r?\n/);let mode='';
  for(const line of lines){
    if(line.startsWith('## 1.1.')){mode='historical';continue;}
    if(line.startsWith('## 2.')){mode='atomized';continue;}
    if(!line.trim().startsWith('|')||line.includes('---'))continue;
    const cells=splitTableRow(line);
    if(!cells.length||/^ID/.test(cells[0])||/^id$/i.test(cells[0]))continue;
    if(mode==='historical'&&cells.length>=5){
      const [id,source,type,entry,status]=cells;const sourceId=inferSourceId(id,source);
      rows.push({kind:'quote',id,file:'registers/quotes/master_quotes.md',heading:'citation historique consolidée',data:{id,source_id:sourceId,source_label:sourceLabel(sourceId),citation_originale:entry,type_citation:type,statut_consolidation:status,statut_verification:status,importance:'',chapitres:['Chapitre 1'],source_origin:['registre historique','master_quotes.md'],arbitrage:'Entrée importée du registre historique ; à promouvoir seulement après vérification contextuelle.'}});
    } else if(mode==='atomized'&&cells.length>=4){
      const [id,citation,status,usage]=cells;const sourceId=inferSourceId(id,'');
      rows.push({kind:'quote',id,file:'registers/quotes/master_quotes.md',heading:'citation atomisée consolidée',data:{id,source_id:sourceId,source_label:sourceLabel(sourceId),citation_originale:citation,usage_recommande:usage,statut_consolidation:status,statut_verification:status,importance:'',chapitres:[],source_origin:['atomisation','master_quotes.md'],arbitrage:usage}});
    }
  }
  return rows;
}

async function loadQuotes() {
  try {
    const [fallbackQuotes, registry, masterQuotesMd] = await Promise.all([
      loadJson('../../exports/generated/quotes.json', []),
      loadJson('../../data/registre.json', []),
      loadText('../../registers/quotes/master_quotes.md', '')
    ]);
    sourceLabels = buildSourceLabels(registry);
    const consolidated = parseConsolidatedQuotesMarkdown(masterQuotesMd);
    quotes = consolidated.length ? consolidated : fallbackQuotes;
    populateFilters();
    renderQuotes(quotes);
    statusCard.textContent = `${quotes.length} citation(s) consolidée(s) chargée(s)`;
  } catch (error) {console.error(error);statusCard.textContent = 'Erreur lors du chargement du registre consolidé des citations.';}
}
function uniqueValues(values) {return [...new Set(values.filter(Boolean))].sort((a,b)=>a.localeCompare(b,undefined,{numeric:true}));}
function populateSelect(select, values, labeler=(v)=>v) {select.innerHTML = select.querySelector('option') ? '<option value="">Toutes</option>' : '';values.forEach(value => {const option = document.createElement('option');option.value = value;option.textContent = labeler(value);select.appendChild(option);});}
function populateFilters() {populateSelect(sourceFilter, uniqueValues(quotes.map(q => normalizeSourceId(q.data?.source_id))), sourceLabel);populateSelect(statusFilter, uniqueValues(quotes.map(q => normalizeStatus(q.data?.statut_verification))));populateSelect(importanceFilter, uniqueValues(quotes.map(q => q.data?.importance)));const chapters = uniqueValues(quotes.flatMap(q => q.data?.chapitres || []));populateSelect(chapterFilter, chapters);}
function normalizeStatus(status) {if (!status) return '';if (typeof status === 'string') return status;return Object.values(status).join(' · ');}
function renderQuotes(items) {quotesBody.innerHTML = '';resultsMeta.textContent = `${items.length} résultat(s)`;items.forEach(item => {const data = item.data || {};const sourceId = normalizeSourceId(data.source_id);const row = document.createElement('tr');row.innerHTML = `<td><strong>${item.id}</strong></td><td>${sourceLabel(sourceId)}</td><td>${data.citation_originale || ''}</td><td>${data.traduction_editoriale_fr || data.usage_recommande || ''}</td><td>${data.page_pdf || ''}</td><td>${data.importance || ''}</td><td class="small">${normalizeStatus(data.statut_verification || data.statut_consolidation)}</td><td class="small">${(data.chapitres || []).join('<br>')}</td><td class="small"><code>${item.file}</code></td>`;quotesBody.appendChild(row);});}
function filterQuotes() {const query = searchInput.value.toLowerCase();const source = sourceFilter.value;const status = statusFilter.value;const importance = importanceFilter.value;const chapter = chapterFilter.value;const filtered = quotes.filter(item => {const data = item.data || {};const sourceId = normalizeSourceId(data.source_id);const haystack = [item.id,sourceId,sourceLabel(sourceId),data.citation_originale,data.traduction_editoriale_fr,data.usage_recommande,data.arbitrage,data.auteur_citation,data.source_citation,...(data.chapitres || [])].join(' ').toLowerCase();return (!query || haystack.includes(query))&&(!source || sourceId === source)&&(!status || normalizeStatus(data.statut_verification || data.statut_consolidation).includes(status))&&(!importance || data.importance === importance)&&(!chapter || (data.chapitres || []).includes(chapter));});renderQuotes(filtered);}
function exportCSV() {const rows = [['id','source','citation_originale','traduction_editoriale_fr','page_pdf','importance','statut_verification']];document.querySelectorAll('#quotes-body tr').forEach(tr => {const cols = [...tr.querySelectorAll('td')].map(td => td.innerText.replace(/\n/g,' | '));rows.push(cols.slice(0,7));});const csv = rows.map(row => row.map(value => `"${String(value).replace(/"/g,'""')}"`).join(',')).join('\n');const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });const url = URL.createObjectURL(blob);const link = document.createElement('a');link.href = url;link.download = 'registre_citations_consolide.csv';link.click();URL.revokeObjectURL(url);}
[searchInput, sourceFilter, statusFilter, importanceFilter, chapterFilter].forEach(element => element.addEventListener('input', filterQuotes));
resetButton.addEventListener('click', () => {searchInput.value='';sourceFilter.value='';statusFilter.value='';importanceFilter.value='';chapterFilter.value='';renderQuotes(quotes);});
downloadButton.addEventListener('click', exportCSV);
loadQuotes();
