/* Registre des chansons — logique d'affichage.
   Groupage par catégorie, facettes croisées (boucle de stabilisation),
   "Voir plus" accessible, pictos SVG par catégorie. La logique de rattachement
   des mentions atomisées au canon (extractCanonicalSongs / canonicalForRecord /
   groupSongRecords) est préservée telle quelle. Data lue via DynamicRegisters. */

const searchInput = document.getElementById('search');
const categoryFilter = document.getElementById('category-filter');
const periodFilter = document.getElementById('period-filter');
const statusFilter = document.getElementById('status-filter');
const sourceFilter = document.getElementById('source-filter');
const chapterFilter = document.getElementById('chapter-filter');
const resetButton = document.getElementById('reset-filters');
const downloadButton = document.getElementById('download-csv');
const resultsMeta = document.getElementById('results-meta');
const statusEl = document.getElementById('songs-status');
const sectionsEl = document.getElementById('songs-sections');
const listHero = document.getElementById('list-hero');
const listView = document.getElementById('list-view');
const detailView = document.getElementById('detail-view');

let songGroups = [];
let canonicalSongs = [];
let rawSongRecords = [];
let sourceLabels = {};
let aliasIndex = new Map();

const T = v => DynamicRegisters.text(v);
const A = v => DynamicRegisters.array(v);
const U = v => DynamicRegisters.uniq(v);
const sourceIds = item => DynamicRegisters.sourceIds(item);
const sourceLabel = id => sourceLabels[id] || id || '';
// Aggregate atom-level source ids (e.g. "S02-A003") to their chapter root
// ("S02") so the Source filter exposes readable roots, not raw atom codes.
const sourceRoot = s => { const m = /^(S\d+)-A\d+$/.exec(T(s)); return m ? m[1] : T(s); };
const chaptersOf = d => A(d.chapters || d.chapitres);
const rawSongTitle = d => d.song || d.titre || d.title || d.canonical_song || d.id || '';
// Real thematic fields only — NOT usage (long prose): usage stays indexed for
// search and is shown verbatim in the mentions list, so the "Thèmes" tags stay
// genuinely compact (the section is simply omitted when no structured theme
// data exists, rather than echoing full usage sentences).
const themesOf = d => A(d.themes || d.keywords || d.motifs || d.related_motifs || d.concepts);
const norm = value => T(value).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[’‘]/g, "'").replace(/[“”«»]/g, '').replace(/\.\.\.|…/g, '').replace(/[^a-z0-9]+/g, ' ').trim();
const esc = s => T(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

// Canonical enum orders (mirror schemas/song.schema.json) for facet ordering.
const PERIOD_ORDER = ['Joy Division', 'Warsaw', 'Warsaw / Joy Division', 'Joy Division / New Order'];
const STATUS_ORDER = ['canonique', 'canonique élargi', 'cas-limite inclus', 'canonique distinct'];
const MENTIONS_MAX = 30;
const EXTRACT_MAX = 180;

async function loadSongs() {
  sourceLabels = await DynamicRegisters.sourceLabels();
  const allSongs = await DynamicRegisters.loadRecords({ prefixes: ['registers/songs/', 'registers/', 'sources/'], kinds: ['song'] });
  const atomRecords = await DynamicRegisters.loadRecords({ prefixes: ['sources/'], kinds: ['atom'] });

  canonicalSongs = extractCanonicalSongs(allSongs);
  buildAliasIndexes(canonicalSongs);

  const songMentions = allSongs.filter(item => !isCanonControlRecord(item));
  const atomMentions = atomRecords.filter(item => canonicalForRecord(item));
  rawSongRecords = [...songMentions, ...atomMentions];

  songGroups = groupSongRecords(canonicalSongs, rawSongRecords);
  statusEl.style.display = 'none';
  refreshFacets();
  render();
  route(); // honore ?id= / ?slug= / ?focus= présent dès le chargement
}

/* ── Rattachement canon ↔ mentions (préservé de la version d'origine) ── */
function isCanonControlRecord(item) {
  const d = item.data || {};
  return item.file.startsWith('registers/songs/') || d.type_unite === 'song_canon' || String(d.id || '').startsWith('JD-SONG-');
}

function extractCanonicalSongs(records) {
  const byId = new Map();
  records
    .map(item => item.data || {})
    .filter(d => d.type_unite === 'song' && d.canonical_song === true && d.exclude !== true)
    .forEach(d => {
      const prev = byId.get(d.id);
      byId.set(d.id, {
        id: d.id,
        song: d.song,
        slug: d.slug,
        category: d.category || '',
        period: d.period || '',
        status: d.status || '',
        aliases: U([d.song, ...(d.aliases || [])]),
        albums: A(d.albums),
        variants: A(d.include_variants),
        // separate_from may live on only one of several same-id canonical blocks
        // (e.g. the standalone JD-SONG-051 file vs the 00_canonical inline entry).
        // Preserve it across the id-dedup regardless of file order so the
        // "Distinct de" link always renders.
        separate_from: d.separate_from || (prev && prev.separate_from) || ''
      });
    });
  return [...byId.values()];
}

function buildAliasIndexes(canon) {
  aliasIndex = new Map();
  canon.forEach(song => {
    const titleKey = norm(song.song);
    if (titleKey) aliasIndex.set(titleKey, song);
    song.aliases.forEach(alias => {
      const key = norm(alias);
      if (!key) return;
      // Do not let ambiguous bare aliases such as "the kill" override an explicit distinct title.
      if (!aliasIndex.has(key)) aliasIndex.set(key, song);
    });
  });
}

function canonicalForRecord(item) {
  const d = item.data || {};
  if (d.song_id) return canonicalSongs.find(s => s.id === d.song_id) || null;
  const direct = aliasIndex.get(norm(rawSongTitle(d)));
  if (direct) return direct;
  const simplified = norm(rawSongTitle(d)).replace(/^the /, '');
  for (const [alias, song] of aliasIndex.entries()) {
    if (alias.replace(/^the /, '') === simplified) return song;
  }
  return null;
}

function groupSongRecords(canon, records) {
  return canon.map(song => {
    const linked = records.filter(record => canonicalForRecord(record)?.id === song.id);
    return {
      canonical: song,
      records: linked,
      sourceRoots: U(linked.flatMap(sourceIds).map(sourceRoot)),
      themes: U(linked.flatMap(x => themesOf(x.data || {}))),
      chapters: U(linked.flatMap(x => chaptersOf(x.data || {})))
    };
  });
}

/* ── Filtres / facettes ─────────────────────────────────── */
function currentFilters() {
  return {
    q: searchInput.value.toLowerCase().trim(),
    category: categoryFilter.value,
    period: periodFilter.value,
    status: statusFilter.value,
    source: sourceFilter.value,
    chapter: chapterFilter.value
  };
}
// Full-text index built from useful fields only. The original register fed
// JSON.stringify(record.data) into the haystack, which leaked YAML field names
// (usage, type_unite, source_id…) into search and produced false positives.
// Index instead the meaningful mention fields: title, short extract, and ids.
function searchIndex(group) {
  const c = group.canonical;
  return [
    c.song, ...c.aliases, ...c.albums, c.period, c.category, c.status, ...c.variants, c.separate_from,
    ...group.sourceRoots, ...group.sourceRoots.map(sourceLabel), ...group.chapters, ...group.themes,
    ...group.records.flatMap(r => { const d = r.data || {}; return [rawSongTitle(d), d.usage, d.id, r.id]; })
  ].map(T).join(' ').toLowerCase();
}
function matches(group, f, except) {
  const c = group.canonical;
  if (except !== 'q' && f.q && !searchIndex(group).includes(f.q)) return false;
  if (except !== 'category' && f.category && c.category !== f.category) return false;
  if (except !== 'period' && f.period && c.period !== f.period) return false;
  if (except !== 'status' && f.status && c.status !== f.status) return false;
  if (except !== 'source' && f.source && !group.sourceRoots.includes(f.source)) return false;
  if (except !== 'chapter' && f.chapter && !group.chapters.includes(f.chapter)) return false;
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
  // (guarded against infinite loops — same pattern as the places register).
  for (let pass = 0; pass < 5; pass++) {
    const f = currentFilters();
    const categoryVals = SongIcons.order.filter(cat =>
      songGroups.some(g => g.canonical.category === cat && matches(g, f, 'category')));
    const periodVals = PERIOD_ORDER.filter(p =>
      songGroups.some(g => g.canonical.period === p && matches(g, f, 'period')));
    const statusVals = STATUS_ORDER.filter(s =>
      songGroups.some(g => g.canonical.status === s && matches(g, f, 'status')));
    let cleaned = false;
    cleaned = setOptions(categoryFilter, categoryVals, 'Toutes') || cleaned;
    cleaned = setOptions(periodFilter, periodVals, 'Toutes') || cleaned;
    cleaned = setOptions(statusFilter, statusVals, 'Tous') || cleaned;
    cleaned = setOptions(sourceFilter, U(songGroups.filter(g => matches(g, f, 'source')).flatMap(g => g.sourceRoots)).sort(), 'Toutes', sourceLabel) || cleaned;
    cleaned = setOptions(chapterFilter, U(songGroups.filter(g => matches(g, f, 'chapter')).flatMap(g => g.chapters)).sort(undefined, { numeric: true }), 'Tous') || cleaned;
    if (!cleaned) break;
  }
}

/* ── Rendu ──────────────────────────────────────────────── */
function tags(values) {
  const v = A(values).filter(Boolean);
  return v.length ? '<div class="song-tags">' + v.map(x => '<span class="song-tag">' + esc(x) + '</span>').join('') + '</div>' : '';
}
function detail(label, content) {
  return content ? '<div class="song-detail"><p class="song-detail__label">' + esc(label) + '</p>' + content + '</div>' : '';
}
function mentionsBlock(group) {
  if (!group.records.length) return '';
  const shown = group.records.slice(0, MENTIONS_MAX);
  const rows = shown.map(item => {
    const d = item.data || {};
    const label = item.kind === 'atom' ? 'Atome' : 'Mention';
    let extract = T(d.usage).trim();
    if (extract.length > EXTRACT_MAX) extract = extract.slice(0, EXTRACT_MAX).trimEnd() + '…';
    const roots = U(sourceIds(item).map(sourceRoot)).map(sourceLabel).join(' · ');
    return '<div class="song-mention">'
      + '<div class="song-mention__head">' + esc(label) + ' — ' + esc(rawSongTitle(d))
      + ' <span class="song-mention__id">' + esc(d.id || item.id) + (roots ? ' · ' + esc(roots) : '') + '</span></div>'
      + (extract ? '<p class="song-mention__extract">' + esc(extract) + '</p>' : '')
      + '</div>';
  }).join('');
  const more = group.records.length > MENTIONS_MAX
    ? '<p class="song-mentions__more">+' + (group.records.length - MENTIONS_MAX) + ' autre(s) mention(s) masquée(s).</p>'
    : '';
  return detail('Mentions atomisées rattachées', '<div class="song-mentions">' + rows + more + '</div>');
}
function card(group) {
  const c = group.canonical;
  const aliases = c.aliases.filter(x => x !== c.song);
  const mentionCount = group.records.length;

  const details = detail('Chapitres', tags(group.chapters))
    + detail('Sources', tags(group.sourceRoots.map(sourceLabel)))
    + detail('Variantes retenues', tags(c.variants))
    + detail('Thèmes / mots-clés', tags(group.themes.slice(0, 24)))
    + mentionsBlock(group);

  // separate_from → clickable scroll link to the target canonical card.
  let separate = '';
  if (c.separate_from) {
    const m = /^(JD-SONG-\d{3})/.exec(c.separate_from);
    separate = m
      ? '<div class="song-card__separate">Distinct de <a class="song-card__separate-link" href="#song-' + m[1] + '" data-target="song-' + m[1] + '">' + esc(c.separate_from) + '</a></div>'
      : '<div class="song-card__separate">Distinct de ' + esc(c.separate_from) + '</div>';
  }

  return '<article class="song-card" id="song-' + esc(c.id) + '"' + (c.slug ? ' data-slug="' + esc(c.slug) + '"' : '') + '>'
    + '<div class="song-card__header">' + SongIcons.svg(c.category)
      + '<div class="song-card__heading"><h3 class="song-card__title">'
        + '<a class="song-card__title-link" href="?slug=' + esc(c.slug || c.id) + '" data-slug="' + esc(c.slug || '') + '" data-id="' + esc(c.id) + '">' + esc(c.song) + '</a></h3>'
      + (c.period ? '<p class="song-card__period">' + esc(c.period) + '</p>' : '') + '</div></div>'
    + '<div class="song-card__badges">'
      + (c.status ? '<span class="song-badge">' + esc(c.status) + '</span>' : '')
      + (mentionCount ? '<span class="song-badge">' + mentionCount + ' mention' + (mentionCount > 1 ? 's' : '') + '</span>'
                      : '<span class="song-badge song-badge--muted">aucune mention</span>')
    + '</div>'
    + (c.albums.length ? '<p class="song-card__line"><strong>Albums / corpus :</strong> ' + esc(c.albums.join(', ')) + '</p>' : '')
    + (aliases.length ? '<p class="song-card__line"><strong>Alias :</strong> ' + esc(aliases.join(', ')) + '</p>' : '')
    + (details ? '<button type="button" class="song-card__more" aria-expanded="false">Voir plus</button>'
        + '<div class="song-card__details" hidden>' + details + '</div>' : '')
    + separate
    + '<p class="song-card__id"><code>' + esc(c.id) + '</code></p>'
    + '</article>';
}
function render() {
  const f = currentFilters();
  const filtered = songGroups.filter(g => matches(g, f));
  resultsMeta.textContent = filtered.length + ' titre' + (filtered.length > 1 ? 's' : '') + ' canonique' + (filtered.length > 1 ? 's' : '');
  sectionsEl.innerHTML = '';
  if (!filtered.length) {
    sectionsEl.innerHTML = '<p class="songs-empty">Aucune chanson ne correspond à ces critères.</p>';
    return;
  }
  const byCategory = new Map();
  filtered.forEach(g => {
    const cat = g.canonical.category || 'generic';
    if (!byCategory.has(cat)) byCategory.set(cat, []);
    byCategory.get(cat).push(g);
  });
  // Sections in canonical category order, then any leftover categories.
  const order = [...SongIcons.order, ...[...byCategory.keys()].filter(c => !SongIcons.order.includes(c))];
  order.forEach(cat => {
    const group = byCategory.get(cat);
    if (!group || !group.length) return;
    group.sort((a, b) => T(a.canonical.song).localeCompare(T(b.canonical.song), undefined, { numeric: true }));
    const section = document.createElement('section');
    section.className = 'songs-section';
    section.innerHTML = '<div class="songs-section__header">' + SongIcons.svg(cat)
      + '<h2 class="songs-section__title">' + esc(SongIcons.label(cat))
      + ' <span class="songs-section__count">' + group.length + '</span></h2></div>'
      + '<div class="songs-list">' + group.map(card).join('') + '</div>';
    sectionsEl.appendChild(section);
  });
}

/* ── Matching tactique vers le registre des releases (12b-2.c MVP) ──────
   Seul cross-repo de ce MVP. Le JSON consolidé de joy-division-releases ne
   porte PAS de tracklist par piste : chaque variante est indexée par un unique
   `canonical_title` (titre du single/EP, ou de l'album). Le matching se fait
   donc titre/alias canonique ↔ canonical_title normalisé. Tactique et imparfait
   (faux positifs sur titres proches, faux négatifs sur "… (Live)", appartenance
   à un album non résolue piste-à-piste). Une FK propre song_id est différée en
   12b-2.c étendu. Le fetch n'a lieu qu'une fois par session (cache mémoire). */
const RELEASES_BASE = 'https://adminquest.github.io/joy-division-releases/';
const RELEASES_JSON = RELEASES_BASE + 'data/all-variants.json';
let releasesPromise = null;
function loadReleases() {
  if (!releasesPromise) {
    releasesPromise = fetch(RELEASES_JSON, { cache: 'no-store' })
      .then(r => { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
      .then(j => Array.isArray(j.variants) ? j.variants : []);
  }
  return releasesPromise;
}
// Clés normalisées d'une chanson canonique (titre + alias), avec variante
// sans "the " initial pour absorber les divergences d'article — même esprit
// que canonicalForRecord().
function songTitleKeys(song) {
  const keys = new Set();
  [song.song, ...(song.aliases || [])].forEach(t => {
    const k = norm(t);
    if (!k) return;
    keys.add(k);
    keys.add(k.replace(/^the /, ''));
  });
  return keys;
}
function matchReleases(variants, song) {
  const keys = songTitleKeys(song);
  return variants.filter(v => {
    const t = norm(v.canonical_title);
    return t && (keys.has(t) || keys.has(t.replace(/^the /, '')));
  });
}

/* ── Routing : ?id=JD-SONG-NNN | ?slug=… → page de détail ─────────────── */
function findGroup({ id, slug }) {
  if (id) return songGroups.find(g => g.canonical.id === id) || null;
  if (slug) {
    const key = norm(slug);
    return songGroups.find(g => norm(g.canonical.slug) === key
      || norm(g.canonical.song) === key) || null;
  }
  return null;
}
function showListView() {
  detailView.hidden = true;
  detailView.innerHTML = '';
  listHero.hidden = false;
  listView.hidden = false;
}
function focusCard(id) {
  const el = document.getElementById('song-' + id);
  if (!el) return;
  el.scrollIntoView({ behavior: 'smooth', block: 'center' });
  el.classList.add('song-card--target');
  setTimeout(() => el.classList.remove('song-card--target'), 1600);
}
// Point d'entrée du routage : appelé au chargement, sur navigation interne
// (pushState) et sur popstate. Décide liste vs détail à partir de l'URL.
function route() {
  const p = new URLSearchParams(location.search);
  const id = p.get('id');
  const slug = p.get('slug');
  if (id || slug) {
    const group = findGroup({ id, slug });
    if (group) renderDetail(group);
    else renderDetailNotFound(id || slug);
    return;
  }
  showListView();
  const focus = p.get('focus');
  if (focus) {
    // La liste peut être filtrée : on réinitialise pour garantir la présence
    // de la card ciblée, puis on la met en évidence.
    resetFilters(); refreshFacets(); render();
    requestAnimationFrame(() => focusCard(focus));
  }
}
// Navigation interne sans rechargement (préserve le fetch unique des chansons).
function navigateTo(query) {
  history.pushState(null, '', query);
  route();
  window.scrollTo({ top: 0, behavior: 'auto' });
}
window.addEventListener('popstate', route);

/* ── Rendu de la page de détail ───────────────────────────────────────── */
function detailRow(label, valueHtml) {
  return valueHtml
    ? '<div class="song-detail-canon__row"><dt>' + esc(label) + '</dt><dd>' + valueHtml + '</dd></div>'
    : '';
}
function detailSection(title, bodyHtml, extraClass) {
  return '<section class="song-detail-section' + (extraClass ? ' ' + extraClass : '') + '">'
    + '<h2 class="song-detail-section__title">' + esc(title) + '</h2>'
    + bodyHtml + '</section>';
}
function renderDetailShell(group, releasesHtml) {
  const c = group.canonical;
  const aliases = c.aliases.filter(x => x !== c.song);
  const editorUrl = (window.LocalEditorLinks && window.LocalEditorLinks.urlFor({ slug: c.slug, title: c.song })) || '';

  // separate_from → lien cliquable vers la liste, card cible en focus.
  let separateHtml = '';
  if (c.separate_from) {
    const m = /^(JD-SONG-\d{3})/.exec(c.separate_from);
    separateHtml = m
      ? '<a class="song-detail-link" href="?focus=' + esc(m[1]) + '" data-focus="' + esc(m[1]) + '">' + esc(c.separate_from) + '</a>'
      : esc(c.separate_from);
  }

  const canon = '<dl class="song-detail-canon">'
    + detailRow('Identifiant', '<code>' + esc(c.id) + '</code>')
    + detailRow('Slug', c.slug ? '<code>' + esc(c.slug) + '</code>' : '')
    + detailRow('Catégorie', esc(c.category))
    + detailRow('Période', esc(c.period))
    + detailRow('Statut', esc(c.status))
    + detailRow('Albums / corpus', c.albums.length ? esc(c.albums.join(', ')) : '')
    + detailRow('Alias', aliases.length ? esc(aliases.join(', ')) : '')
    + detailRow('Variantes retenues', c.variants.length ? esc(c.variants.join(', ')) : '')
    + detailRow('Distinct de', separateHtml)
    + '</dl>';

  const mentions = group.records.length
    ? mentionsBlock(group)
    : '<p class="song-detail-empty">Aucune mention atomisée rattachée.</p>';
  const chapters = group.chapters.length
    ? tags(group.chapters)
    : '<p class="song-detail-empty">Aucun chapitre référencé.</p>';
  const sources = group.sourceRoots.length
    ? tags(group.sourceRoots.map(sourceLabel))
    : '<p class="song-detail-empty">Aucune source référencée.</p>';

  detailView.innerHTML =
    '<a class="song-detail-back songs-hero__back" href="?focus=' + esc(c.id) + '" data-focus="' + esc(c.id) + '">← Retour au registre</a>'
    + '<header class="song-detail-hero">'
      + '<div class="song-detail-hero__icon">' + SongIcons.svg(c.category) + '</div>'
      + '<div class="song-detail-hero__heading">'
        + '<h1 class="song-detail-hero__title">' + esc(c.song) + '</h1>'
        + (c.period ? '<p class="song-detail-hero__period">' + esc(c.period) + '</p>' : '')
        + '<div class="song-detail-hero__badges">'
          + (c.category ? '<span class="song-badge">' + esc(c.category) + '</span>' : '')
          + (c.status ? '<span class="song-badge">' + esc(c.status) + '</span>' : '')
        + '</div>'
      + '</div>'
      + (editorUrl ? '<a class="song-card__editor-link song-detail-hero__editor" href="' + esc(editorUrl) + '" target="_blank" rel="noopener noreferrer" title="Éditeur de Songbook — GitHub Pages (token requis).">ouvrir éditeur</a>' : '')
    + '</header>'
    + detailSection('Canon public', canon, 'song-detail-section--canon')
    + detailSection('Mentions atomisées rattachées', mentions)
    + detailSection('Chapitres référencés', chapters)
    + detailSection('Sources', sources)
    + '<section class="song-detail-section" id="detail-releases">' + releasesHtml + '</section>';

  listHero.hidden = true;
  listView.hidden = true;
  detailView.hidden = false;
}
function releasesPlaceholderHtml() {
  return '<h2 class="song-detail-section__title">Présent sur les releases</h2>'
    + '<p class="song-detail-loading">Recherche dans le registre des releases…</p>';
}
function releaseItemHtml(v) {
  const title = esc(v.canonical_title || '(sans titre)');
  const vid = esc(v.variant_id || '');
  const type = v.release_type || '';
  // Pas de deep-link par variante côté joy-division-releases : on pointe la
  // racine du registre avec un indice de recherche (cohérence forward).
  const href = RELEASES_BASE + (title ? '?search=' + encodeURIComponent(v.canonical_title || '') : '');
  return '<a class="song-release" href="' + href + '" target="_blank" rel="noopener noreferrer">'
    + '<span class="song-release__icon">' + SongIcons.releaseSvg(type) + '</span>'
    + '<span class="song-release__body">'
      + '<span class="song-release__title">' + title + '</span>'
      + '<span class="song-release__meta">' + (vid ? '<code>' + vid + '</code>' : '')
        + (type ? ' <span class="song-release__type">' + esc(SongIcons.releaseLabel(type)) + '</span>' : '') + '</span>'
    + '</span></a>';
}
const RELEASE_TYPE_ORDER = ['officiel', 'coffret', 'pirate', 'bootleg', 'video', 'livre', 'para'];
function renderReleasesSection(song) {
  const host = document.getElementById('detail-releases');
  if (!host) return;
  loadReleases().then(variants => {
    const matched = matchReleases(variants, song);
    if (!matched.length) {
      host.innerHTML = '<h2 class="song-detail-section__title">Présent sur les releases</h2>'
        + '<p class="song-detail-empty">Aucune release ne correspond au titre normalisé de cette chanson.</p>'
        + releasesDisclaimerHtml();
      return;
    }
    matched.sort((a, b) => {
      const ra = RELEASE_TYPE_ORDER.indexOf(a.release_type);
      const rb = RELEASE_TYPE_ORDER.indexOf(b.release_type);
      if (ra !== rb) return (ra < 0 ? 99 : ra) - (rb < 0 ? 99 : rb);
      return T(a.variant_id).localeCompare(T(b.variant_id), undefined, { numeric: true });
    });
    host.innerHTML = '<h2 class="song-detail-section__title">Présent sur les releases '
      + '<span class="song-detail-section__count">' + matched.length + '</span></h2>'
      + '<div class="song-releases">' + matched.map(releaseItemHtml).join('') + '</div>'
      + releasesDisclaimerHtml();
  }).catch(err => {
    console.warn('[song-detail] releases indisponibles :', err);
    host.innerHTML = '<h2 class="song-detail-section__title">Présent sur les releases</h2>'
      + '<p class="song-detail-empty song-detail-warning">Releases non disponibles (le registre n\'a pas pu être chargé).</p>';
  });
}
function releasesDisclaimerHtml() {
  return '<p class="song-detail-note">Matching tactique par titre. Une liaison FK <code>song_id</code> propre est prévue en phase ultérieure (12b-2.c étendu).</p>';
}
function renderDetail(group) {
  renderDetailShell(group, releasesPlaceholderHtml());
  renderReleasesSection(group.canonical);
}
function renderDetailNotFound(ref) {
  listHero.hidden = true;
  listView.hidden = true;
  detailView.hidden = false;
  detailView.innerHTML =
    '<a class="song-detail-back songs-hero__back" href="./" data-home="1">← Retour au registre</a>'
    + '<div class="song-detail-notfound">'
      + '<h1>Chanson non trouvée</h1>'
      + '<p>Aucune chanson canonique ne correspond à <code>' + esc(ref) + '</code>.</p>'
    + '</div>';
}

/* ── Interactions (délégation, accessibles clavier) ─────── */
sectionsEl.addEventListener('click', e => {
  // Clic sur le titre d'une card → ouvre la page de détail (nav interne).
  const titleLink = e.target.closest('.song-card__title-link');
  if (titleLink) {
    e.preventDefault();
    const slug = titleLink.dataset.slug;
    navigateTo(slug ? '?slug=' + encodeURIComponent(slug) : '?id=' + encodeURIComponent(titleLink.dataset.id));
    return;
  }
  const more = e.target.closest('.song-card__more');
  if (more) {
    const details = more.closest('.song-card').querySelector('.song-card__details');
    const opening = details.hasAttribute('hidden');
    details.toggleAttribute('hidden', !opening);
    more.setAttribute('aria-expanded', opening ? 'true' : 'false');
    more.textContent = opening ? 'Voir moins' : 'Voir plus';
    return;
  }
  const link = e.target.closest('.song-card__separate-link');
  if (link) {
    e.preventDefault();
    const targetId = link.dataset.target;
    let el = document.getElementById(targetId);
    if (!el) { resetFilters(); refreshFacets(); render(); el = document.getElementById(targetId); }
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'center' });
      el.classList.add('song-card--target');
      setTimeout(() => el.classList.remove('song-card--target'), 1600);
    }
  }
});

// Liens internes de la page de détail (retour, distinct de, accueil) :
// navigation sans rechargement pour préserver le fetch unique des chansons.
detailView.addEventListener('click', e => {
  const link = e.target.closest('a[data-focus], a[data-home]');
  if (!link) return;
  e.preventDefault();
  navigateTo(link.hasAttribute('data-home') ? './' : '?focus=' + encodeURIComponent(link.dataset.focus));
});

/* ── Export CSV (jeu filtré courant) ────────────────────── */
function exportCSV() {
  const f = currentFilters();
  const rows = [['id', 'song', 'category', 'period', 'status', 'aliases', 'albums', 'variants', 'atomized_mentions', 'sources', 'chapters']];
  songGroups.filter(g => matches(g, f)).forEach(g => {
    const c = g.canonical;
    rows.push([c.id, c.song, c.category, c.period, c.status,
      c.aliases.filter(x => x !== c.song).join(' | '), c.albums.join(' | '), c.variants.join(' | '),
      g.records.length, g.sourceRoots.map(sourceLabel).join(' | '), g.chapters.join(' | ')]);
  });
  const csv = rows.map(r => r.map(v => '"' + String(v ?? '').replace(/"/g, '""') + '"').join(',')).join('\n');
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'joy_division_songs_canonical_register.csv';
  a.click();
  URL.revokeObjectURL(a.href);
}

/* ── Événements ─────────────────────────────────────────── */
function onFilterChange() { refreshFacets(); render(); }
function resetFilters() {
  searchInput.value = ''; categoryFilter.value = ''; periodFilter.value = '';
  statusFilter.value = ''; sourceFilter.value = ''; chapterFilter.value = '';
}
[searchInput, categoryFilter, periodFilter, statusFilter, sourceFilter, chapterFilter].forEach(el => el.addEventListener('input', onFilterChange));
resetButton.addEventListener('click', () => { resetFilters(); refreshFacets(); render(); });
downloadButton.addEventListener('click', exportCSV);

loadSongs().catch(err => {
  console.error(err);
  statusEl.style.display = '';
  statusEl.textContent = 'Erreur de chargement dynamique du registre des chansons : ' + err.message;
});
