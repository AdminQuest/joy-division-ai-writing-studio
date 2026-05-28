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
      S20:'S20 — Dodge, Mapping Manchester’s housing problems, Manchester Geographies, s.d.',
      S41:'S41 — Hook, Unknown Pleasures, 2012',
      S45:'S45 — Curtis, Touching from a Distance, 1995',
      S46:'S46 — Johnson, An Ideal for Living, 1984',
      S47:'S47 — West, Joy Division, 1983',
      S68:'S68 — Broll, Joy Division, s.d.',
      S72:'S72 — Reynolds, Rip It Up and Start Again, 2005/2006',
      S75:'S75 — Ott, Joy Division’s Unknown Pleasures, 2004'
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
    const file = text(data.__file);
    if (id.startsWith('CHR-')) return 'chronology';
    if (id.startsWith('ACT-') || id.startsWith('PERS-') || id.startsWith('PERSONNE-') || /people\//.test(file)) return 'person';
    if (id.startsWith('PLACE-') || /places\//.test(file)) return 'place';
    if (id.startsWith('ORG-') || /organizations\//.test(file)) return 'organization';
    if (id.startsWith('SONG-') || id.startsWith('ALBUM-') || data.song || data.titre && /songs?\//.test(file)) return 'song';
    if (id.startsWith('CONCEPT-')) return 'concept';
    if (id.startsWith('MOTIF-')) return 'motif';
    if (id.startsWith('MYTH-') || id.startsWith('MYTHE-')) return 'myth';
    if (id.startsWith('REF-') || id.startsWith('REG-') || id.startsWith('REL-RAG-')) return 'reference';
    if (id.startsWith('CIT-') || id.includes('-Q')) return 'quote';
    if (id.startsWith('S') && id.includes('-')) return 'atom';
    return 'unknown';
  }

  function normalizeRecord(data, file, heading) {
    const d = { ...data, __file: file };
    if (d.source_id && !d.sources) d.sources = [normalizeSourceId(d.source_id)];
    // Also handle source_ids (plural) used in S80/S81 structuring registers
    if (d.source_ids && !d.sources) d.sources = array(d.source_ids).map(normalizeSourceId).filter(Boolean);
    if (Array.isArray(d.sources)) d.sources = d.sources.map(normalizeSourceId).filter(Boolean);
    if (d.evenement && !d.event) d.event = d.evenement;
    if (d.chapitres && !d.chapters) d.chapters = d.chapitres;
    if (!d.song && d.titre && /songs?\//.test(file)) d.song = String(d.titre).replace(/[«»*]/g, '').trim();
    if (!d.song && d.title && /songs?\//.test(file)) d.song = d.title;
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
    // Track document-level source_id from header blocks so it can be
    // inherited by sub-records (e.g. CONCEPT-* / MOTIF-* blocks in
    // sXX_*_structuring_registers.md) that don't carry their own source_id.
    // This is generic: any file whose first YAML block has source_id but no id
    // field is treated as a document header; all subsequent records without an
    // explicit source reference inherit that source_id automatically.
    let contextSourceId = null;
    const re = /```yaml\s*([\s\S]*?)\s*```/gi;
    let m;
    while ((m = re.exec(markdown))) {
      const heading = nearestHeading(markdown, m.index);
      let loaded;
      try { loaded = yaml.load(m[1]); } catch { continue; }
      if (!loaded || typeof loaded !== 'object' || Array.isArray(loaded)) continue;
      // Document header: has source_id but no record id → capture context, don't emit
      if (loaded.source_id && !loaded.id) {
        contextSourceId = text(loaded.source_id);
        continue;
      }
      const containerKeys = ['chronology','events','people','persons','places','organizations','organisations','orgs','songs','citations','quotes','concepts','motifs','mythes','myths','records'];
      const key = containerKeys.find(k => Array.isArray(loaded[k]));
      if (key) {
        loaded[key].forEach(item => {
          if (item && typeof item === 'object' && !Array.isArray(item)) {
            // Inherit document source_id when the item has no own source reference
            if (contextSourceId && !item.source_id && !item.source_ids && !item.sources) {
              item = { ...item, source_id: contextSourceId };
            }
            out.push(normalizeRecord(item, path, heading));
          }
        });
      } else {
        // Inherit document source_id when the record has no own source reference
        let record = loaded;
        if (contextSourceId && record.id && !record.source_id && !record.source_ids && !record.sources) {
          record = { ...record, source_id: contextSourceId };
        }
        out.push(normalizeRecord(record, path, heading));
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
    const records = chunks.flat()
      // Drop document-header parasites: a place-kind record carrying a
      // type_unite other than "place" (e.g. type_unite: registre_lieux) is
      // register metadata, not an actual place. Scoped to kind 'place' so
      // other registers that use type_unite legitimately (song dossiers,
      // person/chronology/concept records, etc.) are left untouched.
      .filter(r => !(r.kind === 'place' && r.data && r.data.type_unite && r.data.type_unite !== 'place'));
    return kinds ? records.filter(r => kinds.includes(r.kind)) : records;
  }

  function sourceIds(item) {
    const d = item.data || item;
    return array(d.sources || d.source_id).map(normalizeSourceId).filter(Boolean);
  }

  return { loadRecords, sourceLabels, sourceIds, text, array, uniq };
})();