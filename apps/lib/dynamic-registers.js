window.DynamicRegisters = (() => {
  const REPO = 'AdminQuest/joy-division-ai-writing-studio';
  const BRANCH = 'main';
  const TREE_URL = `https://api.github.com/repos/${REPO}/git/trees/${BRANCH}?recursive=1`;
  const RAW_BASE = `https://raw.githubusercontent.com/${REPO}/${BRANCH}/`;
  let treePromise = null;
  let registryPromise = null;
  let yamlPromise = null;

  function text(value) { return value === null || value === undefined ? '' : String(value); }
  function array(value) { return Array.isArray(value) ? value : (value ? [value] : []); }
  function uniq(values) { return [...new Set(values.map(text).filter(Boolean))].sort((a,b)=>a.localeCompare(b,undefined,{numeric:true})); }
  function normalizeSourceId(id) { return id === 'S-BROLL-JOY-001' ? 'S68' : text(id); }

  function loadScript(src) {
    return new Promise((resolve, reject) => {
      if ([...document.scripts].some(s => s.src === src)) return resolve();
      const s = document.createElement('script');
      s.src = src;
      s.onload = resolve;
      s.onerror = reject;
      document.head.appendChild(s);
    });
  }

  async function ensureYaml() {
    if (!yamlPromise) yamlPromise = loadScript('https://cdn.jsdelivr.net/npm/js-yaml@4/dist/js-yaml.min.js');
    await yamlPromise;
    return window.jsyaml;
  }

  async function loadTree() {
    if (!treePromise) {
      treePromise = fetch(TREE_URL, { cache: 'no-store' })
        .then(r => { if (!r.ok) throw new Error(`GitHub tree ${r.status}`); return r.json(); })
        .then(j => j.tree || []);
    }
    return treePromise;
  }

  async function loadRegistry() {
    if (!registryPromise) {
      registryPromise = fetch(`${RAW_BASE}data/registre.json`, { cache: 'no-store' })
        .then(r => r.ok ? r.json() : [])
        .catch(() => []);
    }
    return registryPromise;
  }

  async function sourceLabels() {
    const labels = {
      S41:'S41 — Hook, Unknown Pleasures, 2012',
      S45:'S45 — Curtis, Touching from a Distance, 1995',
      S46:'S46 — Johnson, An Ideal for Living, 1984',
      S47:'S47 — West, Joy Division, 1983',
      S68:'S68 — Broll, Joy Division, s.d.',
      S72:'S72 — Reynolds, Rip It Up and Start Again, 2005/2006'
    };
    const registry = await loadRegistry();
    registry.forEach(entry => {
      const id = normalizeSourceId(entry.id || entry.source_id);
      if (id) labels[id] = entry.source_label || labels[id] || id;
      const legacy = entry.legacy_id || entry.legacy_ids || [];
      array(legacy).forEach(alias => labels[alias] = labels[id] || id);
    });
    return labels;
  }

  function inferKind(data) {
    const id = text(data.id);
    if (id.startsWith('CHR-')) return 'chronology';
    if (id.startsWith('PERS-')) return 'person';
    if (id.startsWith('SONG-') || data.song || data.titre && /songs?\//.test(text(data.__file))) return 'song';
    if (id.startsWith('CONCEPT-')) return 'concept';
    if (id.includes('-Q')) return 'quote';
    if (id.startsWith('S') && id.includes('-')) return 'atom';
    return 'unknown';
  }

  function normalizeRecord(data, file, heading) {
    const d = { ...data, __file: file };
    if (d.source_id && !d.sources) d.sources = [normalizeSourceId(d.source_id)];
    if (Array.isArray(d.sources)) d.sources = d.sources.map(normalizeSourceId).filter(Boolean);
    if (d.evenement && !d.event) d.event = d.evenement;
    if (d.chapitres && !d.chapters) d.chapters = d.chapitres;
    if (!d.song && d.titre) d.song = String(d.titre).replace(/[«»*]/g, '').trim();
    if (!d.song && d.title) d.song = d.title;
    const id = text(d.id) || `NO_ID::${file}`;
    return { kind: inferKind(d), id, file, heading, data: d };
  }

  function nearestHeading(text, pos) {
    const before = text.slice(0, pos).split(/\r?\n/).reverse();
    const line = before.find(l => /^#{1,6}\s+/.test(l));
    return line ? line.replace(/^#{1,6}\s+/, '').trim() : '';
  }

  async function parseMarkdown(path, markdown) {
    const yaml = await ensureYaml();
    const out = [];
    const re = /```yaml\s*([\s\S]*?)\s*```/gi;
    let m;
    while ((m = re.exec(markdown))) {
      const heading = nearestHeading(markdown, m.index);
      let loaded;
      try { loaded = yaml.load(m[1]); } catch { continue; }
      if (!loaded || typeof loaded !== 'object' || Array.isArray(loaded)) continue;
      const containerKeys = ['chronology','people','persons','songs','citations','quotes','concepts','records'];
      const key = containerKeys.find(k => Array.isArray(loaded[k]));
      if (key) {
        loaded[key].forEach(item => {
          if (item && typeof item === 'object' && !Array.isArray(item)) out.push(normalizeRecord(item, path, heading));
        });
      } else {
        out.push(normalizeRecord(loaded, path, heading));
      }
    }
    return out;
  }

  async function listMarkdown(prefixes) {
    const tree = await loadTree();
    return tree
      .filter(x => x.type === 'blob' && x.path.endsWith('.md'))
      .map(x => x.path)
      .filter(path => prefixes.some(prefix => path.startsWith(prefix)));
  }

  async function loadRecords({ prefixes, kinds }) {
    const paths = await listMarkdown(prefixes);
    const chunks = await Promise.all(paths.map(async path => {
      const markdown = await fetch(`${RAW_BASE}${path}`, { cache: 'no-store' }).then(r => r.ok ? r.text() : '');
      return parseMarkdown(path, markdown);
    }));
    const records = chunks.flat();
    return kinds ? records.filter(r => kinds.includes(r.kind)) : records;
  }

  function sourceIds(item) {
    const d = item.data || item;
    return array(d.sources || d.source_id).map(normalizeSourceId).filter(Boolean);
  }

  return { loadRecords, sourceLabels, sourceIds, text, array, uniq };
})();
