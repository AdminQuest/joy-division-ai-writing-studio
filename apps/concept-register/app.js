const DATA_URL='../../exports/generated/atoms.json';
const conceptsList=document.getElementById('concepts-list');
const resultsMeta=document.getElementById('results-meta');
const statusCard=document.getElementById('status-card');
const searchInput=document.getElementById('search');
const sourceFilter=document.getElementById('source-filter');
const chapterFilter=document.getElementById('chapter-filter');
const typeFilter=document.getElementById('type-filter');

let concepts=[];

fetch(DATA_URL)
.then(r=>r.json())
.then(atoms=>{
  concepts=buildConcepts(atoms);
  hydrateFilters(concepts);
  render(concepts);
  statusCard.textContent=`${concepts.length} concepts indexés.`;
})
.catch(err=>{
  console.error(err);
  statusCard.textContent='Erreur de chargement du registre des concepts.';
});

function buildConcepts(atoms){
  const map=new Map();

  atoms.forEach(atom=>{
    const d=atom.data||{};
    const concepts=d.concepts||[];

    concepts.forEach(raw=>{
      const concept=String(raw);

      if(!map.has(concept)){
        map.set(concept,{
          concept,
          occurrences:0,
          sources:new Set(),
          chapters:new Set(),
          types:new Set(),
          atoms:[]
        });
      }

      const entry=map.get(concept);

      entry.occurrences++;
      if(d.source_id) entry.sources.add(d.source_id);
      (d.chapitres||[]).forEach(c=>entry.chapters.add(c));
      if(d.type_unite) entry.types.add(d.type_unite);

      entry.atoms.push({
        id:d.id,
        heading:atom.heading,
        source:d.source_id,
        type:d.type_unite,
        file:atom.file
      });
    });
  });

  return [...map.values()]
    .sort((a,b)=>b.occurrences-a.occurrences);
}

function hydrateFilters(items){
  fill(sourceFilter,[...new Set(items.flatMap(i=>[...i.sources]))].sort());
  fill(chapterFilter,[...new Set(items.flatMap(i=>[...i.chapters]))].sort());
  fill(typeFilter,[...new Set(items.flatMap(i=>[...i.types]))].sort());
}

function fill(select,values){
  values.forEach(v=>{
    const o=document.createElement('option');
    o.value=v;
    o.textContent=v;
    select.appendChild(o);
  });
}

function render(items){
  conceptsList.innerHTML='';
  resultsMeta.textContent=`${items.length} résultat(s)`;

  items.forEach(c=>{
    const card=document.createElement('article');
    card.className='concept-card';

    card.innerHTML=`
      <h3>${c.concept}</h3>
      <div class="occurrences">${c.occurrences} occurrence(s)</div>

      <div class="section-title">Sources</div>
      <div class="meta">${[...c.sources].map(x=>`<span class="badge">${x}</span>`).join('')}</div>

      <div class="section-title">Chapitres</div>
      <div class="meta">${[...c.chapters].map(x=>`<span class="badge">${x}</span>`).join('')}</div>

      <div class="section-title">Types d’atomes</div>
      <div class="meta">${[...c.types].map(x=>`<span class="badge">${x}</span>`).join('')}</div>

      <div class="section-title">Occurrences documentaires</div>
      <ul>
        ${c.atoms.slice(0,15).map(a=>`<li><strong>${a.id}</strong> — ${a.heading} <em>(${a.source})</em></li>`).join('')}
      </ul>
    `;

    conceptsList.appendChild(card);
  });
}

function applyFilters(){
  const q=searchInput.value.toLowerCase();

  const filtered=concepts.filter(c=>{
    const haystack=[
      c.concept,
      ...c.sources,
      ...c.chapters,
      ...c.types,
      ...c.atoms.map(a=>a.heading)
    ].join(' ').toLowerCase();

    return (!q || haystack.includes(q))
      && (!sourceFilter.value || c.sources.has(sourceFilter.value))
      && (!chapterFilter.value || c.chapters.has(chapterFilter.value))
      && (!typeFilter.value || c.types.has(typeFilter.value));
  });

  render(filtered);
}

[searchInput,sourceFilter,chapterFilter,typeFilter]
.forEach(el=>el.addEventListener('input',applyFilters));

document.getElementById('reset-filters').addEventListener('click',()=>{
  searchInput.value='';
  sourceFilter.value='';
  chapterFilter.value='';
  typeFilter.value='';
  render(concepts);
});

document.getElementById('download-csv').addEventListener('click',()=>{
  const rows=concepts.map(c=>({
    concept:c.concept,
    occurrences:c.occurrences,
    sources:[...c.sources].join('; '),
    chapters:[...c.chapters].join('; '),
    types:[...c.types].join('; ')
  }));

  const header=Object.keys(rows[0]).join(',');
  const body=rows.map(r=>Object.values(r).map(v=>`"${String(v).replaceAll('"','""')}"`).join(',')).join('\n');

  const blob=new Blob([header+'\n'+body],{type:'text/csv;charset=utf-8;'});
  const a=document.createElement('a');
  a.href=URL.createObjectURL(blob);
  a.download='joy_division_concepts_register.csv';
  a.click();
});