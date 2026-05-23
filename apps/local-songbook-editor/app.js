const state = {
  songs: [],
  current: null,
};

const el = id => document.getElementById(id);

async function api(path, options={}) {
  const res = await fetch(path, options);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

function linesToArray(text) {
  return text.split('\n').map(x => x.trim()).filter(Boolean);
}

function blockToObjects(text, type) {
  return text.trim()
    ? [{ type, description: text.trim(), verification_status: 'to_check' }]
    : [];
}

function excerptsFromText(text) {
  return linesToArray(text).map(line => ({ excerpt: line, usage: 'court extrait cité ou marqueur lyrique', verification_status: 'to_check' }));
}

function objectsToBlock(items) {
  if (!items || !items.length) return '';
  return items.map(item => {
    if (typeof item === 'string') return item;
    return item.description || item.text || item.excerpt || JSON.stringify(item);
  }).join('\n');
}

function safeJson(text, fallback=[]) {
  const trimmed = text.trim();
  if (!trimmed) return fallback;
  try { return JSON.parse(trimmed); }
  catch { return fallback; }
}

async function loadConfig() {
  const cfg = await api('/api/config');
  el('config').textContent = 'Workspace privé : ' + cfg.private_root;
}

async function loadSongs() {
  const data = await api('/api/songs');
  state.songs = data.songs;
  renderSongs();
}

function renderSongs() {
  const q = el('search').value.toLowerCase();
  const root = el('songs');
  root.innerHTML = '';

  state.songs
    .filter(song => !q || song.canonical_song.toLowerCase().includes(q) || song.slug.toLowerCase().includes(q))
    .forEach(song => {
      const div = document.createElement('div');
      div.className = 'song-item' + (state.current?.slug === song.slug ? ' active' : '');
      div.innerHTML = `
        <strong>${song.canonical_song}</strong>
        <div class="meta">${song.song_id || ''}</div>
        <div class="meta">lyrics: ${song.has_full_lyrics ? 'oui' : 'non'}</div>
        <div class="meta">web sources: ${song.has_web_sources ? 'oui' : 'non'}</div>
      `;
      div.onclick = () => openSong(song.slug);
      root.appendChild(div);
    });
}

async function openSong(slug) {
  const payload = await api('/api/song?slug=' + encodeURIComponent(slug));
  state.current = payload;
  const notes = payload.notes || {};

  el('lyrics').value = payload.full_lyrics || '';
  el('source').value = notes.canonical_lyrics_source || '';
  el('page').value = notes.source_page || '';
  el('motifs').value = (notes.motifs || []).join('\n');
  el('notes').value = (notes.editorial_notes || []).join('\n');
  el('chapters').value = (notes.chapters || []).join('\n');
  el('ragnotes').value = (notes.rag_notes || []).join('\n');
  el('quotes_text').value = objectsToBlock(notes.short_excerpts || []);
  el('variants_text').value = objectsToBlock(notes.variants || []);
  el('sessions_text').value = objectsToBlock(notes.sessions || []);
  el('releases_text').value = objectsToBlock(notes.releases || []);
  el('bootlegs_text').value = objectsToBlock(notes.bootlegs || []);
  el('web_source_links').value = (notes.web_source_links || []).join('\n');
  el('websources').value = JSON.stringify(payload.web_sources || [], null, 2);

  renderSongs();
}

async function saveCurrent() {
  if (!state.current) return;

  const notes = {
    ...(state.current.notes || {}),
    canonical_lyrics_source: el('source').value,
    source_page: el('page').value,
    motifs: linesToArray(el('motifs').value),
    editorial_notes: linesToArray(el('notes').value),
    chapters: linesToArray(el('chapters').value),
    rag_notes: linesToArray(el('ragnotes').value),
    web_source_links: linesToArray(el('web_source_links').value),
    short_excerpts: excerptsFromText(el('quotes_text').value),
    variants: blockToObjects(el('variants_text').value, 'lyrics_variants'),
    sessions: blockToObjects(el('sessions_text').value, 'sessions_versions'),
    releases: blockToObjects(el('releases_text').value, 'releases'),
    bootlegs: blockToObjects(el('bootlegs_text').value, 'bootlegs_live_covers'),
  };

  const payload = {
    full_lyrics: el('lyrics').value,
    notes,
    web_sources: safeJson(el('websources').value, []),
  };

  await api('/api/song?slug=' + encodeURIComponent(state.current.slug), {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload)
  });

  el('status').textContent = 'Enregistré.';
  setTimeout(() => el('status').textContent = '', 2500);

  await loadSongs();
  await openSong(state.current.slug);
}

async function syncRepo() {
  el('status').textContent = 'Extraction en cours…';
  const result = await api('/api/sync', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ skip_build: true })
  });

  if (result.ok) {
    el('status').textContent = 'Extraction terminée.';
  } else {
    el('status').textContent = 'Erreur extraction.';
    console.error(result.stderr);
  }
}

el('search').addEventListener('input', renderSongs);
el('refresh').addEventListener('click', loadSongs);
el('save').addEventListener('click', saveCurrent);
el('sync').addEventListener('click', syncRepo);

(async () => {
  await loadConfig();
  await loadSongs();
  const params = new URLSearchParams(window.location.search);
  const slug = params.get('slug');
  if (slug) await openSong(slug);
})();
