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
const SOURCE_ID_ALIASES = {'S-BROLL-JOY-001':'S68'};
const FALLBACK_SOURCE_LABELS = {S41:'S41 — Hook, Unknown Pleasures, 2012',S45:'S45 — Curtis, Touching from a Distance, 1995',S46:'S46 — Johnson, An Ideal for Living, 1984',S47:'S47 — West, Joy Division, 1983',S68:'S68 — Broll, Joy Division, s.d.'};
function normalizeSourceId(id){return SOURCE_ID_ALIASES[id] || id || ''}
function sourceLabel(id){const n=normalizeSourceId(id);return sourceLabels[n] || sourceLabels[id] || n}
async function loadJson(path,fallback){try{const r=await fetch(path,{cache:'no-store'});if(!r.ok)throw new Error(`${path} ${r.status}`);return await r.json()}catch(e){console.warn('Fallback',path,e);return fallback||[]}}
function buildSourceLabels(registry){const labels={...FALLBACK_SOURCE_LABELS};registry.forEach(entry=>{const id=normalizeSourceId(entry.id||entry.source_id);if(!id)return;labels[id]=entry.source_label||labels[id]||id;if(entry.legacy_id)labels[entry.legacy_id]=labels[id]});return labels}
function asText(value) {return value === null || value === undefined ? '' : String(value)}
function eventDate(item) {return asText(item?.data?.date)}

async function loadChronology() {
  try {
    const [loadedEvents, registry] = await Promise.all([
      loadJson('../../exports/generated/chronology.json', []),
      loadJson('../../data/registre.json', [])
    ]);
    events = loadedEvents;
    sourceLabels = buildSourceLabels(registry);
    events.sort((a, b) => eventDate(a).localeCompare(eventDate(b)));
    populateFilters();
    renderEvents(events);
    statusCard.textContent = `${events.length} événement(s) chargés`;
  } catch (error) {
    console.error(error);
    statusCard.textContent = `Erreur lors du chargement de la chronologie : ${error.message}`;
  }
}

function unique(values) {return [...new Set(values.map(asText).filter(Boolean))].sort((a,b)=>a.localeCompare(b,undefined,{numeric:true}))}
function addOptions(select, values, labeler=(v)=>v) {select.innerHTML = select.querySelector('option') ? '<option value="">Tous</option>' : '';values.forEach(value => {const option=document.createElement('option');option.value=value;option.textContent=labeler(value);select.appendChild(option);});}
function sourceIds(item){return (item.data?.sources||[]).map(normalizeSourceId).filter(Boolean)}
function populateFilters() {
  addOptions(yearFilter, unique(events.map(e => eventDate(e).slice(0, 4))));
  addOptions(typeFilter, unique(events.map(e => e.data?.type)));
  addOptions(locationFilter, unique(events.map(e => e.data?.location)));
  addOptions(sourceFilter, unique(events.flatMap(sourceIds)), sourceLabel);
}

function renderEvents(items) {
  timeline.innerHTML = '';
  resultsMeta.textContent = `${items.length} résultat(s)`;
  items.forEach(item => {
    const data = item.data || {};
    const date = eventDate(item);
    const block = document.createElement('article');
    block.className = 'timeline-item';
    const people = (data.people || []).map(p => `<li>${asText(p)}</li>`).join('');
    const songs = (data.songs || []).map(s => `<li>${asText(s)}</li>`).join('');
    const sources = sourceIds(item).map(s => `<span class="badge">${sourceLabel(s)}</span>`).join('');
    block.innerHTML = `
      <div class="timeline-date">${date || 'Date inconnue'}</div>
      <div class="timeline-event">${data.event || ''}</div>
      <div class="timeline-meta">
        <span class="badge">${data.type || 'type inconnu'}</span>
        <span class="badge">${data.location || 'lieu inconnu'}</span>
        <span class="badge">${data.precision_date || 'précision inconnue'}</span>
        <span class="badge">certitude : ${data.certainty || 'non précisée'}</span>
      </div>
      <div class="timeline-meta">${sources}</div>
      <div class="timeline-lists">
        <div><h4>Personnes</h4><ul>${people || '<li>—</li>'}</ul></div>
        <div><h4>Chansons</h4><ul>${songs || '<li>—</li>'}</ul></div>
      </div>`;
    timeline.appendChild(block);
  });
}

function filterEvents() {
  const query = searchInput.value.toLowerCase();
  const year = yearFilter.value;
  const type = typeFilter.value;
  const location = locationFilter.value;
  const source = sourceFilter.value;
  const filtered = events.filter(item => {
    const data = item.data || {};
    const date = eventDate(item);
    const ids = sourceIds(item);
    const haystack = [item.id,date,data.event,data.type,data.location,...(data.people || []),...(data.songs || []),...ids,...ids.map(sourceLabel)].map(asText).join(' ').toLowerCase();
    return (!query || haystack.includes(query))
      && (!year || date.startsWith(year))
      && (!type || data.type === type)
      && (!location || data.location === location)
      && (!source || ids.includes(source));
  });
  renderEvents(filtered);
}

function exportCSV() {
  const rows = [['id', 'date', 'event', 'type', 'location', 'people', 'songs', 'sources']];
  [...document.querySelectorAll('.timeline-item')].forEach(node => {
    const date=node.querySelector('.timeline-date')?.innerText||'';
    const event=node.querySelector('.timeline-event')?.innerText||'';
    const match=events.find(item=>eventDate(item)===date&&(item.data?.event||'')===event);
    if(!match)return;const data=match.data||{};
    rows.push([match.id,eventDate(match),data.event,data.type,data.location,(data.people||[]).join(' | '),(data.songs||[]).join(' | '),sourceIds(match).map(sourceLabel).join(' | ')]);
  });
  const csv = rows.map(row => row.map(v => `"${String(v || '').replace(/"/g, '""')}"`).join(',')).join('\n');
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');link.href = url;link.download = 'registre_chronologique.csv';link.click();URL.revokeObjectURL(url);
}
[searchInput, yearFilter, typeFilter, locationFilter, sourceFilter].forEach(el => el.addEventListener('input', filterEvents));
resetButton.addEventListener('click', () => {searchInput.value='';yearFilter.value='';typeFilter.value='';locationFilter.value='';sourceFilter.value='';renderEvents(events);});
downloadButton.addEventListener('click', exportCSV);
loadChronology();
