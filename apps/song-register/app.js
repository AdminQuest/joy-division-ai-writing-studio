const songsList = document.getElementById('songs-list');
const resultsMeta = document.getElementById('results-meta');
const statusCard = document.getElementById('status-card');
const searchInput = document.getElementById('search');
const songFilter = document.getElementById('song-filter');
const sourceFilter = document.getElementById('source-filter');
const typeFilter = document.getElementById('type-filter');
const themeFilter = document.getElementById('theme-filter');
const chapterFilter = document.getElementById('chapter-filter');
const resetButton = document.getElementById('reset-filters');
const downloadButton = document.getElementById('download-csv');

let canonicalSongs = [];
let rawSongRecords = [];
let lyricsEditorialRecords = [];
let songGroups = [];
let sourceLabels = {};
let aliasIndex = new Map();

const T = v => DynamicRegisters.text(v);
const A = v => DynamicRegisters.array(v);
const U = v => DynamicRegisters.uniq(v);
const sourceIds = item => DynamicRegisters.sourceIds(item);
const sourceLabel = id => sourceLabels[id] || id || '';
const chaptersOf = d => A(d.chapters || d.chapitres);
const rawSongTitle = d => d.song || d.titre || d.title || d.canonical_song || d.id || '';
const typesOf = d => A(d.type || d.type_unite || d.kind);
const themesOf = d => A(d.themes || d.keywords || d.motifs || d.related_motifs || d.concepts || d.usage);
const norm = value => T(value).toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[’‘]/g, "'").replace(/[“”«»]/g, '').replace(/\.\.\.|…/g, '').replace(/[^a-z0-9]+/g, ' ').trim();

async function loadSongs() {
  try {
    sourceLabels = await DynamicRegisters.sourceLabels();
    const allSongs = await DynamicRegisters.loadRecords({ prefixes: ['registers/songs/', 'registers/', 'sources/'], kinds: ['song'] });
    const atomRecords = await DynamicRegisters.loadRecords({ prefixes: ['sources/'], kinds: ['atom'] });
    const songbookRecords = await DynamicRegisters.loadRecords({ prefixes: ['songs/'] });

    lyricsEditorialRecords = songbookRecords.filter(item => {
      const t = (item.data || {}).type_unite;
      return t === 'song_lyrics_editorial' || t === 'song_editorial_apparatus';
    });

    canonicalSongs = extractCanonicalSongs(allSongs);
    buildAliasIndexes(canonicalSongs);

    const songMentions = allSongs.filter(item => !isCanonControlRecord(item));
    const atomMentions = atomRecords.filter(item => canonicalForRecord(item));
    rawSongRecords = [...songMentions, ...atomMentions];

    songGroups = groupSongRecords(canonicalSongs, rawSongRecords, lyricsEditorialRecords);
    songGroups.sort((a, b) => a.canonical.song.localeCompare(b.canonical.song, undefined, { numeric: true }));
    hydrateFilters(songGroups);
    render(songGroups);

    const linked = songGroups.reduce((acc, g) => acc + g.records.length, 0);
    const editorial = songGroups.reduce((acc, g) => acc + g.lyricsEditorial.length, 0);
    const orphan = rawSongRecords.filter(r => !canonicalForRecord(r)).length;
    statusCard.textContent = canonicalSongs.length + ' titre(s) canoniques Joy Division / Warsaw ; ' + linked + ' mention(s) atomisées rattachée(s) ; ' + editorial + ' fiche(s) éditoriale(s) lyrics ; ' + orphan + ' mention(s) exclue(s) ou hors canon.';
  } catch (err) {
    console.error(err);
    statusCard.textContent = 'Erreur de chargement dynamique du registre des chansons : ' + err.message;
  }
}

function isCanonControlRecord(item) {
  const d = item.data || {};
  return item.file === 'registers/songs/00_canonical_joy_division_songs.md' || d.type_unite === 'song_canon' || String(d.id || '').startsWith('JD-SONG-');
}

function extractCanonicalSongs(records) {
  return records
    .filter(item => item.file === 'registers/songs/00_canonical_joy_division_songs.md')
    .map(item => item.data || {})
    .filter(d => d.type_unite === 'song' && d.canonical_song === true && d.exclude !== true)
    .map(d => ({
      id: d.id,
      song: d.song,
      slug: d.slug,
      category: d.category || '',
      period: d.period || '',
      status: d.status || '',
      aliases: U([d.song, ...(d.aliases || [])]),
      albums: A(d.albums),
      variants: A(d.include_variants)
    }));
}

function buildAliasIndexes(canon) {
  aliasIndex = new Map();
  canon.forEach(song => song.aliases.forEach(alias => aliasIndex.set(norm(alias), song)));
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

function groupSongRecords(canon, records, editorialRecords) {
  return canon.map(song => {
    const linked = records.filter(record => canonicalForRecord(record)?.id === song.id);
    const lyricsEditorial = editorialRecords.filter(record => (record.data || {}).song_id === song.id);
    const editorialThemes = lyricsEditorial.flatMap(x => A((x.data || {}).motifs));
    const editorialChapters = lyricsEditorial.flatMap(x => chaptersOf(x.data || {}));
    return {
      canonical: song,
      records: linked,
      lyricsEditorial,
      sourceIds: U(linked.flatMap(sourceIds)),
      types: U([song.category, ...linked.flatMap(x => typesOf(x.data || {})), ...lyricsEditorial.flatMap(x => typesOf(x.data || {}))]),
      themes: U([...linked.flatMap(x => themesOf(x.data || {})), ...editorialThemes]),
      chapters: U([...linked.flatMap(x => chaptersOf(x.data || {})), ...editorialChapters])
    };
  });
}

function hydrateFilters(items) {
  fillSongFilter(songFilter, items);
  fill(sourceFilter, U(items.flatMap(x => x.sourceIds)), sourceLabel);
  fill(typeFilter, U(items.flatMap(x => x.types)));
  fill(themeFilter, U(items.flatMap(x => x.themes)).slice(0, 250));
  fill(chapterFilter, U(items.flatMap(x => x.chapters)));
}

function fillSongFilter(select, groups) {
  select.innerHTML = '<option value="">Toutes les chansons Joy Division / Warsaw</option>';
  const byCategory = new Map();
  groups.forEach(group => {
    const cat = group.canonical.category || 'Autres';
    if (!byCategory.has(cat)) byCategory.set(cat, []);
    byCategory.get(cat).push(group);
  });
  [...byCategory.entries()].forEach(([category, entries]) => {
    const optgroup = document.createElement('optgroup');
    optgroup.label = category;
    entries.forEach(group => {
      const opt = document.createElement('option');
      opt.value = group.canonical.id;
      opt.textContent = group.canonical.song;
      optgroup.appendChild(opt);
    });
    select.appendChild(optgroup);
  });
}

function fill(select, values, labeler = v => v) {
  select.innerHTML = '<option value="">Tous</option>';
  values.forEach(v => {
    const opt = document.createElement('option');
    opt.value = v;
    opt.textContent = labeler(v);
    select.appendChild(opt);
  });
}

function section(title, content) {
  if (!content || content === '<ul></ul>') return '';
  return '<div class="section-title">' + title + '</div>' + content;
}
function list(arr) {
  const values = A(arr).filter(Boolean);
  return values.length ? '<ul>' + values.map(x => '<li>' + T(x) + '</li>').join('') + '</ul>' : '';
}
function objectList(arr, fields) {
  const values = A(arr).filter(Boolean);
  if (!values.length) return '';
  return '<ul>' + values.map(item => {
    if (typeof item !== 'object') return '<li>' + T(item) + '</li>';
    const bits = fields.map(field => item[field] ? '<strong>' + field + ' :</strong> ' + T(item[field]) : '').filter(Boolean);
    return '<li>' + (bits.join(' — ') || T(JSON.stringify(item))) + '</li>';
  }).join('') + '</ul>';
}
function compactList(d) {
  return list(d.themes || d.motifs || d.related_motifs || d.concepts || d.keywords);
}
function renderLyricsEditorial(records) {
  return records.map(record => {
    const d = record.data || {};
    return '<div class="record-row editorial-row">'
      + '<div><strong>Appareil éditorial des paroles</strong> <span class="small">' + T(d.id || record.id) + '</span></div>'
      + (d.canonical_lyrics_source ? '<p><strong>Source :</strong> ' + T(d.canonical_lyrics_source) + (d.source_page ? ', ' + T(d.source_page) : '') + '</p>' : '')
      + section('Courts extraits citables', objectList(d.short_excerpts, ['excerpt','usage','source_page','verification_status']))
      + section('Variantes décrites', objectList(d.variants, ['variant_type','type','description','source','verification_status']))
      + section('Motifs', list(d.motifs))
      + section('Notes éditoriales', list(d.editorial_notes))
      + '<p class="small"><code>' + record.file + '</code></p>'
      + '</div>';
  }).join('');
}

function renderRecord(item) {
  const d = item.data || {};
  const ids = sourceIds(item);
  const label = item.kind === 'atom' ? 'Atome v2' : 'Mention';
  return '<div class="record-row">'
    + '<div><strong>' + label + ' — ' + T(rawSongTitle(d)) + '</strong> <span class="small">' + T(d.id || item.id) + '</span></div>'
    + '<div class="small">' + ids.map(sourceLabel).join(' ; ') + (d.type_unite ? ' ; ' + T(d.type_unite) : '') + (d.importance ? ' ; ' + T(d.importance) : '') + '</div>'
    + (d.usage ? '<p>' + T(d.usage) + '</p>' : '')
    + section('Thèmes / concepts', compactList(d))
    + section('Chapitres', list(chaptersOf(d)))
    + '<p class="small"><code>' + item.file + '</code></p>'
    + '</div>';
}

function render(items) {
  songsList.innerHTML = '';
  resultsMeta.textContent = items.length + ' titre(s) canonique(s)';
  items.forEach(group => {
    const song = group.canonical;
    const card = document.createElement('article');
    card.className = 'song-card canonical-card';
    const editorialBlocks = renderLyricsEditorial(group.lyricsEditorial);
    const recordBlocks = group.records.slice(0, 30).map(record => renderRecord(record)).join('');
    const more = group.records.length > 30 ? '<p class="small">+' + (group.records.length - 30) + ' autre(s) mention(s) masquée(s) dans cette vue.</p>' : '';
    card.innerHTML = '<h3>' + T(song.song) + '</h3>'
      + '<div class="meta">'
      + '<span class="badge canonical">canon</span>'
      + (song.period ? '<span class="badge">' + T(song.period) + '</span>' : '')
      + (song.status ? '<span class="badge">' + T(song.status) + '</span>' : '')
      + (group.records.length ? '<span class="badge">' + group.records.length + ' mention(s)</span>' : '<span class="badge muted">aucune mention atomisée</span>')
      + (group.lyricsEditorial.length ? '<span class="badge editorial">lyrics éditorial</span>' : '')
      + '</div>'
      + section('Catégorie', '<p>' + T(song.category) + '</p>')
      + section('Albums / corpus', list(song.albums))
      + section('Alias et variantes de titre', list(song.aliases.filter(x => x !== song.song)))
      + section('Types de variantes retenues', list(song.variants))
      + section('Sources liées', list(group.sourceIds.map(sourceLabel)))
      + section('Chapitres liés', list(group.chapters))
      + section('Thèmes / mots-clés issus des atomes et lyrics', list(group.themes.slice(0, 24)))
      + (editorialBlocks ? '<div class="section-title">Appareil éditorial des paroles</div><div class="record-list">' + editorialBlocks + '</div>' : '')
      + (recordBlocks ? '<div class="section-title">Mentions atomisées rattachées</div><div class="record-list">' + recordBlocks + more + '</div>' : '')
      + '<p class="small"><code>' + song.id + '</code></p>';
    songsList.appendChild(card);
  });
}

function applyFilters() {
  const q = searchInput.value.toLowerCase();
  const filtered = songGroups.filter(group => {
    const haystack = [group.canonical.song, group.canonical.category, group.canonical.period, group.canonical.status, group.canonical.aliases.join(' '), group.canonical.albums.join(' '), group.canonical.variants.join(' '), group.lyricsEditorial.map(r => JSON.stringify(r.data || {}) + ' ' + r.id + ' ' + r.file).join(' '), group.records.map(r => JSON.stringify(r.data || {}) + ' ' + r.id + ' ' + r.file).join(' '), group.sourceIds.join(' '), group.sourceIds.map(sourceLabel).join(' ')].join(' ').toLowerCase();
    return (!q || haystack.includes(q)) && (!songFilter.value || group.canonical.id === songFilter.value) && (!sourceFilter.value || group.sourceIds.includes(sourceFilter.value)) && (!typeFilter.value || group.types.includes(typeFilter.value)) && (!themeFilter.value || group.themes.includes(themeFilter.value)) && (!chapterFilter.value || group.chapters.includes(chapterFilter.value));
  });
  render(filtered);
}

function exportCSV() {
  const rows = songGroups.map(group => ({ song: group.canonical.song, category: group.canonical.category, period: group.canonical.period, status: group.canonical.status, aliases: group.canonical.aliases.join('; '), albums: group.canonical.albums.join('; '), variants: group.canonical.variants.join('; '), atomized_mentions: group.records.length, lyrics_editorial: group.lyricsEditorial.length, sources: group.sourceIds.map(sourceLabel).join('; '), chapters: group.chapters.join('; ') }));
  const header = Object.keys(rows[0] || {}).join(',');
  const body = rows.map(r => Object.values(r).map(v => '"' + String(v || '').replace(/"/g, '""') + '"').join(',')).join('\n');
  const blob = new Blob([header + '\n' + body], { type: 'text/csv;charset=utf-8;' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'joy_division_songs_canonical_register.csv';
  a.click();
  URL.revokeObjectURL(a.href);
}

[searchInput, songFilter, sourceFilter, typeFilter, themeFilter, chapterFilter].forEach(el => el.addEventListener('input', applyFilters));
resetButton.addEventListener('click', () => { searchInput.value=''; songFilter.value=''; sourceFilter.value=''; typeFilter.value=''; themeFilter.value=''; chapterFilter.value=''; render(songGroups); });
downloadButton.addEventListener('click', exportCSV);
loadSongs();
