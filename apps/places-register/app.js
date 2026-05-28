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
  if (except !== 'source' && f.source && !sourceIds(item).includes(f.source)) return false;
  if (except !== 'chapter' && f.chapter && !chaptersOf(d).includes(f.chapter)) return false;
  return true;
}
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
  select.value = values.includes(cur) ? cur : '';
}
function refreshFacets() {
  const f = currentFilters();
  // Type ordered by the canonical section order; others alphanumeric.
  const typeVals = PlaceIcons.order.filter(t =>
    items.some(i => typeOf(i.data || {}) === t && matches(i, f, 'type')));
  setOptions(typeFilter, typeVals, 'Tous', PlaceIcons.label);
  setOptions(detailFilter, U(items.filter(i => matches(i, f, 'detail')).map(i => detailOf(i.data || {}))), 'Tous');
  setOptions(sourceFilter, U(items.filter(i => matches(i, f, 'source')).flatMap(sourceIds)), 'Toutes', sourceLabel);
  setOptions(chapterFilter, U(items.filter(i => matches(i, f, 'chapter')).flatMap(i => chaptersOf(i.data || {}))), 'Tous');
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
}

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
