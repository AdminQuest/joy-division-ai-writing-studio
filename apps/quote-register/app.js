/* Registre des citations — page documentaire (étape 8c).
   Réutilise le gabarit éprouvé des registres chansons / concerts (hero, toolbar,
   sections, grille .songs-list, .song-card, .song-badge, .trace). Une carte par
   citation, GROUPÉE PAR SOURCE (pas de date d'énonciation → la source est le
   regroupement naturel), triée par id.

   PLOMBERIE — source unique de vérité. La curation des citations (texte
   canonique, type verbatim/paraphrase/concept, rôles d'attribution locuteur /
   auteur_source / rapporteur, flags) est DÉRIVÉE par le build
   (build_registers.normalize_quote_record) et matérialisée dans l'export
   exports/generated/quotes.json. Pour garantir la parité EXACTE build ↔ page
   (et éviter une 2ᵉ implémentation de la curation qui dériverait), la page lit
   cet export généré plutôt que de re-dériver côté client. Lecture seule ; aucune
   donnée modifiée ; le loader partagé n'est pas touché (jeton ?v=7c inchangé).
   Le loader fournit seulement les libellés de source et les helpers texte. */

const REPO = 'AdminQuest/joy-division-ai-writing-studio';
const BRANCH = 'main';
// CACHE-BUSTING DE L'EXPORT — CONVENTION. quotes.json est un asset statique
// servi par GitHub Pages / raw, soumis au même cache collant que le loader
// partagé (cf. incident concerts 7c : page vide servie depuis le cache). On
// versionne donc le fetch par un jeton ?v=. BUMPER ce jeton à CHAQUE
// régénération significative de l'export (ou changement du loader), afin qu'un
// rebuild des données se propage au lieu d'afficher des citations périmées.
// `cache: 'no-store'` force la revalidation navigateur ; le jeton ?v= invalide
// le cache CDN de Pages. Jeton courant : v=8.
const QUOTES_EXPORT_VERSION = '8';
const QUOTES_URL = `https://raw.githubusercontent.com/${REPO}/${BRANCH}/exports/generated/quotes.json?v=${QUOTES_EXPORT_VERSION}`;

const sectionsEl = document.getElementById('quotes-sections');
const statusCard = document.getElementById('status-card');
const resultsMeta = document.getElementById('results-meta');
const searchInput = document.getElementById('search');
const sourceFilter = document.getElementById('source-filter');
const typeControls = document.getElementById('type-controls');
const resetButton = document.getElementById('reset-filters');
const downloadButton = document.getElementById('download-csv');

let records = [];     // tous les enregistrements kind 'quote' (curés, export)
let display = [];      // cartes affichables (doublon same_as replié)
let sourceLabels = {};

const T = v => DynamicRegisters.text(v);
const A = v => DynamicRegisters.array(v);
const U = v => DynamicRegisters.uniq(v);
const esc = s => T(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const sourceLabel = id => sourceLabels[id] || id || '';

// ── Champs curés (présents dans l'export ; replis défensifs si export ancien) ──
const sourceId = d => T(d.source_id) || (/(?:CIT-)?(S\d+)/.exec(T(d.id)) || [])[1] || '';
// Repli de texte : champ canonique `texte` d'abord (étape 8b-1), puis champs
// legacy — 0 carte vide ; les fiches-pointeur affichent « (non transcrit) ».
const texteOf = d => T(d.texte) || T(d.citation) || T(d.citation_directe) || T(d.citation_originale) || T(d.passage) || '(non transcrit)';
const typeOf = d => { const t = T(d.type); return /^(verbatim|paraphrase|concept)$/.test(t) ? t : 'verbatim'; };
const locuteurOf = d => T(d.locuteur) || 'anonyme';
const pageOf = d => { const p = T(d.page); return p && p !== 'inconnue' ? p : ''; };

// ── Type : verbatim ON ; paraphrase / concept togglables (tous ON au départ) ──
const TYPE_META = {
  verbatim:   { label: 'Verbatim',   on: true },
  paraphrase: { label: 'Paraphrase', on: true },
  concept:    { label: 'Concept',    on: true }
};
const TYPE_ORDER = ['verbatim', 'paraphrase', 'concept'];
let typeState = {};

// ── Chargement de l'export curé ─────────────────────────────────────────────
async function loadQuotes() {
  try {
    sourceLabels = await DynamicRegisters.sourceLabels().catch(() => ({}));
    const raw = await fetch(QUOTES_URL, { cache: 'no-store' }).then(r => {
      if (!r.ok) throw new Error(`quotes.json ${r.status}`);
      return r.json();
    });
    records = (Array.isArray(raw) ? raw : []).filter(r => r && r.id);
    resolveSameAs();
    buildTypeControls();
    populateFilters();
    apply();
    const folded = records.length - display.length;
    statusCard.textContent = `${display.length} citations curées (${records.length} records, ${folded} doublon[s] replié[s] par same_as) — groupées par source ; identité source + ordinal conservée.`;
  } catch (error) {
    console.error(error);
    statusCard.textContent = 'Erreur lors du chargement du registre des citations : ' + error.message;
  }
}

// Une carte par citation. Tout record portant `same_as: <id>` (le doublon
// déprécié) est REPLIÉ dans la carte de son retenu (traçabilité) et n'apparaît
// jamais comme carte autonome — miroir de la résolution des concerts.
function resolveSameAs() {
  const byId = new Map(records.map(r => [T(r.id), r]));
  const folded = new Map();   // memberId -> retained record
  records.forEach(r => {
    const tgt = T((r.data || {}).same_as);
    if (tgt && byId.has(tgt) && tgt !== T(r.id)) folded.set(T(r.id), byId.get(tgt));
  });
  records.forEach(r => {
    r._members = [];
    if (folded.has(T(r.id))) return;
    // Attache les membres repliés pointant vers ce record.
    r._members = records.filter(m => folded.get(T(m.id)) === r);
  });
  display = records.filter(r => !folded.has(T(r.id)));
  display.sort((a, b) => T(a.id).localeCompare(T(b.id), undefined, { numeric: true }));
}

// ── Filtres / toggles ───────────────────────────────────────────────────────
function addOptions(select, values, labeler = v => v) {
  const cur = select.value;
  select.innerHTML = '<option value="">Toutes</option>';
  values.forEach(value => {
    const o = document.createElement('option');
    o.value = value; o.textContent = labeler(value);
    select.appendChild(o);
  });
  if (values.includes(cur)) select.value = cur;
}
function populateFilters() {
  const sources = U(display.map(r => sourceId(r.data)).filter(Boolean));
  addOptions(sourceFilter, sources, id => sourceLabel(id) || id);
}
function buildTypeControls() {
  typeControls.innerHTML = '';
  const counts = {};
  display.forEach(r => { const t = typeOf(r.data); counts[t] = (counts[t] || 0) + 1; });
  TYPE_ORDER.forEach(key => {
    if (!(key in typeState)) typeState[key] = TYPE_META[key].on;
    const id = 'type-' + key;
    const wrap = document.createElement('label');
    wrap.className = 'layer-toggle layer-toggle--' + key + (typeState[key] ? ' is-on' : '');
    wrap.htmlFor = id;
    wrap.innerHTML =
      `<input type="checkbox" id="${id}" ${typeState[key] ? 'checked' : ''}>` +
      `<span class="layer-toggle__dot" aria-hidden="true"></span>` +
      `<span class="layer-toggle__name">${esc(TYPE_META[key].label)}<span class="layer-toggle__count">${counts[key] || 0}</span></span>`;
    wrap.querySelector('input').addEventListener('change', e => {
      typeState[key] = e.target.checked;
      wrap.classList.toggle('is-on', e.target.checked);
      apply();
    });
    typeControls.appendChild(wrap);
  });
}

// Recherche : indexe texte + locuteur + auteur_source + rapporteur + source + id.
function haystack(r) {
  const d = r.data || {};
  const sid = sourceId(d);
  return [r.id, texteOf(d), locuteurOf(d), T(d.auteur_source), T(d.rapporteur), sid, sourceLabel(sid),
    ...(r._members || []).map(m => T(m.id) + ' ' + texteOf(m.data || {}))]
    .map(T).join(' ').toLowerCase();
}
function apply() {
  const q = searchInput.value.toLowerCase().trim();
  const src = sourceFilter.value;
  const filtered = display.filter(r => {
    const d = r.data || {};
    if (!typeState[typeOf(d)]) return false;
    if (src && sourceId(d) !== src) return false;
    if (q && !haystack(r).includes(q)) return false;
    return true;
  });
  render(filtered);
}

// ── Rendu : sections par source, grille de .song-card ───────────────────────
function membersHtml(r) {
  const members = (r._members || []).filter(m => m && m.data);
  if (!members.length) return '';
  const rows = members.map(m => {
    const d = m.data || {};
    return `<li><code>${esc(m.id)}</code><span class="member__label">${esc(sourceLabel(sourceId(d)))} — « ${esc(texteOf(d))} »</span></li>`;
  }).join('');
  return `<details class="trace"><summary>${members.length} doublon(s) replié(s) · same_as</summary>`
    + `<ul class="member-list">${rows}</ul></details>`;
}
function flagsHtml(d) {
  const flags = [];
  if (d.attribution_a_arbitrer) flags.push(['attribution à arbitrer', 'flag--attr']);
  if (d.type_a_arbitrer) flags.push(['type à arbitrer', 'flag--type']);
  if (d.migration_concept_register) flags.push(['à migrer → concept', 'flag--concept']);
  if (d.texte_pointeur) flags.push(['fiche-pointeur', 'flag--pointer']);
  if (!flags.length) return '';
  return `<p class="quote-card__flags">` + flags.map(([t, c]) =>
    `<span class="quote-flag ${c}" title="Drapeau de curation (étape 8b-2)">${esc(t)}</span>`).join('') + `</p>`;
}
function card(r) {
  const d = r.data || {};
  const type = typeOf(d);
  const sid = sourceId(d);
  const loc = locuteurOf(d);
  const anon = loc === 'anonyme';
  const page = pageOf(d);
  const rapporteur = T(d.rapporteur);
  const auteurSrc = T(d.auteur_source);
  const pointer = !!d.texte_pointeur;

  const el = document.createElement('article');
  el.className = 'song-card quote-card quote-card--' + type + (pointer ? ' quote-card--pointer' : '');
  el.innerHTML =
    `<div class="song-card__badges">` +
      `<span class="song-badge quote-badge quote-badge--${type}">${esc(type)}</span>` +
      `<span class="song-badge song-badge--muted quote-card__speaker${anon ? ' is-anon' : ''}">${esc(loc)}</span>` +
    `</div>` +
    `<blockquote class="quote-card__text">${esc(texteOf(d))}</blockquote>` +
    (auteurSrc ? `<p class="song-card__line"><strong>Auteur-source</strong> · ${esc(auteurSrc)}</p>` : '') +
    (rapporteur ? `<p class="song-card__line"><strong>Rapporteur</strong> · ${esc(rapporteur)}</p>` : '') +
    `<p class="song-card__line song-card__prov"><strong>Provenance</strong> · ${esc(sourceLabel(sid) || sid)}` +
      (page ? ` — p. ${esc(page)}` : ` — <span class="quote-card__nopage">page inconnue</span>`) + `</p>` +
    flagsHtml(d) +
    membersHtml(r) +
    `<div class="song-card__id"><code>${esc(r.id)}</code></div>`;
  return el;
}
function render(items) {
  sectionsEl.innerHTML = '';
  resultsMeta.textContent = `${items.length} citation(s)`;
  if (!items.length) {
    sectionsEl.innerHTML = '<p class="songs-empty">Aucune citation pour ces types / filtres.</p>';
    return;
  }
  const bySource = new Map();
  items.forEach(r => { const s = sourceId(r.data) || '—'; if (!bySource.has(s)) bySource.set(s, []); bySource.get(s).push(r); });
  const frag = document.createDocumentFragment();
  [...bySource.keys()].sort((a, b) => a.localeCompare(b, undefined, { numeric: true })).forEach(sid => {
    const list = bySource.get(sid);
    const section = document.createElement('section');
    section.className = 'songs-section';
    section.innerHTML =
      `<div class="songs-section__header">` +
        `<h2 class="songs-section__title">${esc(sourceLabel(sid) || sid)}</h2>` +
        `<span class="songs-section__count">${list.length} citation(s)</span>` +
      `</div>`;
    const grid = document.createElement('div');
    grid.className = 'songs-list';
    list.forEach(r => grid.appendChild(card(r)));
    section.appendChild(grid);
    frag.appendChild(section);
  });
  sectionsEl.appendChild(frag);
}

// ── Export CSV (vue courante des cartes affichables) ────────────────────────
function exportCSV() {
  const rows = [['id', 'source_id', 'source', 'type', 'locuteur', 'auteur_source', 'rapporteur', 'page', 'texte', 'same_as_membres']];
  display.forEach(r => {
    const d = r.data || {};
    const sid = sourceId(d);
    rows.push([r.id, sid, sourceLabel(sid), typeOf(d), locuteurOf(d), T(d.auteur_source), T(d.rapporteur),
      pageOf(d) || 'inconnue', texteOf(d), (r._members || []).map(m => T(m.id)).join(' | ')]);
  });
  const csv = rows.map(row => row.map(v => '"' + String(v == null ? '' : v).replace(/"/g, '""') + '"').join(',')).join('\n');
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'registre_citations_cure.csv';
  link.click();
  URL.revokeObjectURL(link.href);
}

[searchInput, sourceFilter].forEach(el => el.addEventListener('input', apply));
resetButton.addEventListener('click', () => {
  searchInput.value = ''; sourceFilter.value = '';
  typeState = {}; buildTypeControls(); apply();
});
downloadButton.addEventListener('click', exportCSV);
loadQuotes();
