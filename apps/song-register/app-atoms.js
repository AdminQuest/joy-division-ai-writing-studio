(() => {
  const T = value => DynamicRegisters.text(value);
  const A = value => DynamicRegisters.array(value);
  const U = value => DynamicRegisters.uniq(value);
  let atomsBySongId = new Map();
  let atomsReady = false;

  function conceptsOf(data) {
    return U([...(A(data.concepts)), ...(A(data.motifs)), ...(A(data.keywords))]);
  }

  function chaptersOf(data) {
    return U([...(A(data.chapters)), ...(A(data.chapitres))]);
  }

  function renderAtom(atom) {
    const d = atom.data || {};
    const concepts = conceptsOf(d);
    const chapters = chaptersOf(d);
    return '<div class="record-row atom-row">'
      + '<div><strong>' + T(atom.heading || d.canonical_song || d.id) + '</strong> <span class="small">' + T(d.id || atom.id) + '</span></div>'
      + '<div class="small">' + T(d.source_id || '') + (d.type_unite ? ' ; ' + T(d.type_unite) : '') + (d.importance ? ' ; ' + T(d.importance) : '') + '</div>'
      + (concepts.length ? '<div class="section-title">Concepts / motifs</div><ul>' + concepts.map(x => '<li>' + T(x) + '</li>').join('') + '</ul>' : '')
      + (chapters.length ? '<div class="section-title">Chapitres</div><ul>' + chapters.map(x => '<li>' + T(x) + '</li>').join('') + '</ul>' : '')
      + '<p class="small"><code>' + atom.file + '</code></p>'
      + '</div>';
  }

  function songIdFromCard(card) {
    const codes = [...card.querySelectorAll('code')].map(x => x.textContent.trim());
    return codes.find(x => /^JD-SONG-\d+/.test(x)) || '';
  }

  function injectAtoms() {
    if (!atomsReady) return;
    document.querySelectorAll('.atoms-v2-block').forEach(x => x.remove());
    document.querySelectorAll('.song-card').forEach(card => {
      const songId = songIdFromCard(card);
      const atoms = atomsBySongId.get(songId) || [];
      if (!atoms.length) return;
      const meta = card.querySelector('.meta');
      const mutedBadge = [...card.querySelectorAll('.badge')].find(x => x.textContent.includes('aucune mention atomisée'));
      if (mutedBadge) mutedBadge.textContent = atoms.length + ' atome(s) v2';
      else if (meta && ![...meta.querySelectorAll('.badge')].some(x => x.textContent.includes('atome(s) v2'))) {
        const badge = document.createElement('span');
        badge.className = 'badge editorial';
        badge.textContent = atoms.length + ' atome(s) v2';
        meta.appendChild(badge);
      }
      const block = document.createElement('div');
      block.className = 'atoms-v2-block';
      block.innerHTML = '<div class="section-title">Atomes v2 rattachés</div><div class="record-list">'
        + atoms.slice(0, 20).map(renderAtom).join('')
        + (atoms.length > 20 ? '<p class="small">+' + (atoms.length - 20) + ' autre(s) atome(s) masqué(s) dans cette vue.</p>' : '')
        + '</div>';
      const endCode = [...card.querySelectorAll('p.small')].pop();
      card.insertBefore(block, endCode || null);
    });
  }

  async function loadAtomRecords() {
    const atoms = await DynamicRegisters.loadRecords({ prefixes: ['sources/'], kinds: ['atom'] });
    const withSong = atoms.filter(atom => (atom.data || {}).song_id);
    atomsBySongId = new Map();
    withSong.forEach(atom => {
      const songId = atom.data.song_id;
      if (!atomsBySongId.has(songId)) atomsBySongId.set(songId, []);
      atomsBySongId.get(songId).push(atom);
    });
    atomsBySongId.forEach(list => list.sort((a, b) => T(a.id).localeCompare(T(b.id), undefined, { numeric: true })));
    atomsReady = true;
    injectAtoms();
  }

  const target = document.getElementById('songs-list') || document.body;
  new MutationObserver(() => injectAtoms()).observe(target, { childList: true, subtree: true });
  loadAtomRecords().catch(err => console.error('Atomes v2 song-register:', err));
})();
