/* Registre des acteurs — logique d'affichage.
   Miroir de apps/song-register/app.js : groupage par catégorie, facettes
   croisées (boucle de stabilisation), "Voir plus" accessible, pictos SVG par
   catégorie, export CSV. Data lue via DynamicRegisters.

   Modèle de données : la COUCHE CANONIQUE `PERSON-` (registers/people/
   00_canonical_people.md + 00_authors_canonical.md), PAS la couche provisoire
   `PERS-*` atomisée. Le loader renvoie les deux (même kind 'person' + chemin
   people/), donc on filtre sur le préfixe d'identifiant `PERSON-`. Les
   non-personnes (pending_org / pending_concept : Bedhead, Buzzcocks, Minny Pops,
   Oz PA, HM Treasury, Happy Mondays, Perry Boys) ne sont pas des `PERSON-` et
   sont donc exclues par construction. */

const searchInput = document.getElementById('search');
const categoryFilter = document.getElementById('category-filter');
const sourceFilter = document.getElementById('source-filter');
const chapterFilter = document.getElementById('chapter-filter');
const resetButton = document.getElementById('reset-filters');
const downloadButton = document.getElementById('download-csv');
const resultsMeta = document.getElementById('results-meta');
const statusEl = document.getElementById('people-status');
const sectionsEl = document.getElementById('people-sections');

let people = [];               // entrées canoniques normalisées
let sourceLabels = {};
let attributionCounts = new Map(); // PERSON-id -> nombre de citations (attribuee_a)

const T = v => DynamicRegisters.text(v);
const A = v => DynamicRegisters.array(v);
const U = v => DynamicRegisters.uniq(v);
const sourceLabel = id => sourceLabels[id] || id || '';
// Les sources canoniques sont des racines (S41, S76…) : pas de normalisation
// atome→racine nécessaire ici (contrairement au registre chansons).
const chaptersOf = d => A(d.chapters || d.chapitres);
const esc = s => T(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const norm = value => T(value).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[’‘]/g, "'").replace(/[“”«»]/g, '').replace(/[^a-z0-9]+/g, ' ').trim();

// JSON des arêtes d'attribution (étape 9) : fichier généré, lu directement
// depuis le raw GitHub (même origine/branche que le loader partagé).
const ATTRIBUTION_URL = 'https://raw.githubusercontent.com/AdminQuest/joy-division-ai-writing-studio/main/registers/relations/attribution_edges.json';

async function loadAttributionCounts() {
  try {
    const r = await fetch(ATTRIBUTION_URL, { cache: 'no-store' });
    if (!r.ok) throw new Error('HTTP ' + r.status);
    const bundle = await r.json();
    const counts = new Map();
    (bundle.edges || []).forEach(e => {
      (e.liens || []).forEach(l => {
        // Citations attribuées = locuteur (prédicat `attribuee_a`).
        if (l.predicat === 'attribuee_a' && l.cible) {
          counts.set(l.cible, (counts.get(l.cible) || 0) + 1);
        }
      });
    });
    return counts;
  } catch (err) {
    // Dégradation gracieuse : la page rend sans le compteur de citations.
    console.warn('[people] arêtes d\'attribution indisponibles :', err);
    return new Map();
  }
}

function extractCanonicalPeople(records) {
  // Une seule entrée par identifiant canonique PERSON- ; on ignore la couche
  // provisoire PERS-* et tout enregistrement sans préfixe PERSON-.
  const byId = new Map();
  records.forEach(item => {
    const d = item.data || {};
    const id = String(d.id || item.id || '');
    if (!id.startsWith('PERSON-')) return;
    if (byId.has(id)) return; // 1er gagnant (registres canoniques, ids uniques)
    byId.set(id, {
      id,
      name: T(d.name || d.nom || d.full_name || d.person || id),
      categorie: T(d.categorie) || 'generic',
      altNames: A(d.alt_names).map(T).filter(Boolean),
      sources: U(A(d.sources)),
      chapters: U(chaptersOf(d)),
      roles: A(d.role).map(T).filter(Boolean),
      aArbitrer: d.a_arbitrer === true,
      categorieAArbitrer: d.categorie_a_arbitrer === true,
      origine: T(d.origine),
      file: item.file
    });
  });
  return [...byId.values()];
}

async function loadPeople() {
  sourceLabels = await DynamicRegisters.sourceLabels();
  const [records, counts] = await Promise.all([
    DynamicRegisters.loadRecords({ prefixes: ['registers/people/'], kinds: ['person'] }),
    loadAttributionCounts()
  ]);
  attributionCounts = counts;
  people = extractCanonicalPeople(records);
  people.sort((a, b) => T(a.name).localeCompare(T(b.name), undefined, { numeric: true }));
  statusEl.style.display = 'none';
  refreshFacets();
  render();
}

const citationCount = person => attributionCounts.get(person.id) || 0;

/* ── Filtres / facettes ─────────────────────────────────── */
function currentFilters() {
  return {
    q: searchInput.value.toLowerCase().trim(),
    category: categoryFilter.value,
    source: sourceFilter.value,
    chapter: chapterFilter.value
  };
}
// Index plein-texte : nom canonique + alt_names + rôles + sources + chapitres
// (pas de sérialisation YAML brute, pour éviter les faux positifs sur les noms
// de champs — même leçon que le registre chansons).
function searchIndex(p) {
  return [p.name, ...p.altNames, ...p.roles, ...p.sources, ...p.sources.map(sourceLabel),
    ...p.chapters, p.categorie, p.id].map(T).join(' ').toLowerCase();
}
function matches(p, f, except) {
  if (except !== 'q' && f.q && !searchIndex(p).includes(f.q)) return false;
  if (except !== 'category' && f.category && p.categorie !== f.category) return false;
  if (except !== 'source' && f.source && !p.sources.includes(f.source)) return false;
  if (except !== 'chapter' && f.chapter && !p.chapters.includes(f.chapter)) return false;
  return true;
}
// Reconstruit les options d'un select ; renvoie true si la sélection courante a
// été orpheline par le nouveau jeu d'options et a dû être effacée.
function setOptions(select, values, allLabel, labeler = v => v) {
  const cur = select.value;
  select.innerHTML = '';
  const all = document.createElement('option');
  all.value = ''; all.textContent = allLabel;
  select.appendChild(all);
  values.forEach(v => {
    const o = document.createElement('option');
    o.value = v; o.textContent = labeler(v);
    select.appendChild(o);
  });
  const cleaned = cur !== '' && !values.includes(cur);
  select.value = cleaned ? '' : cur;
  return cleaned;
}
function refreshFacets() {
  // Chaque select n'offre que les valeurs encore présentes sous les *autres*
  // filtres actifs. Effacer une sélection orpheline élargit les facettes
  // restantes : on relit currentFilters() et on répète jusqu'à un passage qui
  // n'efface rien (garde contre les boucles infinies — même motif que songs).
  for (let pass = 0; pass < 5; pass++) {
    const f = currentFilters();
    const categoryVals = PeopleIcons.order.filter(cat =>
      people.some(p => p.categorie === cat && matches(p, f, 'category')));
    let cleaned = false;
    cleaned = setOptions(categoryFilter, categoryVals, 'Toutes', PeopleIcons.label) || cleaned;
    cleaned = setOptions(sourceFilter, U(people.filter(p => matches(p, f, 'source')).flatMap(p => p.sources)).sort(), 'Toutes', sourceLabel) || cleaned;
    cleaned = setOptions(chapterFilter, U(people.filter(p => matches(p, f, 'chapter')).flatMap(p => p.chapters)).sort(undefined, { numeric: true }), 'Tous') || cleaned;
    if (!cleaned) break;
  }
}

/* ── Rendu ──────────────────────────────────────────────── */
function badges(values) {
  const v = A(values).filter(Boolean);
  return v.length ? '<div class="person-tags">' + v.map(x => '<span class="person-tag">' + esc(x) + '</span>').join('') + '</div>' : '';
}
function detail(label, content) {
  return content ? '<div class="person-detail"><p class="person-detail__label">' + esc(label) + '</p>' + content + '</div>' : '';
}
function card(p) {
  const count = citationCount(p);
  const details = detail('Autres formes du nom', badges(p.altNames))
    + detail('Sources', badges(p.sources.map(sourceLabel)))
    + detail('Chapitres', badges(p.chapters))
    + detail('Rôles observés', badges(p.roles.slice(0, 16)));

  return '<article class="person-card" id="' + esc(p.id) + '">'
    + '<div class="person-card__header">' + PeopleIcons.svg(p.categorie)
      + '<div class="person-card__heading"><h3 class="person-card__title">' + esc(p.name) + '</h3>'
      + '<p class="person-card__category">' + esc(PeopleIcons.label(p.categorie)) + '</p></div></div>'
    + '<div class="person-card__badges">'
      + (count ? '<span class="person-badge">' + count + ' citation' + (count > 1 ? 's' : '') + '</span>'
               : '<span class="person-badge person-badge--muted">aucune citation</span>')
      + (p.sources.length ? '<span class="person-badge">' + p.sources.length + ' source' + (p.sources.length > 1 ? 's' : '') + '</span>' : '')
      + (p.aArbitrer ? '<span class="person-badge person-badge--flag">à arbitrer</span>' : '')
    + '</div>'
    + (p.altNames.length ? '<p class="person-card__line"><strong>Alias :</strong> ' + esc(p.altNames.join(', ')) + '</p>' : '')
    + (details ? '<button type="button" class="person-card__more" aria-expanded="false">Voir plus</button>'
        + '<div class="person-card__details" hidden>' + details + '</div>' : '')
    + '<p class="person-card__id"><code>' + esc(p.id) + '</code></p>'
    + '</article>';
}
function render() {
  const f = currentFilters();
  const filtered = people.filter(p => matches(p, f));
  resultsMeta.textContent = filtered.length + ' acteur' + (filtered.length > 1 ? 's' : '') + ' canonique' + (filtered.length > 1 ? 's' : '');
  sectionsEl.innerHTML = '';
  if (!filtered.length) {
    sectionsEl.innerHTML = '<p class="people-empty">Aucun acteur ne correspond à ces critères.</p>';
    return;
  }
  const byCategory = new Map();
  filtered.forEach(p => {
    const cat = p.categorie || 'generic';
    if (!byCategory.has(cat)) byCategory.set(cat, []);
    byCategory.get(cat).push(p);
  });
  // Sections dans l'ordre canonique des catégories, puis catégories inattendues.
  const order = [...PeopleIcons.order, ...[...byCategory.keys()].filter(c => !PeopleIcons.order.includes(c))];
  order.forEach(cat => {
    const group = byCategory.get(cat);
    if (!group || !group.length) return;
    group.sort((a, b) => T(a.name).localeCompare(T(b.name), undefined, { numeric: true }));
    const section = document.createElement('section');
    section.className = 'people-section';
    section.innerHTML = '<div class="people-section__header">' + PeopleIcons.svg(cat)
      + '<h2 class="people-section__title">' + esc(PeopleIcons.label(cat))
      + ' <span class="people-section__count">' + group.length + '</span></h2></div>'
      + '<div class="people-list">' + group.map(card).join('') + '</div>';
    sectionsEl.appendChild(section);
  });
}

/* ── Interactions (délégation, accessibles clavier) ─────── */
sectionsEl.addEventListener('click', e => {
  const more = e.target.closest('.person-card__more');
  if (more) {
    const details = more.closest('.person-card').querySelector('.person-card__details');
    const opening = details.hasAttribute('hidden');
    details.toggleAttribute('hidden', !opening);
    more.setAttribute('aria-expanded', opening ? 'true' : 'false');
    more.textContent = opening ? 'Voir moins' : 'Voir plus';
  }
});

/* ── Export CSV (jeu filtré courant) ────────────────────── */
function exportCSV() {
  const f = currentFilters();
  const rows = [['id', 'name', 'categorie', 'alt_names', 'sources', 'chapters', 'citations_attribuees', 'a_arbitrer']];
  people.filter(p => matches(p, f)).forEach(p => {
    rows.push([p.id, p.name, p.categorie, p.altNames.join(' | '),
      p.sources.map(sourceLabel).join(' | '), p.chapters.join(' | '),
      citationCount(p), p.aArbitrer ? 'oui' : 'non']);
  });
  const csv = rows.map(r => r.map(v => '"' + String(v ?? '').replace(/"/g, '""') + '"').join(',')).join('\n');
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'joy_division_people_canonical_register.csv';
  a.click();
  URL.revokeObjectURL(a.href);
}

/* ── Événements ─────────────────────────────────────────── */
function onFilterChange() { refreshFacets(); render(); }
function resetFilters() {
  searchInput.value = ''; categoryFilter.value = ''; sourceFilter.value = ''; chapterFilter.value = '';
}
[searchInput, categoryFilter, sourceFilter, chapterFilter].forEach(el => el.addEventListener('input', onFilterChange));
resetButton.addEventListener('click', () => { resetFilters(); refreshFacets(); render(); });
downloadButton.addEventListener('click', exportCSV);

loadPeople().catch(err => {
  console.error(err);
  statusEl.style.display = '';
  statusEl.textContent = 'Erreur de chargement dynamique du registre des acteurs : ' + err.message;
});
