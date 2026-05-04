let chapData=[];let atelierData=[];let registreData=[];
async function load(){
chapData=await fetch('data/chapitres.json').then(r=>r.json());
atelierData=await fetch('data/ateliers.json').then(r=>r.json());
registreData=await fetch('data/registre.json').then(r=>r.json());
chapData.forEach(c=>document.getElementById('chapitre').add(new Option(c.nom,c.id)));
atelierData.forEach(a=>document.getElementById('atelier').add(new Option(a.nom,a.id)));
}
function generate(){
const chap=chapData.find(c=>c.id===document.getElementById('chapitre').value);
const at=atelierData.find(a=>a.id===document.getElementById('atelier').value);
const input=document.getElementById('input').value;
const mode=document.getElementById('mode').value;
document.getElementById('output').value=buildPrompt({chap,at,input,mode,registre:registreData});
}
document.getElementById('generateBtn').onclick=generate;
document.getElementById('copyBtn').onclick=function(){navigator.clipboard.writeText(document.getElementById('output').value)};
load();