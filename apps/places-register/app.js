/* Registre des lieux — logique d'affichage.
   Groupage par type primaire, facettes croisées, "Voir plus" accessible,
   pictos SVG par famille. Data inchangée (lecture via DynamicRegisters). */

const searchInput = document.getElementById('search');
const typeFilter = document.getElementById('type-filter');
const detailFilter = document.getElementById('detail-filter');
const sourceFilter = document.getElementById('source-filter');
const chapterFilter = document.getElementById('chapter-filter');
const resetButton = document.getElementById('reset-filters');
const downloadButton = document.getElementById('download-csv');
const resultsMeta = document.getElementById('results-meta');
const statusEl = document.getElementById('places-status');
const sectionsEl = document.getElementById('places-sections');

let items = [];
let sourceLabels = {};

const T = v => DynamicRegisters.text(v);
const A = v => DynamicRegisters.array(v);
const U = v => DynamicRegisters.uniq(v);
const sourceIds = item => DynamicRegisters.sourceIds(item);
const sourceLabel = id => sourceLabels[id] || id || '';
// Aggregate atom-level source ids (e.g. "S02-A003") to their chapter root
// ("S02") so the Source filter exposes readable roots, not raw atom codes.
const sourceRoot = s => { const m = /^(S\d+)-A\d+$/.exec(T(s)); return m ? m[1] : T(s); };
const sourceRoots = item => U(sourceIds(item).map(sourceRoot));
const chaptersOf = data => A(data.chapters || data.chapitres);
const labelOf = data => data.label || data.nom || data.name || data.id || '';
const typeOf = data => data.type || data.type_lieu || data.category || 'generic';
const detailOf = data => data.type_detail || '';
const resolveUsage = place => {
  if (place.usage) return place.usage;
  const k = Object.keys(place).filter(x => x.startsWith('usage_'));
  for (const key of k) if (place[key]) return place[key];
  return place.description || place.note || '';
};
const esc = s => T(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

const USAGE_MAX = 120;

async function loadItems() {
  sourceLabels = await DynamicRegisters.sourceLabels();
  items = await DynamicRegisters.loadRecords({ prefixes: ['registers/places/', 'registers/'], kinds: ['place'] });
  statusEl.style.display = 'none';
  refreshFacets();
  render();
}

/* ── Filtres / facettes ─────────────────────────────────── */
function currentFilters() {
  return {
    q: searchInput.value.toLowerCase().trim(),
    type: typeFilter.value,
    detail: detailFilter.value,
    source: sourceFilter.value,
    chapter: chapterFilter.value
  };
}
function haystack(item) {
  const d = item.data || {};
  return [item.id, labelOf(d), typeOf(d), detailOf(d), resolveUsage(d), d.prudence,
    ...sourceIds(item), ...sourceIds(item).map(sourceLabel), ...chaptersOf(d), item.file]
    .map(T).join(' ').toLowerCase();
}
function matches(item, f, except) {
  const d = item.data || {};
  if (except !== 'q' && f.q && !haystack(item).includes(f.q)) return false;
  if (except !== 'type' && f.type && typeOf(d) !== f.type) return false;
  if (except !== 'detail' && f.detail && detailOf(d) !== f.detail) return false;
  if (except !== 'source' && f.source && !sourceRoots(item).includes(f.source)) return false;
  if (except !== 'chapter' && f.chapter && !chaptersOf(d).includes(f.chapter)) return false;
  return true;
}
// Rebuild a select's options; returns true if the current selection was
// orphaned by the new option set and had to be cleared.
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
  // Each select offers only values still present under the *other* active
  // filters. Clearing an orphaned selection widens the remaining facets, so
  // re-read currentFilters() and repeat until a full pass clears nothing
  // (guarded against infinite loops).
  for (let pass = 0; pass < 5; pass++) {
    const f = currentFilters();
    // Type ordered by the canonical section order; others alphanumeric.
    const typeVals = PlaceIcons.order.filter(t =>
      items.some(i => typeOf(i.data || {}) === t && matches(i, f, 'type')));
    let cleaned = false;
    cleaned = setOptions(typeFilter, typeVals, 'Tous', PlaceIcons.label) || cleaned;
    cleaned = setOptions(detailFilter, U(items.filter(i => matches(i, f, 'detail')).map(i => detailOf(i.data || {}))), 'Tous') || cleaned;
    cleaned = setOptions(sourceFilter, U(items.filter(i => matches(i, f, 'source')).flatMap(sourceRoots)), 'Toutes') || cleaned;
    cleaned = setOptions(chapterFilter, U(items.filter(i => matches(i, f, 'chapter')).flatMap(i => chaptersOf(i.data || {}))), 'Tous') || cleaned;
    if (!cleaned) break;
  }
}

/* ── Rendu ──────────────────────────────────────────────── */
function sourceBadges(item) {
  return sourceIds(item).map(v => '<span class="place-badge">' + esc(sourceLabel(v)) + '</span>').join('');
}
function card(item) {
  const d = item.data || {};
  const type = typeOf(d);
  const detail = detailOf(d);
  const usage = T(resolveUsage(d)).trim();
  let usageHtml = '';
  if (usage) {
    if (usage.length > USAGE_MAX) {
      const short = usage.slice(0, USAGE_MAX).trimEnd();
      usageHtml = '<p class="place-card__usage" data-expanded="0" data-full="' + esc(usage) + '" data-short="' + esc(short) + '">'
        + esc(short) + '… <button type="button" class="place-card__more">Voir plus</button></p>';
    } else {
      usageHtml = '<p class="place-card__usage">' + esc(usage) + '</p>';
    }
  }
  return '<article class="place-card">'
    + '<div class="place-card__header">' + PlaceIcons.svg(type)
      + '<div class="place-card__heading"><h3 class="place-card__title">' + esc(labelOf(d)) + '</h3>'
      + (detail ? '<p class="place-card__subtitle">' + esc(detail) + '</p>' : '') + '</div></div>'
    + usageHtml
    + '<div class="place-badges">' + sourceBadges(item) + '</div>'
    + '<div class="place-card__file"><code>' + esc(item.file) + '</code></div>'
    + '</article>';
}
function render() {
  const f = currentFilters();
  const filtered = items.filter(i => matches(i, f));
  resultsMeta.textContent = filtered.length + ' lieu' + (filtered.length > 1 ? 'x' : '');
  sectionsEl.innerHTML = '';
  if (!filtered.length) {
    sectionsEl.innerHTML = '<p class="places-empty">Aucun lieu ne correspond à ces critères.</p>';
    // Codex : sans cet appel, la branche d'état vide sortait AVANT updateMap(),
    // laissant la couche Leaflet et la note avec les marqueurs précédents — la
    // carte ne reflétait plus les facettes actives. On vide explicitement.
    updateMap([]);
    return;
  }
  const byType = new Map();
  filtered.forEach(i => {
    const t = typeOf(i.data || {});
    if (!byType.has(t)) byType.set(t, []);
    byType.get(t).push(i);
  });
  // Sections in canonical order, then any leftover types.
  const order = [...PlaceIcons.order, ...[...byType.keys()].filter(t => !PlaceIcons.order.includes(t))];
  order.forEach(type => {
    const group = byType.get(type);
    if (!group || !group.length) return;
    group.sort((a, b) => T(labelOf(a.data || {})).localeCompare(T(labelOf(b.data || {})), undefined, { numeric: true }));
    const section = document.createElement('section');
    section.className = 'places-section';
    section.innerHTML = '<div class="places-section__header">' + PlaceIcons.svg(type)
      + '<h2 class="places-section__title">' + esc(PlaceIcons.label(type))
      + ' <span class="places-section__count">' + group.length + '</span></h2></div>'
      + '<div class="places-list">' + group.map(card).join('') + '</div>';
    sectionsEl.appendChild(section);
  });
  updateMap(filtered);
}

/* ── Carte (étape 12b-1.c) ──────────────────────────────────
   Couche Leaflet sur fond OpenStreetMap. Marqueurs des lieux CANONIQUES
   géolocalisés (lat/lng WGS84 curés hors-ligne, recoupés Wikidata P625).
   Init paresseuse au premier passage en vue carte ; les marqueurs reflètent
   le jeu filtré courant (mêmes facettes que la liste). */
const mapWrap = document.getElementById('places-map-wrap');
const mapNote = document.getElementById('map-note');
const viewListBtn = document.getElementById('view-list');
const viewMapBtn = document.getElementById('view-map');
const toggleZonesBtn = document.getElementById('toggle-zones');
let map = null;
let markerLayer = null;   // venues précises (punaises ponctuelles)
let zoneLayer = null;     // entités grossières (cercles, étendues — non ponctuelles)
let mapView = false;
let zonesEnabled = true;

// Seuil « grossier » UNIQUE (miroir de COARSE_PRECISIONS dans validate_places.py) :
// ces granularités sont des ZONES (étendues), rendues en cercles translucides et
// exclues des punaises de venues précises. Point d'ajustement central.
const COARSE_PRECISIONS = new Set(['ville', 'region']);
const ZONE_RADIUS_M = { ville: 4000, region: 12000 };
const isCoarse = d => COARSE_PRECISIONS.has(T(d.geo_precision));

const num = v => (typeof v === 'number' && isFinite(v)) ? v : (v !== '' && v != null && isFinite(Number(v)) ? Number(v) : null);
const coords = d => { const la = num(d.lat), ln = num(d.lng); return (la != null && ln != null) ? [la, ln] : null; };

function ensureMap() {
  if (map || typeof L === 'undefined') return map;
  map = L.map('places-map', { scrollWheelZoom: false }).setView([53.4808, -2.2426], 6); // Manchester
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  }).addTo(map);
  zoneLayer = L.layerGroup();          // ajoutée/retirée selon zonesEnabled
  if (zonesEnabled) zoneLayer.addTo(map);
  markerLayer = L.layerGroup().addTo(map);  // au-dessus des zones
  return map;
}

function markerIcon(type) {
  return L.divIcon({
    className: 'place-pin-wrap',
    html: '<span class="place-pin place-pin--' + esc(type) + '">' + PlaceIcons.svg(type) + '</span>',
    iconSize: [30, 30], iconAnchor: [15, 28], popupAnchor: [0, -26]
  });
}

function popupHtml(item) {
  const d = item.data || {};
  const usage = T(resolveUsage(d)).trim();
  const shortUsage = usage.length > 160 ? usage.slice(0, 160).trimEnd() + '…' : usage;
  const prec = T(d.geo_precision);
  const pm = T(d.prudence_methodologique).trim();
  const badges = sourceIds(item).map(v => '<span class="place-badge">' + esc(sourceLabel(v)) + '</span>').join('');
  return '<div class="place-popup">'
    + '<h3 class="place-popup__title">' + esc(labelOf(d)) + '</h3>'
    + '<p class="place-popup__type">' + esc(PlaceIcons.label(typeOf(d)))
      + (detailOf(d) ? ' · <em>' + esc(detailOf(d)) + '</em>' : '') + '</p>'
    + (shortUsage ? '<p class="place-popup__usage">' + esc(shortUsage) + '</p>' : '')
    + (prec ? '<p class="place-popup__geo">Précision : ' + esc(prec) + '</p>' : '')
    + (pm ? '<p class="place-popup__prudence">⚠ ' + esc(pm) + '</p>' : '')
    + (badges ? '<div class="place-badges">' + badges + '</div>' : '')
    + '</div>';
}

function zoneCircle(item, ll) {
  const d = item.data || {};
  return L.circle(ll, {
    radius: ZONE_RADIUS_M[T(d.geo_precision)] || 4000,
    className: 'place-zone',
    interactive: true
  }).bindPopup(popupHtml(item));
}

function updateMap(filtered) {
  if (!mapView || !ensureMap()) return;
  markerLayer.clearLayers();
  zoneLayer.clearLayers();
  const geoloc = filtered.filter(i => coords(i.data || {}));
  let nbVenue = 0, nbZone = 0;
  const pts = [];          // pour le recadrage : venues + zones visibles
  geoloc.forEach(item => {
    const d = item.data || {};
    const ll = coords(d);
    if (isCoarse(d)) {
      zoneCircle(item, ll).addTo(zoneLayer);
      nbZone++;
      if (zonesEnabled) pts.push(ll);
    } else {
      L.marker(ll, { icon: markerIcon(typeOf(d)), title: labelOf(d) })
        .bindPopup(popupHtml(item))
        .addTo(markerLayer);
      nbVenue++;
      pts.push(ll);
    }
  });
  const total = filtered.length;
  mapNote.textContent = nbVenue + ' venue' + (nbVenue > 1 ? 's' : '') + ' précise'
    + (nbVenue > 1 ? 's' : '') + ' (points) + ' + nbZone + ' zone' + (nbZone > 1 ? 's' : '')
    + ' ville/région (étendues' + (zonesEnabled ? '' : ', masquées') + '), sur ' + total
    + ' lieux filtrés. Coordonnées WGS84 curées, recoupées Wikidata P625 ; fond OpenStreetMap.';
  if (pts.length) map.fitBounds(pts, { padding: [40, 40], maxZoom: 14 });
  map.invalidateSize();
}

function setZones(on) {
  zonesEnabled = on;
  toggleZonesBtn.classList.toggle('is-active', on);
  toggleZonesBtn.setAttribute('aria-pressed', String(on));
  if (zoneLayer && map) {
    if (on) zoneLayer.addTo(map); else map.removeLayer(zoneLayer);
  }
  if (mapView) updateMap(items.filter(i => matches(i, currentFilters())));
}
toggleZonesBtn.addEventListener('click', () => setZones(!zonesEnabled));

function setView(toMap) {
  mapView = toMap;
  mapWrap.hidden = !toMap;
  sectionsEl.hidden = toMap;
  viewMapBtn.classList.toggle('is-active', toMap);
  viewMapBtn.setAttribute('aria-selected', String(toMap));
  viewListBtn.classList.toggle('is-active', !toMap);
  viewListBtn.setAttribute('aria-selected', String(!toMap));
  if (toMap) { ensureMap(); updateMap(items.filter(i => matches(i, currentFilters()))); }
}
viewListBtn.addEventListener('click', () => setView(false));
viewMapBtn.addEventListener('click', () => setView(true));

/* ── "Voir plus" (délégation, accessible clavier via <button>) ── */
sectionsEl.addEventListener('click', e => {
  const btn = e.target.closest('.place-card__more');
  if (!btn) return;
  const p = btn.closest('.place-card__usage');
  const nowExpanded = p.dataset.expanded !== '1';
  p.dataset.expanded = nowExpanded ? '1' : '0';
  p.textContent = (nowExpanded ? p.dataset.full : p.dataset.short + '…') + ' ';
  const nb = document.createElement('button');
  nb.type = 'button';
  nb.className = 'place-card__more';
  nb.textContent = nowExpanded ? 'Voir moins' : 'Voir plus';
  p.appendChild(nb);
});

/* ── Export CSV (jeu filtré courant) ────────────────────── */
function exportCSV() {
  const f = currentFilters();
  const rows = [['id', 'label', 'type', 'type_detail', 'sources', 'chapters', 'file']];
  items.filter(i => matches(i, f)).forEach(item => {
    const d = item.data || {};
    rows.push([item.id, labelOf(d), typeOf(d), detailOf(d),
      sourceIds(item).map(sourceLabel).join(' | '), chaptersOf(d).join(' | '), item.file]);
  });
  const csv = rows.map(r => r.map(v => '"' + String(v || '').replace(/"/g, '""') + '"').join(',')).join('\n');
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'registre_lieux.csv';
  a.click();
  URL.revokeObjectURL(a.href);
}

/* ── Événements ─────────────────────────────────────────── */
function onFilterChange() { refreshFacets(); render(); }
[searchInput, typeFilter, detailFilter, sourceFilter, chapterFilter].forEach(el => el.addEventListener('input', onFilterChange));
resetButton.addEventListener('click', () => {
  searchInput.value = ''; typeFilter.value = ''; detailFilter.value = '';
  sourceFilter.value = ''; chapterFilter.value = '';
  refreshFacets(); render();
});
downloadButton.addEventListener('click', exportCSV);

loadItems().catch(err => {
  console.error(err);
  statusEl.style.display = '';
  statusEl.textContent = 'Erreur de chargement : ' + err.message;
});
