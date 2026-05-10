const peopleList = document.getElementById('people-list');
const statusCard = document.getElementById('status-card');
const resultsMeta = document.getElementById('results-meta');

const searchInput = document.getElementById('search');
const sourceFilter = document.getElementById('source-filter');
const roleFilter = document.getElementById('role-filter');
const entityFilter = document.getElementById('entity-filter');
const chapterFilter = document.getElementById('chapter-filter');
const resetButton = document.getElementById('reset-filters');
const downloadButton = document.getElementById('download-csv');

let people = [];

function text(v){return v===undefined||v===null?'':String(v)}
function uniq(arr){return [...new Set(arr.filter(Boolean).map(text))].sort()}

async function loadPeople(){
  try{
    const response = await fetch('../../exports/generated/people.json');
    if(!response.ok) throw new Error(`people.json introuvable (${response.status})`);

    people = await response.json();

    populateFilters();
    renderPeople(people);

    statusCard.textContent = `${people.length} acteur(s) chargé(s)`;
  }catch(error){
    console.error(error);
    statusCard.textContent = `Erreur lors du chargement des acteurs : ${error.message}`;
  }
}

function addOptions(select, values){
  values.forEach(value=>{
    const option = document.createElement('option');
    option.value = value;
    option.textContent = value;
    select.appendChild(option);
  });
}

function populateFilters(){
  addOptions(sourceFilter, uniq(people.flatMap(p=>p.data?.sources||[])));
  addOptions(roleFilter, uniq(people.flatMap(p=>p.data?.role||[])));
  addOptions(entityFilter, uniq(people.flatMap(p=>p.data?.associated_entities||[])));
  addOptions(chapterFilter, uniq(people.flatMap(p=>p.data?.chapters||[])));
}

function badges(values){
  return (values||[]).map(v=>`<span class="badge">${text(v)}</span>`).join('');
}

function list(values){
  if(!values || !values.length) return '<li>—</li>';
  return values.map(v=>`<li>${text(v)}</li>`).join('');
}

function renderPeople(items){
  peopleList.innerHTML = '';
  resultsMeta.textContent = `${items.length} résultat(s)`;

  items.forEach(item=>{
    const data = item.data || {};

    const card = document.createElement('article');
    card.className = 'person-card';

    card.innerHTML = `
      <div class="person-header">
        <div>
          <div class="person-name">${text(data.name)}</div>
          <div class="person-period">${text(data.full_name)} · ${text(data.period)}</div>
        </div>

        <div>
          <code>${text(item.id)}</code>
        </div>
      </div>

      <div class="badges">
        ${badges(data.role)}
      </div>

      <div class="badges">
        ${badges(data.sources)}
      </div>

      <div class="columns">
        <div>
          <h4>Entités associées</h4>
          <ul>${list(data.associated_entities)}</ul>

          <h4>Chansons liées</h4>
          <ul>${list(data.related_songs)}</ul>

          <h4>Événements liés</h4>
          <ul>${list(data.related_events)}</ul>
        </div>

        <div>
          <h4>Contradictions</h4>
          <ul>${list(data.contradictions)}</ul>

          <h4>Précautions méthodologiques</h4>
          <ul>${list(data.methodological_warnings)}</ul>

          <h4>Chapitres</h4>
          <ul>${list(data.chapters)}</ul>
        </div>
      </div>

      <div class="notes">
        <strong>Notes :</strong><br>
        ${text(data.notes)}
      </div>
    `;

    peopleList.appendChild(card);
  });
}

function filterPeople(){
  const query = searchInput.value.toLowerCase();
  const source = sourceFilter.value;
  const role = roleFilter.value;
  const entity = entityFilter.value;
  const chapter = chapterFilter.value;

  const filtered = people.filter(item=>{
    const data = item.data || {};

    const haystack = [
      item.id,
      data.name,
      data.full_name,
      data.period,
      data.notes,
      ...(data.role||[]),
      ...(data.sources||[]),
      ...(data.associated_entities||[]),
      ...(data.related_songs||[]),
      ...(data.chapters||[]),
      ...(data.contradictions||[])
    ].map(text).join(' ').toLowerCase();

    const q = !query || haystack.includes(query);
    const s = !source || (data.sources||[]).includes(source);
    const r = !role || (data.role||[]).includes(role);
    const e = !entity || (data.associated_entities||[]).includes(entity);
    const c = !chapter || (data.chapters||[]).includes(chapter);

    return q && s && r && e && c;
  });

  renderPeople(filtered);
}

function exportCSV(){
  const rows = [[
    'id','name','full_name','period','roles','sources','entities','songs','chapters'
  ]];

  const visible = [...document.querySelectorAll('.person-card code')].map(el=>el.innerText);

  visible.forEach(id=>{
    const item = people.find(p=>p.id===id);
    if(!item) return;

    const data = item.data || {};

    rows.push([
      item.id,
      text(data.name),
      text(data.full_name),
      text(data.period),
      (data.role||[]).join(' | '),
      (data.sources||[]).join(' | '),
      (data.associated_entities||[]).join(' | '),
      (data.related_songs||[]).join(' | '),
      (data.chapters||[]).join(' | ')
    ]);
  });

  const csv = rows.map(r=>r.map(v=>`"${String(v||'').replace(/"/g,'""')}"`).join(',')).join('\n');

  const blob = new Blob([csv], {type:'text/csv;charset=utf-8;'});
  const url = URL.createObjectURL(blob);

  const link = document.createElement('a');
  link.href = url;
  link.download = 'registre_acteurs.csv';
  link.click();

  URL.revokeObjectURL(url);
}

[searchInput, sourceFilter, roleFilter, entityFilter, chapterFilter]
  .forEach(el=>el.addEventListener('input', filterPeople));

resetButton.addEventListener('click', ()=>{
  searchInput.value='';
  sourceFilter.value='';
  roleFilter.value='';
  entityFilter.value='';
  chapterFilter.value='';
  renderPeople(people);
});

downloadButton.addEventListener('click', exportCSV);

loadPeople();
