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

function parseJsonField(text, fallback=[]) {
  const trimmed = text.trim();
  if (!trimmed) return fallback;
  try {
    return JSON.parse(trimmed);
  } catch (err) {
    alert('JSON invalide : ' + err.message);
    throw err;
  }
}

function uniq(items) {
  const out = [];
  for (const item of items || []) {
    if (item === undefined || item === null || item === '') continue;
    const key = typeof item === 'string' ? item : JSON.stringify(item);
    if (!out.some(x => (typeof x === 'string' ? x : JSON.stringify(x)) === key)) out.push(item);
  }
  return out;
}

function sourceProjection(webSources) {
  const sessions = [];
  const releases = [];
  const bootlegs = [];
  const variants = [];
  const ragNotes = [];
  const motifs = [];

  for (const source of webSources || []) {
    const f = source.extracted_fields || {};
    const sourceRef = source.source_name || source.url || 'source web';

    for (const item of f.versions || []) sessions.push({ source: sourceRef, description: item, verification_status: source.verification_status || 'to_check' });
    for (const item of f.releases || []) releases.push({ source: sourceRef, description: item, verification_status: source.verification_status || 'to_check' });
    for (const item of f.bootlegs || []) bootlegs.push({ source: sourceRef, type: 'bootleg', description: item, verification_status: source.verification_status || 'to_check' });
    for (const item of f.live_occurrences || []) bootlegs.push({ source: sourceRef, type: 'live_occurrence', description: item, verification_status: source.verification_status || 'to_check' });
    for (const item of f.aliases || []) variants.push({ source: sourceRef, variant_type: 'alias', description: item, verification_status: source.verification_status || 'to_check' });

    if ((f.versions || []).length) motifs.push('versions documentées');
    if ((f.releases || []).length) motifs.push('discographie');
    if ((f.live_occurrences || []).length) motifs.push('occurrences live');
    if ((f.bootlegs || []).length) motifs.push('bootlegs');

    if (source.url) ragNotes.push(`Source web à vérifier : ${source.source_name || 'source web'} — ${source.url}`);
    if ((f.notes || []).length) ragNotes.push(...f.notes.slice(0, 10));
  }

  return {
    sessions: uniq(sessions),
    releases: uniq(releases),
    bootlegs: uniq(bootlegs),
    variants: uniq(variants),
    ragNotes: uniq(ragNotes),
    motifs: uniq(motifs),
  };
}

function mergeIfEmpty(current, projected) {
  return (current && current.length) ? current : projected;
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
  const webSources = payload.web_sources || [];
  const projected = sourceProjection(webSources);

  const motifs = mergeIfEmpty(notes.motifs || [], projected.motifs);
  const variants = mergeIfEmpty(notes.variants || [], projected.variants);
  const sessions = mergeIfEmpty(notes.sessions || [], projected.sessions);
  const releases = mergeIfEmpty(notes.releases || [], projected.releases);
  const bootlegs = mergeIfEmpty(notes.bootlegs || [], projected.bootlegs);
  const ragNotes = mergeIfEmpty(notes.rag_notes || [], projected.ragNotes);

  el('lyrics').value = payload.full_lyrics || '';
  el('source').value = notes.canonical_lyrics_source || '';
  el('page').value = notes.source_page || '';
  el('motifs').value = motifs.join('\n');
  el('notes').value = (notes.editorial_notes || []).join('\n');
  el('chapters').value = (notes.chapters || []).join('\n');
  el('quotes').value = JSON.stringify(notes.short_excerpts || [], null, 2);
  el('variants').value = JSON.stringify(variants, null, 2);
  el('sessions').value = JSON.stringify(sessions, null, 2);
  el('releases').value = JSON.stringify(releases, null, 2);
  el('bootlegs').value = JSON.stringify(bootlegs, null, 2);
  el('ragnotes').value = ragNotes.join('\n');
  el('websources').value = JSON.stringify(webSources, null, 2);

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
    short_excerpts: parseJsonField(el('quotes').value, []),
    variants: parseJsonField(el('variants').value, []),
    sessions: parseJsonField(el('sessions').value, []),
    releases: parseJsonField(el('releases').value, []),
    bootlegs: parseJsonField(el('bootlegs').value, []),
  };

  const payload = {
    full_lyrics: el('lyrics').value,
    notes,
    web_sources: parseJsonField(el('websources').value, []),
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
