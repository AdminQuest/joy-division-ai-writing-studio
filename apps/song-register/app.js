const DATA_URL = '../../exports/generated/songs.json';

const songsList = document.getElementById('songs-list');
const resultsMeta = document.getElementById('results-meta');
const statusCard = document.getElementById('status-card');
const searchInput = document.getElementById('search');
const sourceFilter = document.getElementById('source-filter');
const typeFilter = document.getElementById('type-filter');
const themeFilter = document.getElementById('theme-filter');
const chapterFilter = document.getElementById('chapter-filter');

let songs = [];
let sourceLabels = {};
const SOURCE_ID_ALIASES = {'S-BROLL-JOY-001':'S68'};
const FALLBACK_SOURCE_LABELS = {S41:'S41 — Hook, Unknown Pleasures, 2012',S45:'S45 — Curtis, Touching from a Distance, 1995',S46:'S46 — Johnson, An Ideal for Living, 1984',S47:'S47 — West, Joy Division, 1983',S68:'S68 — Broll, Joy Division, s.d.'};
function normalizeSourceId(id){return SOURCE_ID_ALIASES[id] || id || ''}
function sourceLabel(id){const n=normalizeSourceId(id);return sourceLabels[n] || sourceLabels[id] || n}
async function loadJson(path,fallback){try{const r=await fetch(path,{cache:'no-store'});if(!r.ok)throw new Error(`${path} ${r.status}`);return await r.json()}catch(e){console.warn('Fallback',path,e);return fallback||[]}}
function buildSourceLabels(registry){const labels={...FALLBACK_SOURCE_LABELS};registry.forEach(entry=>{const id=normalizeSourceId(entry.id||entry.source_id);if(!id)return;labels[id]=entry.source_label||labels[id]||id;if(entry.legacy_id)labels[entry.legacy_id]=labels[id]});return labels}
function sourceIds(item){return (item.data?.sources||[]).map(normalizeSourceId).filter(Boolean)}

Promise.all([loadJson(DATA_URL,[]),loadJson('../../data/registre.json',[])])
  .then(([data,registry]) => {
    sourceLabels = buildSourceLabels(registry);
    songs = data.filter(x => x.data && x.data.song);
    hydrateFilters(songs);
    render(songs);
    statusCard.textContent = `${songs.length} chansons indexées.`;
  })
  .catch(err => {console.error(err);statusCard.textContent = 'Erreur de chargement du registre.';});

function hydrateFilters(items) {
  fill(sourceFilter, collectSources(items), sourceLabel);
  fill(typeFilter, collect(items, 'type'));
  fill(themeFilter, collect(items, 'themes'));
  fill(chapterFilter, collect(items, 'chapters'));
}
function collect(items, key) {return [...new Set(items.flatMap(x => x.data[key] || []))].sort();}
function collectSources(items){return [...new Set(items.flatMap(sourceIds))].sort((a,b)=>a.localeCompare(b,undefined,{numeric:true}));}
function fill(select, values, labeler=(v)=>v) {select.innerHTML=select.querySelector('option')?'<option value="">Tous</option>':'';values.forEach(v => {const opt=document.createElement('option');opt.value=v;opt.textContent=labeler(v);select.appendChild(opt);});}
function render(items) {
  songsList.innerHTML = '';resultsMeta.textContent = `${items.length} résultat(s)`;
  items.forEach(item => {const d=item.data;const ids=sourceIds(item);const card=document.createElement('article');card.className='song-card';card.innerHTML=`
      <h3>${d.song}</h3>
      <div class="meta">${(d.type || []).map(x => `<span class="badge">${x}</span>`).join('')}${d.period ? `<span class="badge">${d.period}</span>` : ''}${d.certainty ? `<span class="badge">certitude : ${d.certainty}</span>` : ''}</div>
      ${section('Thèmes', list(d.themes))}
      ${section('Mots-clés', list(d.keywords))}
      ${section('Auteurs', list(d.writers))}
      ${section('Production', production(d.production))}
      ${section('Historique live', live(d.live_history))}
      ${section('Paroles / motifs', lyrics(d.lyrics))}
      ${section('Sources', list(ids.map(sourceLabel)))}
      ${section('Atomes liés', list(d.related_atoms))}
      ${section('Citations liées', list(d.related_quotes))}
      ${section('Chapitres', list(d.chapters))}
      ${section('Contradictions', list(d.contradictions))}
      ${d.notes ? `<div class="section-title">Notes</div><p>${d.notes}</p>` : ''}`;songsList.appendChild(card);});
}
function section(title, content) {if (!content || content === '<ul></ul>') return '';return `<div class="section-title">${title}</div>${content}`;}
function list(arr) {if (!arr || !arr.length) return '';return `<ul>${arr.map(x => `<li>${x}</li>`).join('')}</ul>`;}
function production(p) {if (!p) return '';const rows=[];if(p.producer)rows.push(`<li><strong>Producteur :</strong> ${p.producer.join(', ')}</li>`);if(p.label)rows.push(`<li><strong>Label :</strong> ${p.label.join(', ')}</li>`);if(p.sound_characteristics)rows.push(`<li><strong>Son :</strong> ${p.sound_characteristics.join(', ')}</li>`);return `<ul>${rows.join('')}</ul>`;}
function live(l) {if (!l) return '';const rows=[];if(l.important_performances)rows.push(`<li><strong>Performances :</strong> ${l.important_performances.join(', ')}</li>`);if(l.observations)rows.push(`<li><strong>Observations :</strong> ${l.observations.join(', ')}</li>`);return `<ul>${rows.join('')}</ul>`;}
function lyrics(l) {if (!l) return '';const rows=[];if(l.notable_lines)rows.push(`<li><strong>Lignes notables :</strong> ${l.notable_lines.join(' / ')}</li>`);if(l.recurring_motifs)rows.push(`<li><strong>Motifs :</strong> ${l.recurring_motifs.join(', ')}</li>`);return `<ul>${rows.join('')}</ul>`;}
function applyFilters() {const q=searchInput.value.toLowerCase();const filtered=songs.filter(item=>{const d=item.data;const ids=sourceIds(item);const haystack=[JSON.stringify(d),...ids,...ids.map(sourceLabel)].join(' ').toLowerCase();return (!q||haystack.includes(q))&&(!sourceFilter.value||ids.includes(sourceFilter.value))&&(!typeFilter.value||(d.type||[]).includes(typeFilter.value))&&(!themeFilter.value||(d.themes||[]).includes(themeFilter.value))&&(!chapterFilter.value||(d.chapters||[]).includes(chapterFilter.value));});render(filtered);}
[searchInput, sourceFilter, typeFilter, themeFilter, chapterFilter].forEach(el => el.addEventListener('input', applyFilters));
document.getElementById('reset-filters').addEventListener('click', () => {searchInput.value='';sourceFilter.value='';typeFilter.value='';themeFilter.value='';chapterFilter.value='';render(songs);});
document.getElementById('download-csv').addEventListener('click', () => {const rows=songs.map(s=>({song:s.data.song,period:s.data.period,themes:(s.data.themes||[]).join('; '),sources:sourceIds(s).map(sourceLabel).join('; '),chapters:(s.data.chapters||[]).join('; ')}));const header=Object.keys(rows[0]||{}).join(',');const body=rows.map(r=>Object.values(r).map(v=>`"${String(v||'').replaceAll('"','""')}"`).join(',')).join('\n');const blob=new Blob([header+'\n'+body],{type:'text/csv;charset=utf-8;'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='joy_division_songs_register.csv';a.click();});
