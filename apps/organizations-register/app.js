const searchInput = document.getElementById('search');
const categoryFilter = document.getElementById('category-filter');
const statusFilter = document.getElementById('status-filter');
const resetButton = document.getElementById('reset-filters');
const downloadButton = document.getElementById('download-csv');
const resultsMeta = document.getElementById('results-meta');
const statusEl = document.getElementById('org-status');
const sectionsEl = document.getElementById('org-sections');

let orgs = [];

const ORGS_URL = '../../registers/orgs/orgs.json';

const CATEGORY_META = {
  group:       { label: 'Groupe',       order: 0 },
  label:       { label: 'Label',        order: 1 },
  institution: { label: 'Institution',  order: 2 },
  venue_org:   { label: 'Salle / org.', order: 3 },
  crew:        { label: 'Equipe tech.', order: 4 },
  media:       { label: 'Media',        order: 5 },
  other:       { label: 'Autre',        order: 6 }
};

const STATUS_LABELS = {
  active: 'Actif',
  dissolved: 'Dissous',
  dormant: 'Dormant',
  unknown: 'Inconnu'
};

const esc = s => String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

function categoryLabel(cat) {
  return (CATEGORY_META[cat] || {}).label || cat;
}

function categoryOrder(cat) {
  return (CATEGORY_META[cat] || {}).order ?? 99;
}

async function loadOrgs() {
  const resp = await fetch(ORGS_URL, { cache: 'no-store' });
  if (!resp.ok) throw new Error('HTTP ' + resp.status);
  const data = await resp.json();
  orgs = data.map(entry => ({
    id: entry.org_id,
    name: entry.canonical_name || '',
    aliases: entry.aliases || [],
    category: entry.category || 'other',
    subcategory: entry.subcategory || '',
    country: entry.country || '',
    city: entry.city || '',
    activeFrom: entry.active_from || '',
    activeUntil: entry.active_until || '',
    status: entry.status || 'unknown',
    sameAs: entry.same_as || {},
    relation: entry.joy_division_relation || {},
    sources: entry.sources || [],
    gate: entry.gate || 'public',
    lastVerified: entry.last_verified || ''
  }));
  // GitHub Pages has no auth context — unconditionally drop private entries.
  orgs = orgs.filter(o => o.gate === 'public');
  orgs.sort((a, b) => a.name.localeCompare(b.name, undefined, { numeric: true }));

  statusEl.style.display = 'none';

  handleDeepLink();
  refreshFacets();
  render();
}

function handleDeepLink() {
  const params = new URLSearchParams(window.location.search);
  const targetId = params.get('id');
  if (!targetId) return;
  requestAnimationFrame(() => {
    const el = document.getElementById(targetId);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      el.style.outline = '2px solid var(--accent)';
      setTimeout(() => { el.style.outline = ''; }, 3000);
    }
  });
}

function currentFilters() {
  return {
    q: searchInput.value.toLowerCase().trim(),
    category: categoryFilter.value,
    status: statusFilter.value
  };
}

function searchIndex(o) {
  return [o.name, ...o.aliases, o.category, o.subcategory, o.city, o.country,
    o.status, o.id, ...o.sources, (o.relation.notes || '')].join(' ').toLowerCase();
}

function matches(o, f, except) {
  if (except !== 'q' && f.q && !searchIndex(o).includes(f.q)) return false;
  if (except !== 'category' && f.category && o.category !== f.category) return false;
  if (except !== 'status' && f.status && o.status !== f.status) return false;
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
  for (let pass = 0; pass < 5; pass++) {
    const f = currentFilters();
    const cats = uniq(orgs.filter(o => matches(o, f, 'category')).map(o => o.category))
      .sort((a, b) => categoryOrder(a) - categoryOrder(b));
    const statuses = uniq(orgs.filter(o => matches(o, f, 'status')).map(o => o.status));
    let cleaned = false;
    cleaned = setOptions(categoryFilter, cats, 'Toutes', categoryLabel) || cleaned;
    cleaned = setOptions(statusFilter, statuses, 'Tous', v => STATUS_LABELS[v] || v) || cleaned;
    if (!cleaned) break;
  }
}

function sameAsLinks(sameAs) {
  const links = [];
  if (sameAs.wikidata) {
    links.push('<a href="https://www.wikidata.org/wiki/' + esc(sameAs.wikidata) + '" target="_blank" rel="noopener">Wikidata</a>');
  }
  if (sameAs.discogs) {
    links.push('<a href="' + esc(sameAs.discogs) + '" target="_blank" rel="noopener">Discogs</a>');
  }
  if (sameAs.musicbrainz) {
    links.push('<a href="https://musicbrainz.org/artist/' + esc(sameAs.musicbrainz) + '" target="_blank" rel="noopener">MusicBrainz</a>');
  }
  return links.length ? '<div class="org-card__links">' + links.join('') + '</div>' : '';
}

function periodStr(o) {
  if (o.activeFrom && o.activeUntil) return o.activeFrom + ' – ' + o.activeUntil;
  if (o.activeFrom) return o.activeFrom + ' – present';
  return '';
}

function detail(label, content) {
  return content ? '<div class="org-detail"><p class="org-detail__label">' + esc(label) + '</p>' + content + '</div>' : '';
}

function tags(values) {
  const arr = (values || []).filter(Boolean);
  return arr.length ? '<div class="org-tags">' + arr.map(v => '<span class="org-tag">' + esc(v) + '</span>').join('') + '</div>' : '';
}

function card(o) {
  const rel = o.relation || {};
  const hasDetails = o.aliases.length || o.sources.length || rel.notes || Object.keys(o.sameAs).length;

  const relationBlock = rel.notes
    ? '<div class="org-card__relation">'
      + '<p class="org-card__relation-label">Relation a Joy Division'
      + (rel.period ? ' (' + esc(rel.period) + ')' : '') + '</p>'
      + '<p class="org-card__relation-notes">' + esc(rel.notes) + '</p>'
      + '</div>'
    : '';

  const detailsContent = detail('Alias', tags(o.aliases))
    + detail('Sources', tags(o.sources))
    + detail('Pays / Ville', o.country || o.city
        ? '<span class="org-tag">' + esc([o.city, o.country].filter(Boolean).join(', ')) + '</span>'
        : '')
    + sameAsLinks(o.sameAs);

  return '<article class="org-card org-card--' + esc(o.category) + '" id="' + esc(o.id) + '">'
    + '<div class="org-card__header"><div class="org-card__heading">'
    + '<h3 class="org-card__title">' + esc(o.name) + '</h3></div></div>'
    + '<div class="org-card__badges">'
    + '<span class="org-badge org-badge--' + esc(o.category) + '">' + esc(categoryLabel(o.category)) + '</span>'
    + (o.subcategory ? '<span class="org-badge org-badge--category">' + esc(o.subcategory) + '</span>' : '')
    + '<span class="org-badge org-badge--status org-badge--' + esc(o.status) + '">' + esc(STATUS_LABELS[o.status] || o.status) + '</span>'
    + '</div>'
    + (periodStr(o) ? '<p class="org-card__line"><strong>Activite :</strong> ' + esc(periodStr(o)) + '</p>' : '')
    + relationBlock
    + (hasDetails
        ? '<button type="button" class="org-card__more" aria-expanded="false">Voir plus</button>'
          + '<div class="org-card__details" hidden>' + detailsContent + '</div>'
        : '')
    + '<p class="org-card__id"><code>' + esc(o.id) + '</code></p>'
    + '</article>';
}

function render() {
  const f = currentFilters();
  const filtered = orgs.filter(o => matches(o, f));
  resultsMeta.textContent = filtered.length + ' organisation' + (filtered.length > 1 ? 's' : '') + ' canonique' + (filtered.length > 1 ? 's' : '');
  sectionsEl.innerHTML = '';
  if (!filtered.length) {
    sectionsEl.innerHTML = '<p class="org-empty">Aucune organisation ne correspond a ces criteres.</p>';
    return;
  }
  const byCategory = new Map();
  filtered.forEach(o => {
    if (!byCategory.has(o.category)) byCategory.set(o.category, []);
    byCategory.get(o.category).push(o);
  });
  const order = [...byCategory.keys()].sort((a, b) => categoryOrder(a) - categoryOrder(b));
  order.forEach(cat => {
    const group = byCategory.get(cat);
    if (!group || !group.length) return;
    group.sort((a, b) => a.name.localeCompare(b.name, undefined, { numeric: true }));
    const section = document.createElement('section');
    section.className = 'org-section';
    section.innerHTML = '<div class="org-section__header">'
      + '<h2 class="org-section__title">' + esc(categoryLabel(cat))
      + ' <span class="org-section__count">' + group.length + '</span></h2></div>'
      + '<div class="org-list">' + group.map(card).join('') + '</div>';
    sectionsEl.appendChild(section);
  });

  handleDeepLink();
}

sectionsEl.addEventListener('click', e => {
  const more = e.target.closest('.org-card__more');
  if (more) {
    const details = more.closest('.org-card').querySelector('.org-card__details');
    const opening = details.hasAttribute('hidden');
    details.toggleAttribute('hidden', !opening);
    more.setAttribute('aria-expanded', opening ? 'true' : 'false');
    more.textContent = opening ? 'Voir moins' : 'Voir plus';
  }
});

function exportCSV() {
  const f = currentFilters();
  const rows = [['org_id', 'canonical_name', 'category', 'subcategory', 'country', 'city',
    'active_from', 'active_until', 'status', 'gate', 'wikidata', 'joy_division_relation_type', 'sources']];
  orgs.filter(o => matches(o, f)).forEach(o => {
    rows.push([o.id, o.name, o.category, o.subcategory, o.country, o.city,
      o.activeFrom, o.activeUntil || '', o.status, o.gate,
      (o.sameAs || {}).wikidata || '', (o.relation || {}).type || '',
      o.sources.join(' | ')]);
  });
  const csv = rows.map(r => r.map(v => '"' + String(v ?? '').replace(/"/g, '""') + '"').join(',')).join('\n');
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'joy_division_organizations_canonical_register.csv';
  a.click();
  URL.revokeObjectURL(a.href);
}

function onFilterChange() { refreshFacets(); render(); }
[searchInput, categoryFilter, statusFilter].forEach(el => el.addEventListener('input', onFilterChange));
resetButton.addEventListener('click', () => {
  searchInput.value = ''; categoryFilter.value = ''; statusFilter.value = '';
  refreshFacets(); render();
});
downloadButton.addEventListener('click', exportCSV);

loadOrgs().catch(err => {
  console.error(err);
  statusEl.style.display = '';
  statusEl.textContent = 'Erreur de chargement du registre des organisations : ' + err.message;
});
