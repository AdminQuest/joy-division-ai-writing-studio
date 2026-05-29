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
const themesOf = d => A(d.themes || d.keywords || d.motifs || d.related_motifs || d.concepts || d.usage);
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
        separate_from: d.separate_from || ''
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
// Full-text haystack (ported from the original register: mentions are indexed
// via JSON.stringify of their data — refined in a follow-up commit).
function searchIndex(group) {
  const c = group.canonical;
  return [
    c.song, ...c.aliases, ...c.albums, c.period, c.category, c.status, ...c.variants, c.separate_from,
    ...group.sourceRoots, ...group.sourceRoots.map(sourceLabel), ...group.chapters, ...group.themes,
    ...group.records.map(r => JSON.stringify(r.data || {}) + ' ' + r.id + ' ' + r.file)
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
      + '<div class="song-card__heading"><h3 class="song-card__title">' + esc(c.song) + '</h3>'
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

/* ── Interactions (délégation, accessibles clavier) ─────── */
sectionsEl.addEventListener('click', e => {
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
