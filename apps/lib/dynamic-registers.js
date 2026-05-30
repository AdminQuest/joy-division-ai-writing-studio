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

  function recordLabel(d) { return text(d.label || d.nom || d.name || d.id); }
  function recordOrigin(rec) {
    const s = array(rec.data.sources)[0] || rec.data.source_id || '';
    return text(s).split('-')[0];
  }
  // Merge several records that share the same id into one consolidated entry:
  // longest label, unioned sources/chapters/atoms/song_ids, usage concatenated
  // with its source of origin ("Selon S02 : … | Selon S05 : …"), distinct
  // prudences joined. Scalars fall back to the first record; a divergent
  // canonical type is reported via console.warn.
  function mergeGroup(group) {
    const data = { ...group[0].data };
    data.label = group.map(r => recordLabel(r.data)).reduce((a, b) => b.length > a.length ? b : a, '');

    const types = uniq(group.map(r => text(r.data.type)).filter(Boolean));
    if (types.length > 1) console.warn(`[places] type conflict for ${group[0].id}: ${types.join(' / ')} — keeping "${types[0]}"`);

    data.sources = uniq(group.flatMap(r => sourceIds(r)));
    const chapters = uniq(group.flatMap(r => array(r.data.chapters || r.data.chapitres)));
    if (chapters.length) { data.chapters = chapters; delete data.chapitres; }
    const atoms = uniq(group.flatMap(r => array(r.data.atoms)));
    if (atoms.length) data.atoms = atoms;
    const songIds = uniq(group.flatMap(r => array(r.data.song_ids)));
    if (songIds.length) data.song_ids = songIds;

    const usages = [];
    group.forEach(r => {
      const u = text(r.data.usage || Object.keys(r.data).filter(k => k.startsWith('usage_')).map(k => r.data[k]).find(Boolean) || '').trim();
      if (u) usages.push({ origin: recordOrigin(r), usage: u });
    });
    const distinctUsages = uniq(usages.map(x => x.usage));
    if (distinctUsages.length === 1) data.usage = distinctUsages[0];
    else if (distinctUsages.length > 1) data.usage = usages.map(x => `Selon ${x.origin} : ${x.usage}`).join(' | ');

    const prudences = uniq(group.flatMap(r => array(r.data.prudence || r.data.methodological_warnings)));
    if (prudences.length) data.prudence = prudences.join(' | ');

    // Géo (étape 12b-1.c) : coordonnées portées par le lieu CANONIQUE. group[0]
    // est le représentant (point fixe same_as), mais on coalesce défensivement
    // la première valeur définie de la composante pour les fusions par id pur.
    ['lat', 'lng', 'geo_precision'].forEach(k => {
      const v = group.map(r => r.data[k]).find(x => x !== undefined && x !== null && x !== '');
      if (v !== undefined) data[k] = v;
    });
    const refs = uniq(group.flatMap(r => array(r.data.reference_croisee)));
    if (refs.length) data.reference_croisee = refs;
    const pm = uniq(group.flatMap(r => array(r.data.prudence_methodologique)));
    if (pm.length) data.prudence_methodologique = pm.join(' | ');

    // L'identifiant fusionné est toujours celui du représentant canonique.
    return { ...group[0], id: group[0].id, data: { ...data, id: group[0].id } };
  }

  // Résout le représentant canonique (point fixe) de chaque identifiant via la
  // clôture transitive des arêtes same_as. same_as est porté par les
  // enregistrements legacy et pointe vers le canonique ; le canonique n'en
  // porte pas (il est son propre représentant). Robuste aux cibles absentes et
  // aux cycles éventuels (s'arrête au premier nœud déjà visité).
  function sameAsTargets(rec) {
    const v = rec.data && rec.data.same_as;
    return v == null ? [] : array(v).map(text).filter(Boolean);
  }
  function buildCanonicalMap(places) {
    const edge = new Map();             // id -> cible canonique directe
    const known = new Set(places.map(r => r.id));
    places.forEach(r => {
      const t = sameAsTargets(r)[0];
      if (t && known.has(t)) edge.set(r.id, t);
    });
    const repOf = id => {
      const seen = new Set();
      let cur = id;
      while (edge.has(cur) && !seen.has(cur)) { seen.add(cur); cur = edge.get(cur); }
      return cur;
    };
    const rep = new Map();
    known.forEach(id => rep.set(id, repOf(id)));
    return rep;
  }
  // Deduplicate place records by id. Scoped to kind 'place' only: records of
  // other registers (which may carry their own legitimate duplicate ids) are
  // passed through untouched, preserving their current behaviour.
  function dedupeById(records) {
    const others = records.filter(r => r.kind !== 'place');
    const places = records.filter(r => r.kind === 'place');
    // Réconciliation same_as (étape 12b-1.c) : chaque enregistrement est
    // rattaché à son représentant canonique avant le groupage, de sorte que des
    // identifiants distincts décrivant le même lieu physique (ex. PLACE-S83-001
    // & PLACE-S41-… -> PLACE-TJ-DAVIDSONS) fusionnent en une seule entrée.
    const rep = buildCanonicalMap(places);
    const groups = new Map(); const order = [];
    places.forEach(r => {
      const key = rep.get(r.id) || r.id;
      if (!groups.has(key)) { groups.set(key, []); order.push(key); }
      // Le représentant canonique d'abord : il pilote id/label/type/géo.
      if (key === r.id) groups.get(key).unshift(r); else groups.get(key).push(r);
    });
    const merged = order.map(id => { const g = groups.get(id); return g.length === 1 ? g[0] : mergeGroup(g); });
    return others.concat(merged);
  }

  async function loadRecords({ prefixes, kinds }) {
    const paths = await listMarkdown(prefixes);
    const chunks = await Promise.all(paths.map(async path => {
      const markdown = await fetch(`${RAW_BASE}${path}`, { cache: 'no-store' }).then(r => r.ok ? r.text() : '');
      return parseMarkdown(path, markdown);
    }));
    const filtered = kinds ? chunks.flat().filter(r => kinds.includes(r.kind)) : chunks.flat();
    // The remaining normalization (header-parasite drop + same-id dedup/merge,
    // incl. the [places] console.warn in mergeGroup) is place-register-specific.
    // Scope it to calls that actually surface place records: other registers
    // (songs, atoms, people, …) return untouched here, so the song register no
    // longer triggers a needless merge pass nor risks places-only warnings.
    if (!filtered.some(r => r.kind === 'place')) return filtered;
    // Drop document-header parasites: a place-kind record carrying a type_unite
    // other than "place" (e.g. type_unite: registre_lieux) is register metadata,
    // not an actual place. Then consolidate records sharing the same id (e.g.
    // PLACE-HULME documented by S02, S06 and S20).
    return dedupeById(filtered.filter(r => !(r.kind === 'place' && r.data && r.data.type_unite && r.data.type_unite !== 'place')));
  }

  function sourceIds(item) {
    const d = item.data || item;
    return array(d.sources || d.source_id).map(normalizeSourceId).filter(Boolean);
  }

  return { loadRecords, sourceLabels, sourceIds, text, array, uniq };
})();