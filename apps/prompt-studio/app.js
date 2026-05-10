let chapData=[];
let atelierData=[];
let registreData=[];
let niveauData=[];
let corpus=[];
let sourceLabels={};

const KNOWN_SOURCE_LABELS={
  S41:'S41 — Hook, Unknown Pleasures, 2012',
  S45:'S45 — D. Curtis, Touching from a Distance, 1995',
  S46:'S46 — Johnson/Morley, An Ideal for Living, 1984',
  S47:'S47 — West, Joy Division, 1983'
};

async function loadJson(path,fallback){
  try{
    const response=await fetch(path,{cache:'no-store'});
    if(!response.ok){throw new Error(path+' non chargé');}
    return await response.json();
  }catch(error){
    console.warn('Fallback utilisé pour',path,error);
    return fallback||[];
  }
}

async function load(){
  chapData=await loadJson('../../data/chapitres.json',[]);
  atelierData=await loadJson('../../data/ateliers.json',[]);
  registreData=await loadJson('../../data/registre.json',[]);
  niveauData=await loadJson('../../data/niveaux.json',[]);
  corpus=await loadJson('../../exports/generated/all_records.json',[]);

  sourceLabels=buildSourceLabels(corpus);

  populateSelect('chapitre',chapData);
  populateSelect('atelier',atelierData);
  populateSelect('niveau',niveauData);

  populateSources();
  populateContextChapters();

  document.getElementById('corpusStatus').textContent=`${corpus.length} entrées documentaires chargées`;
}

function populateSelect(id,data){
  const select=document.getElementById(id);
  if(!select)return;
  select.innerHTML='';
  data.forEach(item=>select.add(new Option(item.nom,item.id)));
}

function compactTitle(title){
  if(!title)return '';
  return String(title)
    .replace(/^Unknown Pleasures: Inside Joy Division$/,'Unknown Pleasures')
    .replace(/^An Ideal for Living: An History of Joy Division$/,'An Ideal for Living')
    .replace(/^Touching from a Distance: Ian Curtis and Joy Division$/,'Touching from a Distance')
    .slice(0,42);
}

function compactAuthor(author){
  if(!author)return '';
  return String(author)
    .replace('Peter Hook','Hook')
    .replace('Deborah Curtis','D. Curtis')
    .replace('Mike West','West')
    .replace('Mark Johnson; Paul Morley; David Lees; Jon Wozencroft','Johnson/Morley')
    .replace('Mark Johnson','Johnson')
    .slice(0,28);
}

function findYear(data){
  const values=[data?.annee,data?.year,data?.date,data?.publication_year,data?.titre,data?.reference].filter(Boolean).join(' ');
  const match=String(values).match(/\b(19|20)\d{2}\b/);
  return match?match[0]:'';
}

function buildSourceLabels(records){
  const labels={...KNOWN_SOURCE_LABELS};

  records.forEach(item=>{
    const d=item.data||{};
    const id=d.source_id;
    if(!id||labels[id])return;

    const author=compactAuthor(d.auteur||d.author);
    const title=compactTitle(d.titre||d.title);
    const year=findYear(d);

    const parts=[id];
    const detail=[author,title,year].filter(Boolean).join(', ');
    labels[id]=detail?`${id} — ${detail}`:id;
  });

  return labels;
}

function populateSources(){
  const select=document.getElementById('sources');
  const ids=[...new Set(corpus.map(item=>item.data?.source_id).filter(Boolean))].sort();
  ids.forEach(id=>select.add(new Option(sourceLabels[id]||id,id)));
}

function populateContextChapters(){
  const select=document.getElementById('contextChapters');
  const chapters=[...new Set(corpus.flatMap(item=>item.data?.chapitres||[]))].sort();
  chapters.forEach(ch=>select.add(new Option(ch,ch)));
}

function getSelectedValues(id){
  return [...document.getElementById(id).selectedOptions].map(o=>o.value);
}

function buildContext(){
  const selectedSources=getSelectedValues('sources');
  const selectedChapters=getSelectedValues('contextChapters');
  const query=document.getElementById('contextQuery').value.toLowerCase().trim();
  const limit=parseInt(document.getElementById('contextLimit').value,10);

  let filtered=[...corpus];

  if(selectedSources.length){
    filtered=filtered.filter(item=>selectedSources.includes(item.data?.source_id));
  }

  if(selectedChapters.length){
    filtered=filtered.filter(item=>(item.data?.chapitres||[]).some(ch=>selectedChapters.includes(ch)));
  }

  if(query){
    filtered=filtered.filter(item=>JSON.stringify(item).toLowerCase().includes(query));
  }

  filtered=filtered.slice(0,limit);

  if(!filtered.length){
    return 'Aucun contexte documentaire correspondant.';
  }

  return filtered.map(item=>{
    const d=item.data||{};
    const sourceLabel=sourceLabels[d.source_id]||d.source_id||'Source inconnue';
    return `- ${item.id} | ${sourceLabel} | ${d.auteur||'Auteur inconnu'} | ${d.titre||''} | concepts : ${(d.concepts||[]).join(', ')} | chapitres : ${(d.chapitres||[]).join(', ')}`;
  }).join('\n');
}

function generate(){
  const chap=chapData.find(c=>c.id===document.getElementById('chapitre').value);
  const at=atelierData.find(a=>a.id===document.getElementById('atelier').value);
  const niveau=niveauData.find(n=>n.id===document.getElementById('niveau').value);
  const input=document.getElementById('input').value;
  const mode=document.getElementById('mode').value;
  const contexte=buildContext();

  document.getElementById('output').value=buildPrompt({
    chap,
    at,
    input,
    mode,
    registre:registreData,
    niveau,
    contexte
  });
}

document.getElementById('generateBtn').onclick=generate;
document.getElementById('copyBtn').onclick=function(){navigator.clipboard.writeText(document.getElementById('output').value)};

load();
