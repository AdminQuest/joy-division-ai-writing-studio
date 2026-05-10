const STOPWORDS = new Set(['a','an','and','are','as','at','be','by','for','from','in','is','it','of','on','or','that','the','to','with','au','aux','ce','ces','dans','de','des','du','elle','en','et','il','la','le','les','pour','que','qui','sur','un','une']);
const TOKEN_RE = /[\wÀ-ÿ']+/gu;
let ALL_RECORDS = [];
let SOURCES_INDEX = [];

function flatten(value){if(value===null||value===undefined)return '';if(typeof value==='string')return value;if(typeof value==='number'||typeof value==='boolean')return String(value);if(Array.isArray(value))return value.map(flatten).join(' ');if(typeof value==='object')return Object.entries(value).map(([k,v])=>`${k} ${flatten(v)}`).join(' ');return String(value)}
function tokenize(text){return (text.toLowerCase().match(TOKEN_RE)||[]).filter(t=>t.length>2&&!STOPWORDS.has(t))}
function recordText(record){return [record.id||'',record.kind||'',record.heading||'',record.file||'',flatten(record.data||{})].join('\n').toLowerCase()}

function conciseRecord(record){const data=record.data||{};return {id:record.id,kind:record.kind,file:record.file,heading:record.heading,summary_fields:Object.fromEntries(Object.entries({source_id:data.source_id,auteur:data.auteur,titre:data.titre,pages_pdf:data.pages_pdf,type_unite:data.type_unite,concepts:data.concepts,chapitres:data.chapitres,citation_originale:data.citation_originale,traduction_editoriale_fr:data.traduction_editoriale_fr,song:data.song,themes:data.themes,name:data.name,role:data.role,date:data.date,event:data.event,certainty:data.certainty}).filter(([,v])=>v!==undefined&&v!==null&&v!==''))}}

function buildSourcesIndex(){const grouped=new Map();for(const record of ALL_RECORDS){const sourceId=record.data?.source_id;if(!sourceId)continue;if(!grouped.has(sourceId)){grouped.set(sourceId,{source_id:sourceId,titre:record.data?.titre||record.heading||sourceId,auteur:record.data?.auteur||'Inconnu',records:[],counts:{atom:0,quote:0,chronology:0,person:0,song:0,unknown:0}})}const entry=grouped.get(sourceId);entry.records.push(record);entry.counts[record.kind]=(entry.counts[record.kind]||0)+1}SOURCES_INDEX=[...grouped.values()].sort((a,b)=>a.source_id.localeCompare(b.source_id))}

function renderSources(){const container=document.getElementById('sources-list');const count=document.getElementById('sources-count');container.innerHTML='';count.textContent=`${SOURCES_INDEX.length} source(s)`;for(const source of SOURCES_INDEX){const wrapper=document.createElement('div');wrapper.className='source-entry';const button=document.createElement('button');button.innerHTML=`<div class="source-title">${source.source_id} — ${source.titre}</div><div class="source-meta">${source.auteur}<br>${source.counts.atom||0} atomes · ${source.counts.quote||0} citations · ${source.counts.chronology||0} chronologies · ${source.records.length} enregistrements</div>`;button.addEventListener('click',()=>openSource(source.source_id));wrapper.appendChild(button);container.appendChild(wrapper)}}

function openSource(sourceId){const source=SOURCES_INDEX.find(s=>s.source_id===sourceId);if(!source)return;document.getElementById('results-title').textContent=`${source.source_id} — ${source.titre}`;renderResults({total_matches:source.records.length,results:source.records.map(record=>({score:'source',record:conciseRecord(record)}))})}

async function loadCorpus(){const card=document.getElementById('status-card');try{const response=await fetch('../../exports/generated/all_records.json');if(!response.ok)throw new Error(`Impossible de charger all_records.json (${response.status})`);ALL_RECORDS=await response.json();const counts={};for(const record of ALL_RECORDS){const kind=record.kind||'unknown';counts[kind]=(counts[kind]||0)+1}const summary=Object.entries(counts).map(([k,c])=>`${k}: ${c}`).join(' · ');card.textContent=`Corpus chargé · ${ALL_RECORDS.length} enregistrements · ${summary}`;buildSourcesIndex();renderSources()}catch(error){card.textContent=`Erreur : ${error.message}`}}

function clearResults(){document.getElementById('results').innerHTML='';document.getElementById('results-meta').textContent=''}

function addField(dl,key,value){if(value===undefined||value===null||value==='')return;const dt=document.createElement('dt');dt.textContent=key;const dd=document.createElement('dd');dd.textContent=typeof value==='object'?JSON.stringify(value,null,2):value;dl.appendChild(dt);dl.appendChild(dd)}

function renderResults(data){clearResults();const results=document.getElementById('results');const meta=document.getElementById('results-meta');const template=document.getElementById('result-template');meta.textContent=`${data.total_matches} résultat(s)`;if(!data.results.length){const empty=document.createElement('div');empty.className='status-card';empty.textContent='Aucun résultat.';results.appendChild(empty);return}for(const item of data.results){const node=template.content.cloneNode(true);node.querySelector('.result-kind').textContent=item.record.kind;node.querySelector('.result-score').textContent=`${item.score}`;node.querySelector('.result-title').textContent=item.record.id;node.querySelector('.result-file').textContent=item.record.file;const fields=node.querySelector('.result-fields');for(const [key,value] of Object.entries(item.record.summary_fields)){addField(fields,key,value)}results.appendChild(node)}}

function scoreRecords(query,kind){const terms=tokenize(query);if(!terms.length)return [];const results=[];for(const record of ALL_RECORDS){if(kind&&record.kind!==kind)continue;const text=recordText(record);let score=0;for(const term of terms){const matches=text.split(term).length-1;if(matches>0)score+=matches}if(text.includes(query.toLowerCase()))score+=10;if(score>0)results.push({score,record:conciseRecord(record)})}return results.sort((a,b)=>b.score-a.score)}

async function performSearch(query,kind,top){document.getElementById('results-title').textContent='Résultats';const results=document.getElementById('results');results.innerHTML='<div class="status-card">Recherche en cours…</div>';const scored=scoreRecords(query,kind);renderResults({total_matches:scored.length,results:scored.slice(0,Number(top))})}

function bindExamples(){for(const button of document.querySelectorAll('.example-query')){button.addEventListener('click',()=>{const query=button.dataset.query;document.getElementById('query').value=query;performSearch(query,'',10)})}}

function bindForm(){const form=document.getElementById('search-form');form.addEventListener('submit',async event=>{event.preventDefault();const query=document.getElementById('query').value.trim();const kind=document.getElementById('kind').value;const top=document.getElementById('top').value;if(!query)return;await performSearch(query,kind,top)})}

loadCorpus();
bindExamples();
bindForm();