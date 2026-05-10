let chapData=[];
let atelierData=[];
let registreData=[];
let niveauData=[];
let corpus=[];

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

function populateSources(){
  const select=document.getElementById('sources');
  const ids=[...new Set(corpus.map(item=>item.data?.source_id).filter(Boolean))].sort();
  ids.forEach(id=>select.add(new Option(id,id)));
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
    return `- ${item.id} | ${d.auteur||'Auteur inconnu'} | ${d.titre||''} | concepts : ${(d.concepts||[]).join(', ')} | chapitres : ${(d.chapitres||[]).join(', ')}`;
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
