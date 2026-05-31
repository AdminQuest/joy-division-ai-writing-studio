/* Registre chronologique — frise documentaire (refonte étape 6).
   Affiche le modèle CANONIQUE : 62 jalons EVENT- dédoublonnés par résolution
   same_as (une carte par identité, jamais une par membre legacy), des beats
   (jalons nus, subordonnés), et trois couches activables (concerts à migrer,
   contexte, réception posthume). Données inchangées — lecture seule via
   DynamicRegisters. Précision honnête calquée sur geo_precision (carte lieux). */

const timeline = document.getElementById('timeline');
const statusCard = document.getElementById('status-card');
const resultsMeta = document.getElementById('results-meta');
const searchInput = document.getElementById('search');
const yearFilter = document.getElementById('year-filter');
const sourceFilter = document.getElementById('source-filter');
const resetButton = document.getElementById('reset-filters');
const downloadButton = document.getElementById('download-csv');
const layerControls = document.getElementById('layer-controls');

let records = [];        // tous les enregistrements chronology (canoniques + legacy)
let display = [];        // colonne vertébrale dédoublonnée (cartes affichables)
let sourceLabels = {};

const T = v => DynamicRegisters.text(v);
const A = v => DynamicRegisters.array(v);
const U = v => DynamicRegisters.uniq(v);
const sourceIds = item => DynamicRegisters.sourceIds(item);
const sourceLabel = id => sourceLabels[id] || id || '';
const esc = s => T(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

// ── Lecture du modèle : canonique (label/categorie/date_precision/date XOR
// date_debut|fin/membres_reconcilies) ET legacy (event/evenement/type/location/
// precision_date). Correctif bug label : label || event || evenement, puis repli
// sur le titre Markdown de l'entrée (registres spécialisés S67/S80… qui portent
// l'intitulé dans le heading, pas dans un champ). ───────────────────────────
const cleanHeading = h => T(h).replace(/^\s*(?:CHR|EVENT)-[A-Za-z0-9-]+\s*[—:–-]\s*/, '').trim();
const labelOf = r => {
  const d = (r && r.data) || {};
  return T(d.label || d.event || d.evenement) || cleanHeading(r && r.heading) || T(d.id) || 'Sans intitulé';
};
const isCanonical = r => /^EVENT-/.test(T(r.id)) && !/^EVENT-S\d+-/.test(T(r.id));
// Correctif Codex : une date pleine non quotée (date: 1980-05-18) est parsée
// par js-yaml en objet Date → T() la rendrait « Sun May 18 1980 … » et casserait
// humanDate / yearOf / tri / filtres / CSV. On normalise tout Date (et tout
// AAAA-MM-JJ porté par un Date) en ISO local AAAA-MM-JJ AVANT le repli sur T().
const isoDate = v => {
  // Détection de Date robuste au cross-realm (Object.prototype.toString plutôt
  // qu'instanceof) : js-yaml peut créer la Date dans un autre realm que celui
  // de l'app (cas des environnements de rendu) — instanceof y échouerait.
  if (v && Object.prototype.toString.call(v) === '[object Date]' && !isNaN(v)) {
    const p = n => String(n).padStart(2, '0');
    return `${v.getUTCFullYear()}-${p(v.getUTCMonth() + 1)}-${p(v.getUTCDate())}`;
  }
  return T(v);
};
const startDate = d => isoDate(d.date != null ? d.date : d.date_debut);
const endDate = d => isoDate(d.date_fin);
const categoryOf = d => T(d.categorie) || 'jalon';   // legacy sans categorie → jalon

// ── Couches activables : ordre = priorité d'empilement de la frise ──────────
const LAYERS = [
  { key: 'jalon', label: 'Jalons', hint: 'ancres + beats', on: true },
  { key: 'concert_a_migrer', label: 'Concerts', hint: '→ registre concerts', on: false },
  { key: 'contexte', label: 'Contexte', hint: '', on: false },
  { key: 'reception_posthume', label: 'Réception posthume', hint: '', on: false }
];
const layerState = Object.fromEntries(LAYERS.map(l => [l.key, l.on]));

// ── Précision honnête (miroir du traitement geo_precision de la carte lieux).
// Buckets contrôlés du schéma chronology_event : jour | mois | saison | annee
// | circa | intervalle. On lit date_precision (canonique) puis precision_date
// (legacy, texte libre) que l'on normalise ; à défaut on infère du format de la
// date — jamais plus précis que ce que la donnée déclare. ───────────────────
function precisionBucket(d) {
  if (d.date_debut && d.date_fin) return 'intervalle';
  const raw = T(d.date_precision || d.precision_date).toLowerCase().trim();
  if (raw) {
    if (/(intervalle|range|periode|période|date_range|exact_range|month_range|approximate_range)/.test(raw)) return 'intervalle';
    if (/(circa|approx|inferred|to_verify|decade|after_|before_|around|envir|late_|early_|mid_)/.test(raw)) return 'circa';
    if (/(saison|season|spring|summer|autumn|fall|winter|printemps|été|ete|automne|hiver)/.test(raw)) return 'saison';
    if (/(mois|month)/.test(raw)) return 'mois';
    if (/(annee|année|year|^an$)/.test(raw)) return 'annee';
    if (/(jour|exact|same_day|overnight|day)/.test(raw)) return 'jour';
  }
  // Inférence par le format de la date — borne supérieure de précision.
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

// Affichage humain d'une date ISO partielle (1979-06-14 / 1979-06 / 1979).
const MONTH_FR = ['', 'janv.', 'févr.', 'mars', 'avril', 'mai', 'juin', 'juill.', 'août', 'sept.', 'oct.', 'nov.', 'déc.'];
function humanDate(iso) {
  const s = T(iso);
  let m;
  if ((m = /^(\d{4})-(\d{2})-(\d{2})/.exec(s))) return `${+m[3]} ${MONTH_FR[+m[2]]} ${m[1]}`;
  if ((m = /^(\d{4})-(\d{2})/.exec(s))) return `${MONTH_FR[+m[2]]} ${m[1]}`;
  if ((m = /^(\d{4})/.exec(s))) return m[1];
  return s;
}
const sortKey = d => startDate(d) || endDate(d);

// ── Chargement + résolution de la colonne vertébrale ────────────────────────
async function loadChronology() {
  try {
    sourceLabels = await DynamicRegisters.sourceLabels();
    // Corpus = registre chronologique curé et gelé (registers/chronology/).
    // C'est exactement le périmètre de validate_chronology.py (562 entrées, dont
    // 62 canoniques EVENT-). On exclut volontairement les échos d'atomisation
    // bruts de sources/ (CHR- non catégorisés, hors modèle étape 6).
    records = await DynamicRegisters.loadRecords({
      prefixes: ['registers/chronology/'],
      kinds: ['chronology']
    });
    resolveBackbone();
    buildLayerControls();
    populateFilters();
    apply();
    const anchors = display.filter(isCanonical).length;
    statusCard.textContent = `${display.length} entrées affichables — ${anchors} jalons canoniques (ancres) + ${display.length - anchors} legacy, dédoublonnés par réconciliation same_as.`;
  } catch (error) {
    console.error(error);
    statusCard.textContent = 'Erreur lors du chargement dynamique de la chronologie : ' + error.message;
  }
}

// Dédoublonnage par identité canonique : tout enregistrement legacy listé dans
// `membres_reconcilies` d'un EVENT-, ou portant `same_as: EVENT-…`, est REPLIÉ
// dans la carte de son canonique (traçabilité) et n'apparaît jamais en double.
function resolveBackbone() {
  // Dédoublonnage par identifiant : un même CHR-/EVENT- peut apparaître dans
  // plusieurs fichiers chargés (p. ex. registers/chronology/ ET sources/…).
  // On garde un seul représentant par id — priorité au canonique EVENT-, puis
  // à la copie sous registers/chronology/, sinon la première vue.
  const pick = (a, b) => {
    if (isCanonical(a) !== isCanonical(b)) return isCanonical(a) ? a : b;
    const ca = /^registers\/chronology\//.test(T(a.file));
    const cb = /^registers\/chronology\//.test(T(b.file));
    if (ca !== cb) return ca ? a : b;
    return a;
  };
  const uniqMap = new Map();
  records.forEach(r => {
    const id = T(r.id);
    uniqMap.set(id, uniqMap.has(id) ? pick(uniqMap.get(id), r) : r);
  });
  const unique = [...uniqMap.values()];

  const byId = uniqMap;
  const foldedInto = new Map();           // memberId -> canonical record
  unique.forEach(r => {
    if (!isCanonical(r)) return;
    A(r.data.membres_reconcilies).forEach(m => foldedInto.set(T(m), r));
  });
  unique.forEach(r => {                    // réciproque : same_as porté par le legacy
    A(r.data.same_as).map(T).filter(Boolean).forEach(t => {
      const tgt = byId.get(t);
      if (tgt && isCanonical(tgt)) foldedInto.set(T(r.id), tgt);
    });
  });
  // Attache aux canoniques les enregistrements legacy repliés (pour le dépli).
  unique.forEach(r => {
    if (!isCanonical(r)) return;
    const ids = U(A(r.data.membres_reconcilies).map(T));
    r._members = ids.map(id => byId.get(id) || { id, data: { id } });
  });
  display = unique.filter(r => !foldedInto.has(T(r.id)));
  display.sort((a, b) => sortKey(a.data).localeCompare(sortKey(b.data), undefined, { numeric: true }));
}

// ── Filtres ─────────────────────────────────────────────────────────────────
function addOptions(select, values, labeler = v => v) {
  const cur = select.value;
  select.innerHTML = '<option value="">Tous</option>';
  values.forEach(value => {
    const o = document.createElement('option');
    o.value = value; o.textContent = labeler(value);
    select.appendChild(o);
  });
  if (values.includes(cur)) select.value = cur;
}
const yearOf = d => { const m = /^(\d{4})/.exec(sortKey(d)); return m ? m[1] : ''; };
function populateFilters() {
  addOptions(yearFilter, U(display.map(r => yearOf(r.data)).filter(Boolean)));
  addOptions(sourceFilter, U(display.flatMap(sourceIds)), sourceLabel);
}
function buildLayerControls() {
  layerControls.innerHTML = '';
  const counts = {};
  display.forEach(r => { const c = categoryOf(r.data); counts[c] = (counts[c] || 0) + 1; });
  LAYERS.forEach(l => {
    const id = 'layer-' + l.key;
    const wrap = document.createElement('label');
    wrap.className = 'layer-toggle layer-toggle--' + l.key + (layerState[l.key] ? ' is-on' : '');
    wrap.htmlFor = id;
    wrap.innerHTML =
      `<input type="checkbox" id="${id}" ${layerState[l.key] ? 'checked' : ''}>` +
      `<span class="layer-toggle__dot" aria-hidden="true"></span>` +
      `<span class="layer-toggle__name">${esc(l.label)}<span class="layer-toggle__count">${counts[l.key] || 0}</span></span>` +
      (l.hint ? `<span class="layer-toggle__hint">${esc(l.hint)}</span>` : '');
    wrap.querySelector('input').addEventListener('change', e => {
      layerState[l.key] = e.target.checked;
      wrap.classList.toggle('is-on', e.target.checked);
      apply();
    });
    layerControls.appendChild(wrap);
  });
}

function haystack(r) {
  const d = r.data || {};
  return [r.id, labelOf(r), d.type, d.location, startDate(d), endDate(d),
    ...A(d.membres_reconcilies), ...sourceIds(r), ...sourceIds(r).map(sourceLabel), d.prudence_methodologique, r.file]
    .map(T).join(' ').toLowerCase();
}
function apply() {
  const q = searchInput.value.toLowerCase().trim();
  const year = yearFilter.value;
  const source = sourceFilter.value;
  const filtered = display.filter(r => {
    const d = r.data || {};
    if (!layerState[categoryOf(d)]) return false;
    if (q && !haystack(r).includes(q)) return false;
    if (year && yearOf(d) !== year) return false;
    if (source && !sourceIds(r).includes(source)) return false;
    return true;
  });
  renderTimeline(filtered);
}

// ── Rendu de la frise ────────────────────────────────────────────────────────
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
    const src = sourceIds(m).map(sourceLabel).join(', ');
    return `<li><code>${esc(m.id)}</code><span class="member__label">${esc(labelOf(m))}</span>`
      + (src ? `<span class="member__src">${esc(src)}</span>` : '') + `</li>`;
  }).join('');
  return `<details class="trace"><summary>${members.length} membre(s) réconcilié(s) · traçabilité</summary>`
    + `<ul class="member-list">${rows}</ul></details>`;
}

function card(r) {
  const d = r.data || {};
  const cat = categoryOf(d);
  const anchor = isCanonical(r);
  const meta = PRECISION_META[precisionBucket(d)];
  const display_start = (meta.sigil || '') + humanDate(startDate(d));
  const dateText = (precisionBucket(d) === 'intervalle')
    ? `${humanDate(startDate(d))} → ${humanDate(endDate(d))}`
    : display_start;
  const sources = sourceIds(r).map(s => `<span class="badge">${esc(sourceLabel(s))}</span>`).join('');
  const prud = T(d.prudence_methodologique).trim();
  const note = T(d.notes || d.note).trim();

  const el = document.createElement('article');
  el.className = 'beat'
    + (anchor ? ' beat--anchor' : ' beat--minor')
    + ' beat--' + cat
    + (cat === 'concert_a_migrer' ? ' beat--transit' : '');

  el.innerHTML =
    `<div class="beat__node" aria-hidden="true"></div>` +
    `<div class="beat__body">` +
      `<div class="beat__head">` +
        `<time class="beat__date">${esc(dateText)}</time>` +
        precisionTrack(d) +
        `<span class="beat__tag beat__tag--${cat}">${esc(tagLabel(cat, anchor))}</span>` +
        `<span class="beat__prec">${esc(meta.text)}</span>` +
      `</div>` +
      `<h3 class="beat__label">${esc(labelOf(r))}</h3>` +
      (sources ? `<div class="beat__sources">${sources}</div>` : '') +
      (prud ? `<p class="beat__prudence">⚠ ${esc(prud)}</p>` : '') +
      (note ? `<p class="beat__note">${esc(note)}</p>` : '') +
      membersHtml(r) +
    `</div>`;
  return el;
}

function tagLabel(cat, anchor) {
  if (cat === 'jalon') return anchor ? 'ancre' : 'beat';
  if (cat === 'concert_a_migrer') return '→ concerts';
  if (cat === 'reception_posthume') return 'réception';
  return cat;
}

function renderTimeline(items) {
  timeline.innerHTML = '';
  resultsMeta.textContent = `${items.length} entrée(s)`;
  if (!items.length) {
    timeline.innerHTML = '<p class="empty">Aucune entrée pour ces couches / filtres.</p>';
    return;
  }
  // Repère d'année : on insère un marqueur quand le millésime change.
  let lastYear = '';
  const frag = document.createDocumentFragment();
  items.forEach(r => {
    const y = yearOf(r.data);
    if (y && y !== lastYear) {
      lastYear = y;
      const mark = document.createElement('div');
      mark.className = 'year-mark';
      mark.innerHTML = `<span>${esc(y)}</span>`;
      frag.appendChild(mark);
    }
    frag.appendChild(card(r));
  });
  timeline.appendChild(frag);
}

// ── Export CSV (modèle canonique + legacy) ───────────────────────────────────
function exportCSV() {
  const rows = [['id', 'categorie', 'ancre', 'date', 'date_fin', 'date_precision', 'label', 'sources', 'membres_reconcilies', 'file']];
  display.forEach(r => {
    const d = r.data || {};
    rows.push([
      r.id, categoryOf(d), isCanonical(r) ? 'oui' : 'non',
      startDate(d), endDate(d), precisionBucket(d), labelOf(r),
      sourceIds(r).map(sourceLabel).join(' | '),
      A(d.membres_reconcilies).join(' | '), r.file
    ]);
  });
  const csv = rows.map(row => row.map(v => '"' + String(v || '').replace(/"/g, '""') + '"').join(',')).join('\n');
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'registre_chronologique_canonique.csv';
  link.click();
  URL.revokeObjectURL(link.href);
}

[searchInput, yearFilter, sourceFilter].forEach(el => el.addEventListener('input', apply));
resetButton.addEventListener('click', () => {
  searchInput.value = ''; yearFilter.value = ''; sourceFilter.value = '';
  LAYERS.forEach(l => { layerState[l.key] = l.on; });
  buildLayerControls();
  apply();
});
downloadButton.addEventListener('click', exportCSV);
loadChronology();
