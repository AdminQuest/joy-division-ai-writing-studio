const searchInput = document.getElementById('search');
const contextFilter = document.getElementById('context-filter');
const photographerFilter = document.getElementById('photographer-filter');
const yearFilter = document.getElementById('year-filter');
const resetButton = document.getElementById('reset-filters');
const downloadButton = document.getElementById('download-csv');
const resultsMeta = document.getElementById('results-meta');
const statusEl = document.getElementById('img-status');
const sessionsSections = document.getElementById('sessions-sections');
const imagesSections = document.getElementById('images-sections');
const panelSessions = document.getElementById('panel-sessions');
const panelImages = document.getElementById('panel-images');
const tabSessions = document.getElementById('tab-sessions');
const tabImages = document.getElementById('tab-images');

let allEntries = [];
let sessions = [];
let images = [];
let currentView = 'sessions';
let _rendering = false;

const IMAGES_URL = '../../registers/images/images.json';

const CONTEXT_META = {
  promo:     { label: 'Promo',      order: 0 },
  live:      { label: 'Live',       order: 1 },
  portrait:  { label: 'Portrait',   order: 2 },
  artwork:   { label: 'Artwork',    order: 3 },
  rehearsal: { label: 'Repetition', order: 4 },
  other:     { label: 'Autre',      order: 5 }
};

const PRECISION_LABELS = {
  day: 'Jour',
  month: 'Mois',
  year: 'Annee',
  approximate: 'Approx.',
  unknown: 'Inconnue'
};

const esc = s => String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

function contextLabel(ctx) {
  return (CONTEXT_META[ctx] || {}).label || ctx;
}

function contextOrder(ctx) {
  return (CONTEXT_META[ctx] || {}).order ?? 99;
}

function photographerName(pid) {
  return pid ? pid.replace(/^PERSON-/, '').replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase()) : 'Non identifie';
}

function yearFromDate(date) {
  return date ? date.substring(0, 4) : '';
}

async function loadImages() {
  const resp = await fetch(IMAGES_URL, { cache: 'no-store' });
  if (!resp.ok) throw new Error('HTTP ' + resp.status);
  const data = await resp.json();

  allEntries = data
    .filter(e => e.gate === 'public')
    .map(entry => ({
      id: entry.image_id,
      level: entry.level || 'session',
      sessionRef: entry.session_ref || null,
      name: entry.canonical_name || '',
      photographer: entry.photographer || '',
      date: entry.date || '',
      datePrecision: entry.date_precision || 'approximate',
      place: entry.place || null,
      eventRef: entry.event_ref || null,
      context: entry.context || 'other',
      subjects: entry.subjects || [],
      outputCount: entry.output_count || null,
      usage: entry.usage || [],
      iconic: entry.iconic || false,
      notes: entry.notes || '',
      sources: entry.sources || [],
      sourceUrl: entry.source_url || null,
      sourcePlatform: entry.source_platform || null,
      status: entry.status || null,
      rightsStatus: entry.rights_status || null,
      localFile: entry.local_file || null,
      thumbnail: entry.thumbnail || null,
      sameAs: entry.same_as || {},
      gate: entry.gate || 'public'
    }));

  sessions = allEntries.filter(e => e.level === 'session');
  images = allEntries.filter(e => e.level === 'image' || e.level === 'image_reference');

  sessions.sort((a, b) => a.date.localeCompare(b.date));
  images.sort((a, b) => a.date.localeCompare(b.date));

  statusEl.style.display = 'none';

  handleDeepLink();
  refreshFacets();
  render();
}

function handleDeepLink() {
  const params = new URLSearchParams(window.location.search);
  const targetId = params.get('id');
  if (!targetId) return;
  const target = allEntries.find(e => e.id === targetId);
  if (target && target.level !== 'session') {
    switchView('images');
  } else {
    switchView('sessions');
  }
  requestAnimationFrame(() => {
    const el = document.getElementById(targetId);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      el.style.outline = '2px solid var(--accent)';
      setTimeout(() => { el.style.outline = ''; }, 3000);
    }
  });
}

function switchView(view) {
  currentView = view;
  const isSessions = view === 'sessions';
  tabSessions.setAttribute('aria-selected', isSessions ? 'true' : 'false');
  tabSessions.tabIndex = isSessions ? 0 : -1;
  tabImages.setAttribute('aria-selected', isSessions ? 'false' : 'true');
  tabImages.tabIndex = isSessions ? -1 : 0;
  panelSessions.hidden = !isSessions;
  panelImages.hidden = isSessions;
  refreshFacets();
  render();
}

tabSessions.addEventListener('click', () => switchView('sessions'));
tabImages.addEventListener('click', () => switchView('images'));

function currentData() {
  return currentView === 'sessions' ? sessions : images;
}

function currentFilters() {
  return {
    q: searchInput.value.toLowerCase().trim(),
    context: contextFilter.value,
    photographer: photographerFilter.value,
    year: yearFilter.value
  };
}

function searchIndex(e) {
  return [e.name, e.photographer, photographerName(e.photographer), e.date,
    e.context, e.place || '', e.eventRef || '', ...e.subjects,
    ...e.sources, e.sourceUrl || '', e.sourcePlatform || '', e.status || '',
    e.rightsStatus || '', e.notes, ...(e.usage || []), e.id].join(' ').toLowerCase();
}

function matches(e, f, except) {
  if (except !== 'q' && f.q && !searchIndex(e).includes(f.q)) return false;
  if (except !== 'context' && f.context && e.context !== f.context) return false;
  if (except !== 'photographer' && f.photographer && e.photographer !== f.photographer) return false;
  if (except !== 'year' && f.year && yearFromDate(e.date) !== f.year) return false;
  return true;
}

function setOptions(select, values, allLabel, labeler) {
  const cur = select.value;
  select.innerHTML = '';
  const all = document.createElement('option');
  all.value = ''; all.textContent = allLabel;
  select.appendChild(all);
  values.forEach(v => {
    const o = document.createElement('option');
    o.value = v; o.textContent = labeler ? labeler(v) : v;
    select.appendChild(o);
  });
  const cleaned = cur !== '' && !values.includes(cur);
  select.value = cleaned ? '' : cur;
  return cleaned;
}

function uniq(arr) {
  return [...new Set(arr)].filter(Boolean);
}

function refreshFacets() {
  const data = currentData();
  for (let pass = 0; pass < 5; pass++) {
    const f = currentFilters();
    const contexts = uniq(data.filter(e => matches(e, f, 'context')).map(e => e.context))
      .sort((a, b) => contextOrder(a) - contextOrder(b));
    const photographers = uniq(data.filter(e => matches(e, f, 'photographer')).map(e => e.photographer))
      .sort((a, b) => photographerName(a).localeCompare(photographerName(b)));
    const years = uniq(data.filter(e => matches(e, f, 'year')).map(e => yearFromDate(e.date))).sort();
    let cleaned = false;
    cleaned = setOptions(contextFilter, contexts, 'Tous', contextLabel) || cleaned;
    cleaned = setOptions(photographerFilter, photographers, 'Tous', photographerName) || cleaned;
    cleaned = setOptions(yearFilter, years, 'Toutes') || cleaned;
    if (!cleaned) break;
  }
}

function detail(label, content) {
  return content ? '<div class="img-detail"><p class="img-detail__label">' + esc(label) + '</p>' + content + '</div>' : '';
}

function tags(values) {
  const arr = (values || []).filter(Boolean);
  return arr.length ? '<div class="img-tags">' + arr.map(v => '<span class="img-tag">' + esc(v) + '</span>').join('') + '</div>' : '';
}

function sourceLink(url) {
  if (!url) return '';
  return '<a href="' + esc(url) + '" class="img-tag img-tag--link" target="_blank" rel="noopener noreferrer">' + esc(url) + '</a>';
}

function sessionCard(e) {
  const notesBlock = e.notes
    ? '<div class="img-card__notes">'
      + '<p class="img-card__notes-label">Notes</p>'
      + '<p class="img-card__notes-text">' + esc(e.notes) + '</p>'
      + '</div>'
    : '';

  const detailsContent = detail('Sujets', tags(e.subjects.map(s => s.replace(/^PERSON-/, '').replace(/-/g, ' '))))
    + detail('Sources', tags(e.sources))
    + (e.place ? detail('Lieu', '<span class="img-tag">' + esc(e.place) + '</span>') : '')
    + (e.eventRef ? detail('Evenement', '<span class="img-tag">' + esc(e.eventRef) + '</span>') : '');

  return '<article class="img-card img-card--' + esc(e.context) + '" id="' + esc(e.id) + '">'
    + '<div class="img-card__header"><div class="img-card__heading">'
    + '<h3 class="img-card__title">' + esc(e.name) + '</h3></div></div>'
    + '<div class="img-card__badges">'
    + '<span class="img-badge img-badge--' + esc(e.context) + '">' + esc(contextLabel(e.context)) + '</span>'
    + '<span class="img-badge img-badge--precision">' + esc(e.date) + '</span>'
    + (e.outputCount ? '<span class="img-badge img-badge--level">' + e.outputCount + ' cliches</span>' : '')
    + '</div>'
    + '<p class="img-card__line"><strong>Photographe :</strong> ' + esc(photographerName(e.photographer)) + '</p>'
    + notesBlock
    + '<button type="button" class="img-card__more" aria-expanded="false">Voir plus</button>'
    + '<div class="img-card__details" hidden>' + detailsContent + '</div>'
    + '<p class="img-card__id"><code>' + esc(e.id) + '</code></p>'
    + '</article>';
}

function imageCard(e) {
  const notesBlock = e.notes
    ? '<div class="img-card__notes">'
      + '<p class="img-card__notes-label">Notes</p>'
      + '<p class="img-card__notes-text">' + esc(e.notes) + '</p>'
      + '</div>'
    : '';

  const detailsContent = detail('Sujets', tags(e.subjects.map(s => s.replace(/^PERSON-/, '').replace(/-/g, ' '))))
    + detail('Usages', tags(e.usage))
    + detail('Sources', tags(e.sources))
    + (e.sourceUrl ? detail('Source externe', sourceLink(e.sourceUrl)) : '')
    + (e.sourcePlatform ? detail('Plateforme', '<span class="img-tag">' + esc(e.sourcePlatform) + '</span>') : '')
    + (e.rightsStatus ? detail('Droits', '<span class="img-tag">' + esc(e.rightsStatus) + '</span>') : '')
    + (e.status ? detail('Statut', '<span class="img-tag">' + esc(e.status) + '</span>') : '')
    + (e.sessionRef ? detail('Seance', '<a href="?id=' + esc(e.sessionRef) + '" class="img-tag">' + esc(e.sessionRef) + '</a>') : '')
    + (e.place ? detail('Lieu', '<span class="img-tag">' + esc(e.place) + '</span>') : '');

  return '<article class="img-card img-card--' + esc(e.context) + '" id="' + esc(e.id) + '">'
    + '<div class="img-card__header"><div class="img-card__heading">'
    + '<h3 class="img-card__title">' + esc(e.name) + '</h3></div></div>'
    + '<div class="img-card__badges">'
    + '<span class="img-badge img-badge--' + esc(e.context) + '">' + esc(contextLabel(e.context)) + '</span>'
    + (e.date ? '<span class="img-badge img-badge--precision">' + esc(e.date) + '</span>' : '')
    + (e.iconic ? '<span class="img-badge img-badge--iconic">Iconique</span>' : '')
    + (e.status === 'reference_only' ? '<span class="img-badge img-badge--level">Reference externe</span>' : '')
    + '</div>'
    + '<p class="img-card__line"><strong>Photographe :</strong> ' + esc(photographerName(e.photographer)) + '</p>'
    + notesBlock
    + '<button type="button" class="img-card__more" aria-expanded="false">Voir plus</button>'
    + '<div class="img-card__details" hidden>' + detailsContent + '</div>'
    + '<p class="img-card__id"><code>' + esc(e.id) + '</code></p>'
    + '</article>';
}

function render() {
  if (_rendering) return;
  _rendering = true;

  const f = currentFilters();
  const data = currentData();
  const filtered = data.filter(e => matches(e, f));
  if (currentView === 'sessions') {
    resultsMeta.textContent = filtered.length + ' seance' + (filtered.length > 1 ? 's' : '');
  } else {
    resultsMeta.textContent = filtered.length + ' entree' + (filtered.length > 1 ? 's' : '') + ' image/reference';
  }

  const container = currentView === 'sessions' ? sessionsSections : imagesSections;
  container.innerHTML = '';

  if (!filtered.length) {
    container.innerHTML = '<p class="img-empty">Aucune entree ne correspond a ces criteres.</p>';
    _rendering = false;
    return;
  }

  if (currentView === 'sessions') {
    const byPhotographer = new Map();
    filtered.forEach(e => {
      const key = e.photographer;
      if (!byPhotographer.has(key)) byPhotographer.set(key, []);
      byPhotographer.get(key).push(e);
    });
    const order = [...byPhotographer.keys()].sort((a, b) =>
      photographerName(a).localeCompare(photographerName(b)));
    order.forEach(key => {
      const group = byPhotographer.get(key);
      if (!group || !group.length) return;
      group.sort((a, b) => a.date.localeCompare(b.date));
      const section = document.createElement('section');
      section.className = 'img-section';
      section.innerHTML = '<div class="img-section__header">'
        + '<h2 class="img-section__title">' + esc(photographerName(key))
        + ' <span class="img-section__count">' + group.length + '</span></h2></div>'
        + '<div class="img-list">' + group.map(sessionCard).join('') + '</div>';
      container.appendChild(section);
    });
  } else {
    const section = document.createElement('section');
    section.className = 'img-section';
    section.innerHTML = '<div class="img-section__header">'
      + '<h2 class="img-section__title">Images et references'
      + ' <span class="img-section__count">' + filtered.length + '</span></h2></div>'
      + '<div class="img-list">' + filtered.map(imageCard).join('') + '</div>';
    container.appendChild(section);
  }

  handleDeepLink();
  _rendering = false;
}

document.querySelector('.img-layout').addEventListener('click', e => {
  const more = e.target.closest('.img-card__more');
  if (more) {
    const details = more.closest('.img-card').querySelector('.img-card__details');
    const opening = details.hasAttribute('hidden');
    details.toggleAttribute('hidden', !opening);
    more.setAttribute('aria-expanded', opening ? 'true' : 'false');
    more.textContent = opening ? 'Voir moins' : 'Voir plus';
  }
});

function exportCSV() {
  const f = currentFilters();
  const data = currentData();
  const rows = [['image_id', 'level', 'canonical_name', 'photographer', 'date',
    'date_precision', 'context', 'place', 'iconic', 'source_url', 'rights_status', 'sources']];
  data.filter(e => matches(e, f)).forEach(e => {
    rows.push([e.id, e.level, e.name, photographerName(e.photographer), e.date,
      e.datePrecision, e.context, e.place || '', e.iconic ? 'oui' : 'non',
      e.sourceUrl || '', e.rightsStatus || '', e.sources.join(' | ')]);
  });
  const csv = rows.map(r => r.map(v => '"' + String(v ?? '').replace(/"/g, '""') + '"').join(',')).join('\n');
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'joy_division_images_canonical_register.csv';
  a.click();
  URL.revokeObjectURL(a.href);
}

function onFilterChange() { refreshFacets(); render(); }
[searchInput, contextFilter, photographerFilter, yearFilter].forEach(el =>
  el.addEventListener('input', onFilterChange));
resetButton.addEventListener('click', () => {
  searchInput.value = ''; contextFilter.value = ''; photographerFilter.value = ''; yearFilter.value = '';
  refreshFacets(); render();
});
downloadButton.addEventListener('click', exportCSV);

loadImages().catch(err => {
  console.error(err);
  statusEl.style.display = '';
  statusEl.textContent = 'Erreur de chargement du registre iconographique : ' + err.message;
});
