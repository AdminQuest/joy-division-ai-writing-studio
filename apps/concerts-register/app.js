/* Registre des concerts — page documentaire (étape 7c).
   Affiche les identités CANONIQUES CONCERT- (192) dédoublonnées par résolution
   same_as : une carte par identité, jamais une par membre legacy. Les membres
   réconciliés (JD-CONCERT- joydiv + CHR- chronologie) sont repliés dans la carte
   (traçabilité). Données inchangées — lecture seule via DynamicRegisters.
   Reprend d'emblée les correctifs étape 6 : inferKind concert, dédoublonnage
   same_as, recherche indexant le TEXTE des membres repliés (labels + sources,
   pas que les ids), normalisation isoDate (Date YAML cross-realm), repli label. */

const sectionsEl = document.getElementById('concerts-sections');
const statusCard = document.getElementById('status-card');
const resultsMeta = document.getElementById('results-meta');
const searchInput = document.getElementById('search');
const yearFilter = document.getElementById('year-filter');
const statusControls = document.getElementById('status-controls');
const resetButton = document.getElementById('reset-filters');
const downloadButton = document.getElementById('download-csv');

let records = [];          // tous les enregistrements kind 'concert'
let display = [];          // identités canoniques CONCERT- (cartes affichables)
let placeLabels = {};      // PLACE-id -> nom lisible
let sourceLabels = {};

const T = v => DynamicRegisters.text(v);
const A = v => DynamicRegisters.array(v);
const U = v => DynamicRegisters.uniq(v);
const sourceIds = item => DynamicRegisters.sourceIds(item);
const sourceLabel = id => sourceLabels[id] || id || '';
const esc = s => T(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

// Gabarit-placeholder du README (JD-CONCERT-YYYYMMDD-NNN) : exclu de l'ingestion,
// comme côté build. Détection sur le jeton de date factice.
const isPlaceholder = id => /YYYYMMDD|AAAAMMJJ/.test(T(id));
const isCanonical = r => /^CONCERT-/.test(T(r.id)) && !isPlaceholder(r.id);

// Repli de label : label (canonique) → notes → heading Markdown → id. Pas de carte vide.
const cleanHeading = h => T(h).replace(/^\s*(?:CONCERT|JD-CONCERT)-[A-Za-z0-9-]+\s*[—:–-]\s*/, '').trim();
const labelOf = r => {
  const d = (r && r.data) || {};
  return T(d.label) || cleanHeading(r && r.heading) || T(d.notes) || T(d.id) || 'Sans intitulé';
};

// Correctif Codex (étape 6) : une date pleine non quotée (date: 1980-05-02) est
// parsée par js-yaml en objet Date → T() la rendrait « Fri May 02 1980 … » et
// casserait humanDate / yearOf / tri / filtres / CSV. On normalise tout Date en
// ISO local AAAA-MM-JJ AVANT le repli sur T(). Détection cross-realm robuste via
// Object.prototype.toString (instanceof échoue si la Date vient d'un autre realm).
const isoDate = v => {
  if (v && Object.prototype.toString.call(v) === '[object Date]' && !isNaN(v)) {
    const p = n => String(n).padStart(2, '0');
    return `${v.getUTCFullYear()}-${p(v.getUTCMonth() + 1)}-${p(v.getUTCDate())}`;
  }
  return T(v);
};
const startDate = d => isoDate(d.date != null ? d.date : d.date_debut);
const endDate = d => isoDate(d.date_fin);
const sortKey = d => startDate(d) || endDate(d);
const yearOf = d => { const m = /^(\d{4})/.exec(sortKey(d)); return m ? m[1] : ''; };

// ── Statut : confirmé ON par défaut ; annulé / douteux OFF (toggles) ────────
const STATUS_META = {
  'confirmé':  { label: 'Confirmés', on: true },
  'annulé':    { label: 'Annulés',   on: false },
  'douteux':   { label: 'Douteux',   on: false }
};
const statusOf = d => { const s = T(d.statut).toLowerCase().trim(); return STATUS_META[s] ? s : (s || 'confirmé'); };
let statusState = {};

// ── Lieu : nom du PLACE- (registre des lieux) ; repli humanisé du slug ──────
const humanizeSlug = id => T(id).replace(/^PLACE-/, '').toLowerCase()
  .replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
const lieuName = d => { const id = T(d.lieu); if (!id) return ''; return placeLabels[id] || humanizeSlug(id); };

// ── Précision honnête (miroir exact de la frise chronologie / carte lieux) ──
function precisionBucket(d) {
  if (d.date_debut && d.date_fin) return 'intervalle';
  const raw = T(d.date_precision || d.precision_date).toLowerCase().trim();
  if (raw) {
    if (/(intervalle|range|periode|période)/.test(raw)) return 'intervalle';
    if (/(circa|approx|inferred|to_verify|decade|around|envir)/.test(raw)) return 'circa';
    if (/(saison|season|spring|summer|autumn|winter|printemps|été|ete|automne|hiver)/.test(raw)) return 'saison';
    if (/(mois|month)/.test(raw)) return 'mois';
    if (/(annee|année|year|^an$)/.test(raw)) return 'annee';
    if (/(jour|exact|day)/.test(raw)) return 'jour';
  }
  const s = startDate(d);
  if (/^\d{4}-\d{2}-\d{2}/.test(s)) return 'jour';
  if (/^\d{4}-\d{2}/.test(s)) return 'mois';
  if (/^\d{4}/.test(s)) return 'annee';
  return 'circa';
}
const PRECISION_META = {
  jour:       { tier: 'point', sigil: '',  text: 'jour précis' },
  mois:       { tier: 'short', sigil: '',  text: 'mois' },
  saison:     { tier: 'short', sigil: '~', text: 'saison' },
  annee:      { tier: 'wide',  sigil: '~', text: 'année' },
  circa:      { tier: 'wide',  sigil: '~', text: 'approximatif' },
  intervalle: { tier: 'span',  sigil: '',  text: 'intervalle' }
};
const MONTH_FR = ['', 'janv.', 'févr.', 'mars', 'avril', 'mai', 'juin', 'juill.', 'août', 'sept.', 'oct.', 'nov.', 'déc.'];
function humanDate(iso) {
  const s = T(iso);
  let m;
  if ((m = /^(\d{4})-(\d{2})-(\d{2})/.exec(s))) return `${+m[3]} ${MONTH_FR[+m[2]]} ${m[1]}`;
  if ((m = /^(\d{4})-(\d{2})/.exec(s))) return `${MONTH_FR[+m[2]]} ${m[1]}`;
  if ((m = /^(\d{4})/.exec(s))) return m[1];
  return s;
}

// ── Chargement + résolution de la colonne vertébrale ────────────────────────
async function loadConcerts() {
  try {
    sourceLabels = await DynamicRegisters.sourceLabels();
    // Lieux : on charge le registre des lieux pour afficher le NOM du PLACE-
    // (le concert ne porte que la référence). Tolérant : si indisponible, repli
    // sur le slug humanisé.
    try {
      const places = await DynamicRegisters.loadRecords({ prefixes: ['registers/places/'], kinds: ['place'] });
      places.forEach(p => { placeLabels[T(p.id)] = T(p.data.label || p.data.nom || p.data.name) || T(p.id); });
    } catch (e) { console.warn('Lieux indisponibles, repli sur le slug :', e && e.message); }

    records = await DynamicRegisters.loadRecords({
      prefixes: ['registers/concerts/'],
      kinds: ['concert']
    });
    resolveBackbone();
    buildStatusControls();
    populateFilters();
    apply();
    const cancelled = display.filter(r => statusOf(r.data) === 'annulé').length;
    statusCard.textContent = `${display.length} concerts canoniques (${display.length - cancelled} confirmés, ${cancelled} annulés) — identités dédoublonnées par réconciliation same_as ; membres joydiv + chronologie repliés en traçabilité.`;
  } catch (error) {
    console.error(error);
    statusCard.textContent = 'Erreur lors du chargement du registre des concerts : ' + error.message;
  }
}

// Une carte par IDENTITÉ canonique CONCERT-. Tout membre legacy listé dans
// `membres_reconcilies` (JD-CONCERT- joydiv ou CHR- chronologie), ou portant
// `same_as: CONCERT-…`, est REPLIÉ dans la carte de son canonique (traçabilité)
// et n'apparaît jamais comme carte autonome.
function resolveBackbone() {
  // Dédoublonnage par id (un même CONCERT-/JD-CONCERT- peut apparaître dans
  // plusieurs fichiers chargés). Priorité au canonique CONCERT-.
  const pick = (a, b) => (isCanonical(a) !== isCanonical(b)) ? (isCanonical(a) ? a : b) : a;
  const byId = new Map();
  records.forEach(r => {
    if (isPlaceholder(r.id)) return;            // gabarit README exclu
    const id = T(r.id);
    byId.set(id, byId.has(id) ? pick(byId.get(id), r) : r);
  });
  const unique = [...byId.values()];

  const foldedInto = new Map();                 // memberId -> canonical record
  unique.forEach(r => {
    if (!isCanonical(r)) return;
    A(r.data.membres_reconcilies).forEach(m => foldedInto.set(T(m), r));
  });
  unique.forEach(r => {                         // réciproque : same_as porté par le legacy
    A(r.data.same_as).map(T).filter(Boolean).forEach(t => {
      const tgt = byId.get(t);
      if (tgt && isCanonical(tgt)) foldedInto.set(T(r.id), tgt);
    });
  });
  // Attache à chaque canonique ses membres repliés (résolus ; les CHR- de la
  // chronologie ne sont pas chargés ici → repli id-seul, traçabilité conservée).
  unique.forEach(r => {
    if (!isCanonical(r)) return;
    const ids = U(A(r.data.membres_reconcilies).map(T));
    r._members = ids.map(id => byId.get(id) || { id, data: { id } });
  });
  // Affichables = identités canoniques uniquement (les legacy non repliés —
  // p. ex. un JD-CONCERT- résiduel sans canonique — ne sont pas des identités
  // de concert : exclus de l'affichage).
  display = unique.filter(isCanonical);
  display.sort((a, b) => sortKey(a.data).localeCompare(sortKey(b.data), undefined, { numeric: true }));
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
  addOptions(yearFilter, U(display.map(r => yearOf(r.data)).filter(Boolean)));
}
function presentStatuses() {
  const present = U(display.map(r => statusOf(r.data)));
  // Ordre stable : confirmé, annulé, douteux, puis éventuels autres.
  const order = ['confirmé', 'annulé', 'douteux'];
  return present.sort((a, b) => (order.indexOf(a) + 1 || 99) - (order.indexOf(b) + 1 || 99));
}
function buildStatusControls() {
  statusControls.innerHTML = '';
  const counts = {};
  display.forEach(r => { const s = statusOf(r.data); counts[s] = (counts[s] || 0) + 1; });
  presentStatuses().forEach(key => {
    if (!(key in statusState)) statusState[key] = STATUS_META[key] ? STATUS_META[key].on : false;
    const meta = STATUS_META[key] || { label: key };
    const id = 'status-' + key;
    const wrap = document.createElement('label');
    wrap.className = 'layer-toggle layer-toggle--' + (key === 'confirmé' ? 'jalon' : 'concert_a_migrer') + (statusState[key] ? ' is-on' : '');
    wrap.htmlFor = id;
    wrap.innerHTML =
      `<input type="checkbox" id="${id}" ${statusState[key] ? 'checked' : ''}>` +
      `<span class="layer-toggle__dot" aria-hidden="true"></span>` +
      `<span class="layer-toggle__name">${esc(meta.label)}<span class="layer-toggle__count">${counts[key] || 0}</span></span>`;
    wrap.querySelector('input').addEventListener('change', e => {
      statusState[key] = e.target.checked;
      wrap.classList.toggle('is-on', e.target.checked);
      apply();
    });
    statusControls.appendChild(wrap);
  });
}

// Recherche : indexe le TEXTE des membres repliés (labels + lieu + sources), pas
// seulement leurs ids — exigence Codex (étape 6), appliquée d'emblée.
function memberText(r) {
  return (r._members || []).flatMap(m => [m.id, labelOf(m), lieuName(m.data || {}), T((m.data || {}).ville),
    ...sourceIds(m), ...sourceIds(m).map(sourceLabel)]);
}
function haystack(r) {
  const d = r.data || {};
  return [r.id, labelOf(r), lieuName(d), T(d.lieu), T(d.statut), T(d.nom_tournee), startDate(d), endDate(d),
    ...A(d.membres_reconcilies), ...memberText(r), ...sourceIds(r), ...sourceIds(r).map(sourceLabel)]
    .map(T).join(' ').toLowerCase();
}
function apply() {
  const q = searchInput.value.toLowerCase().trim();
  const year = yearFilter.value;
  const filtered = display.filter(r => {
    const d = r.data || {};
    if (!statusState[statusOf(d)]) return false;
    if (year && yearOf(d) !== year) return false;
    if (q && !haystack(r).includes(q)) return false;
    return true;
  });
  render(filtered);
}

// ── Rendu : sections par année, grille de .song-card ────────────────────────
function precisionTrack(d) {
  const b = precisionBucket(d);
  const meta = PRECISION_META[b];
  if (b === 'intervalle') {
    return `<span class="prec prec--span" title="Précision : intervalle (${esc(startDate(d))} → ${esc(endDate(d))})">`
      + `<span class="prec__cap"></span><span class="prec__bar"></span><span class="prec__cap"></span></span>`;
  }
  return `<span class="prec prec--${meta.tier}" title="Précision : ${esc(meta.text)}"><span class="prec__bar"></span></span>`;
}
function membersHtml(r) {
  const members = (r._members || []).filter(m => m && m.data);
  if (!members.length) return '';
  const rows = members.map(m => {
    const extra = [labelOf(m), sourceIds(m).map(sourceLabel).join(', ')].filter(Boolean).join(' — ');
    return `<li><code>${esc(m.id)}</code><span class="member__label">${esc(extra)}</span></li>`;
  }).join('');
  return `<details class="trace"><summary>${members.length} membre(s) réconcilié(s) · traçabilité</summary>`
    + `<ul class="member-list">${rows}</ul></details>`;
}
function card(r) {
  const d = r.data || {};
  const status = statusOf(d);
  const cancelled = status === 'annulé';
  const meta = PRECISION_META[precisionBucket(d)];
  const dateText = (precisionBucket(d) === 'intervalle')
    ? `${humanDate(startDate(d))} → ${humanDate(endDate(d))}`
    : (meta.sigil || '') + humanDate(startDate(d));
  const lieu = lieuName(d);
  const tour = T(d.nom_tournee).trim();

  const el = document.createElement('article');
  el.className = 'song-card concert-card concert-card--' + (cancelled ? 'cancelled' : 'confirmed');
  el.innerHTML =
    `<div class="song-card__header">` +
      `<div class="song-card__heading">` +
        `<h3 class="song-card__title">${esc(labelOf(r))}</h3>` +
        `<p class="song-card__period"><time>${esc(dateText)}</time> ` +
          precisionTrack(d) + `<span class="concert-card__prec">${esc(meta.text)}</span></p>` +
      `</div>` +
    `</div>` +
    `<div class="song-card__badges">` +
      `<span class="song-badge concert-status concert-status--${cancelled ? 'cancelled' : 'confirmed'}">` +
        (cancelled ? 'annulé' : 'confirmé') + `</span>` +
      (tour ? `<span class="song-badge song-badge--muted">${esc(tour)}</span>` : '') +
    `</div>` +
    (lieu ? `<p class="song-card__line"><strong>Lieu</strong> · ${esc(lieu)}</p>` : '') +
    membersHtml(r) +
    `<div class="song-card__id"><code>${esc(r.id)}</code></div>`;
  return el;
}
function render(items) {
  sectionsEl.innerHTML = '';
  resultsMeta.textContent = `${items.length} concert(s)`;
  if (!items.length) {
    sectionsEl.innerHTML = '<p class="songs-empty">Aucun concert pour ces statuts / filtres.</p>';
    return;
  }
  const byYear = new Map();
  items.forEach(r => { const y = yearOf(r.data) || '—'; if (!byYear.has(y)) byYear.set(y, []); byYear.get(y).push(r); });
  const frag = document.createDocumentFragment();
  [...byYear.keys()].sort((a, b) => a.localeCompare(b, undefined, { numeric: true })).forEach(y => {
    const list = byYear.get(y);
    const section = document.createElement('section');
    section.className = 'songs-section';
    section.innerHTML =
      `<div class="songs-section__header">` +
        `<h2 class="songs-section__title">${esc(y)}</h2>` +
        `<span class="songs-section__count">${list.length} concert(s)</span>` +
      `</div>`;
    const grid = document.createElement('div');
    grid.className = 'songs-list';
    list.forEach(r => grid.appendChild(card(r)));
    section.appendChild(grid);
    frag.appendChild(section);
  });
  sectionsEl.appendChild(frag);
}

// ── Export CSV ──────────────────────────────────────────────────────────────
function exportCSV() {
  const rows = [['id', 'date', 'date_fin', 'date_precision', 'statut', 'lieu', 'lieu_nom', 'label', 'nom_tournee', 'membres_reconcilies']];
  display.forEach(r => {
    const d = r.data || {};
    rows.push([r.id, startDate(d), endDate(d), precisionBucket(d), statusOf(d), T(d.lieu), lieuName(d),
      labelOf(r), T(d.nom_tournee), A(d.membres_reconcilies).join(' | ')]);
  });
  const csv = rows.map(row => row.map(v => '"' + String(v || '').replace(/"/g, '""') + '"').join(',')).join('\n');
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'registre_concerts_canonique.csv';
  link.click();
  URL.revokeObjectURL(link.href);
}

[searchInput, yearFilter].forEach(el => el.addEventListener('input', apply));
resetButton.addEventListener('click', () => {
  searchInput.value = ''; yearFilter.value = '';
  statusState = {}; buildStatusControls(); apply();
});
downloadButton.addEventListener('click', exportCSV);
loadConcerts();
