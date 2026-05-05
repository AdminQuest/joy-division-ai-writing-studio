let chapData=[];
let atelierData=[];
let registreData=[];
let niveauData=[];

async function loadJson(path,fallback){
  try{
    const response=await fetch(path,{cache:'no-store'});
    if(!response.ok){throw new Error(path+' non chargé');}
    return await response.json();
  }catch(error){
    console.warn('Fallback utilisé pour',path);
    return fallback||[];
  }
}

async function load(){
  chapData=await loadJson('data/chapitres.json',[]);
  atelierData=await loadJson('data/ateliers.json',[]);
  registreData=await loadJson('data/registre.json',[]);
  niveauData=await loadJson('data/niveaux.json',[]);
  populateSelect('chapitre',chapData);
  populateSelect('atelier',atelierData);
  populateSelect('niveau',niveauData);
}

function populateSelect(id,data){
  const select=document.getElementById(id);
  if(!select)return;
  select.innerHTML='';
  data.forEach(item=>select.add(new Option(item.nom,item.id)));
}

function generate(){
  const chap=chapData.find(c=>c.id===document.getElementById('chapitre').value);
  const at=atelierData.find(a=>a.id===document.getElementById('atelier').value);
  const niveau=niveauData.find(n=>n.id===document.getElementById('niveau').value);
  const input=document.getElementById('input').value;
  const mode=document.getElementById('mode').value;

  document.getElementById('output').value=buildPrompt({chap,at,input,mode,registre:registreData,niveau});
}

document.getElementById('generateBtn').onclick=generate;
document.getElementById('copyBtn').onclick=function(){navigator.clipboard.writeText(document.getElementById('output').value)};
load();
