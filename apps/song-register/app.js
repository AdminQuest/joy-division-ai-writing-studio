const songsList = document.getElementById('songs-list');
const resultsMeta = document.getElementById('results-meta');
const statusCard = document.getElementById('status-card');
const searchInput = document.getElementById('search');
const sourceFilter = document.getElementById('source-filter');
const typeFilter = document.getElementById('type-filter');
const themeFilter = document.getElementById('theme-filter');
const chapterFilter = document.getElementById('chapter-filter');
const resetButton = document.getElementById('reset-filters');
const downloadButton = document.getElementById('download-csv');

let songs = [];
let sourceLabels = {};

const T = v => DynamicRegisters.text(v);
const A = v => DynamicRegisters.array(v);
const U = v => DynamicRegisters.uniq(v);
const sourceIds = item => DynamicRegisters.sourceIds(item);
const sourceLabel = id => sourceLabels[id] || id || '';
const chaptersOf = d => A(d.chapters || d.chapitres);
const songTitle = d => d.song || d.titre || d.title || d.id || '';
const typesOf = d => A(d.type || d.type_unite);
const themesOf = d => A(d.themes || d.keywords || d.motifs || d.related_motifs);

async function loadSongs() {
  try {
    sourceLabels = await DynamicRegisters.sourceLabels();
    songs = await DynamicRegisters.loadRecords({ prefixes: ['registers/songs/', 'sources/'], kinds: ['song'] });
    songs.sort((a, b) => T(songTitle(a.data || {})).localeCompare(T(songTitle(b.data || {})), undefined, { numeric: true }));
    hydrateFilters(songs);
    render(songs);
    statusCard.textContent = songs.length + ' chanson(s) chargée(s) depuis les fichiers Markdown spécialisés';
  } catch (err) {
    console.error(err);
    statusCard.textContent = 'Erreur de chargement dynamique du registre des chansons : ' + err.message;
  }
}

function hydrateFilters(items) {
  fill(sourceFilter, U(items.flatMap(sourceIds)), sourceLabel);
  fill(typeFilter, U(items.flatMap(x => typesOf(x.data || {}))));
  fill(themeFilter, U(items.flatMap(x => themesOf(x.data || {}))));
  fill(chapterFilter, U(items.flatMap(x => chaptersOf(x.data || {}))));
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
  const values = A(arr);
  if (!values.length) return '';
  return '<ul>' + values.map(x => '<li>' + T(x) + '</li>').join('') + '</ul>';
}
function production(p) {
  if (!p) return '';
  const rows = [];
  if (p.producer) rows.push('<li><strong>Producteur :</strong> ' + A(p.producer).join(', ') + '</li>');
  if (p.label) rows.push('<li><strong>Label :</strong> ' + A(p.label).join(', ') + '</li>');
  if (p.sound_characteristics) rows.push('<li><strong>Son :</strong> ' + A(p.sound_characteristics).join(', ') + '</li>');
  if (p.studio) rows.push('<li><strong>Studio :</strong> ' + A(p.studio).join(', ') + '</li>');
  return rows.length ? '<ul>' + rows.join('') + '</ul>' : '';
}
function live(l) {
  if (!l) return '';
  const rows = [];
  if (l.important_performances) rows.push('<li><strong>Performances :</strong> ' + A(l.important_performances).join(', ') + '</li>');
  if (l.observations) rows.push('<li><strong>Observations :</strong> ' + A(l.observations).join(', ') + '</li>');
  return rows.length ? '<ul>' + rows.join('') + '</ul>' : '';
}
function lyrics(l) {
  if (!l) return '';
  const rows = [];
  if (l.notable_lines) rows.push('<li><strong>Lignes notables :</strong> ' + A(l.notable_lines).join(' / ') + '</li>');
  if (l.recurring_motifs) rows.push('<li><strong>Motifs :</strong> ' + A(l.recurring_motifs).join(', ') + '</li>');
  return rows.length ? '<ul>' + rows.join('') + '</ul>' : '';
}

function render(items) {
  songsList.innerHTML = '';
  resultsMeta.textContent = items.length + ' résultat(s)';
  items.forEach(item => {
    const d = item.data || {};
    const ids = sourceIds(item);
    const card = document.createElement('article');
    card.className = 'song-card';
    card.innerHTML = '<h3>' + T(songTitle(d)) + '</h3>'
      + '<div class="meta">' + typesOf(d).map(x => '<span class="badge">' + T(x) + '</span>').join('') + (d.period ? '<span class="badge">' + d.period + '</span>' : '') + (d.certainty ? '<span class="badge">certitude : ' + d.certainty + '</span>' : '') + '</div>'
      + section('Thèmes', list(d.themes || d.motifs || d.related_motifs))
      + section('Mots-clés', list(d.keywords || d.usage))
      + section('Auteurs', list(d.writers || d.associated_people))
      + section('Pistes / titres associés', list(d.tracks))
      + section('Production', production(d.production || d))
      + section('Historique live', live(d.live_history))
      + section('Paroles / motifs', lyrics(d.lyrics))
      + section('Sources', list(ids.map(sourceLabel)))
      + section('Atomes liés', list(d.related_atoms || d.atomes_lies))
      + section('Citations liées', list(d.related_quotes || d.citations_liees))
      + section('Chapitres', list(chaptersOf(d)))
      + section('Contradictions', list(d.contradictions))
      + (d.notes || d.resume ? '<div class="section-title">Notes</div><p>' + T(d.notes || d.resume) + '</p>' : '')
      + '<p class="small"><code>' + item.file + '</code></p>';
    songsList.appendChild(card);
  });
}

function applyFilters() {
  const q = searchInput.value.toLowerCase();
  const filtered = songs.filter(item => {
    const d = item.data || {};
    const ids = sourceIds(item);
    const haystack = [JSON.stringify(d), item.id, item.file, ...ids, ...ids.map(sourceLabel)].join(' ').toLowerCase();
    return (!q || haystack.includes(q))
      && (!sourceFilter.value || ids.includes(sourceFilter.value))
      && (!typeFilter.value || typesOf(d).includes(typeFilter.value))
      && (!themeFilter.value || themesOf(d).includes(themeFilter.value))
      && (!chapterFilter.value || chaptersOf(d).includes(chapterFilter.value));
  });
  render(filtered);
}

function exportCSV() {
  const rows = songs.map(s => {
    const d = s.data || {};
    return {
      song: songTitle(d),
      period: d.period || '',
      types: typesOf(d).join('; '),
      themes: themesOf(d).join('; '),
      sources: sourceIds(s).map(sourceLabel).join('; '),
      chapters: chaptersOf(d).join('; '),
      file: s.file
    };
  });
  const header = Object.keys(rows[0] || {}).join(',');
  const body = rows.map(r => Object.values(r).map(v => '"' + String(v || '').replace(/"/g, '""') + '"').join(',')).join('\n');
  const blob = new Blob([header + '\n' + body], { type: 'text/csv;charset=utf-8;' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'joy_division_songs_register_dynamic.csv';
  a.click();
  URL.revokeObjectURL(a.href);
}

[searchInput, sourceFilter, typeFilter, themeFilter, chapterFilter].forEach(el => el.addEventListener('input', applyFilters));
resetButton.addEventListener('click', () => { searchInput.value=''; sourceFilter.value=''; typeFilter.value=''; themeFilter.value=''; chapterFilter.value=''; render(songs); });
downloadButton.addEventListener('click', exportCSV);
loadSongs();
