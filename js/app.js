async function load(){
const c=await fetch('data/chapitres.json').then(r=>r.json());
const a=await fetch('data/ateliers.json').then(r=>r.json());
c.forEach(x=>chapitre.add(new Option(x.nom,x.id)));
a.forEach(x=>atelier.add(new Option(x.nom,x.id)));
}
function generate(){
output.textContent=`Chapitre: ${chapitre.value}\nAtelier: ${atelier.value}\n\n${input.value}`;
}
load();