(() => {
  const LOCAL_EDITOR_BASE = 'https://adminquest.github.io/joy-division-studio-private/apps/local-songbook-editor/';

  function slugifySongTitle(title) {
    return String(title || '')
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/[’‘]/g, '')
      .replace(/&/g, 'and')
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '');
  }

  const overrides = {
    "she's lost control": 'shes-lost-control',
    "you're no good for me": 'youre-no-good-for-me',
    "from safety to where...?": 'from-safety-to-where',
    "from safety to where": 'from-safety-to-where',
    "at a later date": 'at-a-later-date',
    "a means to an end": 'a-means-to-an-end',
    "in a lonely place": 'in-a-lonely-place',
    "love will tear us apart": 'love-will-tear-us-apart',
    "no love lost": 'no-love-lost',
    "new dawn fades": 'new-dawn-fades',
    "day of the lords": 'day-of-the-lords',
    "the eternal": 'the-eternal',
    "the drawback": 'the-drawback',
    "walked in line": 'walked-in-line',
    "leaders of men": 'leaders-of-men',
    "atrocity exhibition": 'atrocity-exhibition',
    "the only mistake": 'the-only-mistake',
    "something must break": 'something-must-break',
    "these days": 'these-days',
    "novelty": 'novelty',
    "warsaw": 'warsaw'
  };

  function slugFor(title) {
    const key = String(title || '').trim().toLowerCase();
    return overrides[key] || slugifySongTitle(title);
  }

  function addLinks() {
    document.querySelectorAll('.song-card').forEach(card => {
      if (card.querySelector('.local-editor-link')) return;
      const h3 = card.querySelector('h3');
      const meta = card.querySelector('.meta');
      if (!h3 || !meta) return;
      const slug = slugFor(h3.textContent);
      const a = document.createElement('a');
      a.className = 'badge editorial local-editor-link';
      a.href = LOCAL_EDITOR_BASE + '?slug=' + encodeURIComponent(slug);
      a.target = '_blank';
      a.rel = 'noopener noreferrer';
      a.textContent = 'ouvrir éditeur';
      a.title = 'Éditeur de Songbook — GitHub Pages (token requis).';
      meta.appendChild(a);
    });
  }

  const observer = new MutationObserver(addLinks);
  observer.observe(document.body, { childList: true, subtree: true });
  addLinks();
})();