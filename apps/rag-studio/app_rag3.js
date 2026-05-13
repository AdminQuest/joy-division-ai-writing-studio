// RAG 3 — regroupement documentaire des résultats RAG 2
// Ce module ne remplace pas RAG 2. Il ajoute une vue de synthèse classée
// par rôle documentaire : faits, scènes, lectures, mythes, controverses,
// citations, concepts, motifs et vigilance.

(function () {
  const GROUPS = [
    {id: 'facts', title: 'Faits établis', hint: 'Éléments factuels, datés ou directement exploitables.'},
    {id: 'scenes', title: 'Scènes fondatrices', hint: 'Épisodes narratifs structurants.'},
    {id: 'readings', title: 'Lectures / interprétations', hint: 'Analyses, hypothèses, interprétations critiques.'},
    {id: 'myths', title: 'Mythes à déconstruire', hint: 'Récits de fondation, légendes, simplifications historiographiques.'},
    {id: 'controversies', title: 'Controverses', hint: 'Points litigieux, attributions, débats ou objets sensibles.'},
    {id: 'quotes', title: 'Citations', hint: 'Citations utilisables avec contrôle préalable du statut.'},
    {id: 'concepts', title: 'Concepts / motifs', hint: 'Objets conceptuels, motifs récurrents ou chaînes interprétatives.'},
    {id: 'vigilance', title: 'Points de vigilance', hint: 'Risques de surinterprétation, preuves faibles, prudences.'},
    {id: 'other', title: 'Autres résultats', hint: 'Résultats utiles non classés automatiquement.'}
  ];

  function $(id) {
    return document.getElementById(id);
  }

  function normalize(value) {
    return String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  }

  function stringify(value) {
    if (value === undefined || value === null) return '';
    if (typeof value === 'string') return value;
    try { return JSON.stringify(value, null, 2); } catch (_) { return String(value); }
  }

  function fieldsOf(result) {
    return result?.record?.summary_fields || {};
  }

  function titleOf(result) {
    const record = result.record || {};
    const fields = fieldsOf(result);
    return record.id || fields.titre || record.heading || '(sans id)';
  }

  function sourceOf(result) {
    const fields = fieldsOf(result);
    return fields.source_label || fields.source_id || '';
  }

  function typeOf(result) {
    return stringify(fieldsOf(result).type_unite || '').trim();
  }

  function importanceOf(result) {
    return stringify(fieldsOf(result).importance || '').trim();
  }

  function proofOf(result) {
    return stringify(fieldsOf(result).niveau_preuve || fieldsOf(result).certainty || '').trim();
  }

  function fullText(result) {
    const record = result.record || {};
    const fields = fieldsOf(result);
    return normalize([
      record.id,
      record.kind,
      record.heading,
      record.file,
      fields.titre,
      fields.type_unite,
      fields.importance,
      fields.niveau_preuve,
      fields.concepts,
      fields.motifs,
      fields.citation_originale,
      fields.traduction_editoriale_fr,
      fields.event,
      fields.score_details
    ].map(stringify).join('\n'));
  }

  function hasAny(text, words) {
    return words.some(word => text.includes(word));
  }

  function classify(result) {
    const record = result.record || {};
    const fields = fieldsOf(result);
    const kind = record.kind || '';
    const type = normalize(fields.type_unite || '');
    const text = fullText(result);

    if (kind === 'quote' || fields.citation_originale || fields.traduction_editoriale_fr) return 'quotes';
    if (kind === 'concept' || kind === 'motif' || fields.concepts || fields.motifs) return 'concepts';
    if (kind === 'myth' || type.includes('mythe') || hasAny(text, ['mythe', 'myth', 'legende', 'legend', 'demystification', 'deconstruction'])) return 'myths';
    if (hasAny(type, ['controverse', 'litige']) || hasAny(text, ['controverse', 'controvers', 'litigieux', 'sensible', 'attribution', 'erreur', 'risque'])) return 'controversies';
    if (hasAny(text, ['risque_surinterpretation', 'surinterpretation', 'prudence', 'preuve faible', 'plausible', 'reconstruction_retrospective', 'a verifier'])) return 'vigilance';
    if (hasAny(type, ['scene']) || hasAny(text, ['scene fondatrice', 'moment originel', 'episode', 'concert', 'session', 'rencontre'])) return 'scenes';
    if (hasAny(type, ['lecture', 'interpretation', 'analyse']) || hasAny(text, ['lecture', 'interpretation', 'hypothese', 'analyse critique'])) return 'readings';
    if (kind === 'chronology' || hasAny(type, ['fait', 'biographie', 'lieu', 'temoignage', 'session'])) return 'facts';
    return 'other';
  }

  function groupResults(results) {
    const grouped = Object.fromEntries(GROUPS.map(group => [group.id, []]));
    for (const result of results || []) {
      grouped[classify(result)].push(result);
    }
    return grouped;
  }

  function ensurePanel() {
    let panel = $('rag3-panel');
    if (panel) return panel;

    const resultsPanel = document.querySelector('.results-panel');
    if (!resultsPanel) return null;

    panel = document.createElement('section');
    panel.id = 'rag3-panel';
    panel.className = 'rag3-panel status-card';
    panel.innerHTML = `
      <div class="rag3-header">
        <div>
          <h2>RAG 3 — Dossier regroupé</h2>
          <p class="panel-note">Regroupement automatique des résultats par rôle documentaire.</p>
        </div>
        <button type="button" id="rag3-copy">Copier le dossier</button>
      </div>
      <div id="rag3-summary"></div>
      <div id="rag3-groups"></div>
    `;
    resultsPanel.appendChild(panel);

    const copy = $('rag3-copy');
    if (copy) copy.addEventListener('click', copyGroupedMarkdown);
    return panel;
  }

  function itemLine(result) {
    const fields = fieldsOf(result);
    const source = sourceOf(result);
    const type = typeOf(result);
    const importance = importanceOf(result);
    const proof = proofOf(result);
    const bits = [];
    if (source) bits.push(`source : ${source}`);
    if (type) bits.push(`type : ${type}`);
    if (importance) bits.push(`importance : ${importance}`);
    if (proof) bits.push(`preuve : ${proof}`);
    return `<li><strong>${escapeHtml(titleOf(result))}</strong>${bits.length ? `<br><span>${escapeHtml(bits.join(' ; '))}</span>` : ''}</li>`;
  }

  function escapeHtml(value) {
    return String(value || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function renderGroups() {
    const panel = ensurePanel();
    if (!panel || !window.rag2?.state) return;
    const results = window.rag2.state.results || [];
    const grouped = groupResults(results);
    const summary = $('rag3-summary');
    const container = $('rag3-groups');
    if (!summary || !container) return;

    const counts = GROUPS.map(group => `${group.title} : ${grouped[group.id].length}`).join(' · ');
    summary.textContent = `${results.length} résultat(s) regroupé(s) · ${counts}`;

    container.innerHTML = '';
    for (const group of GROUPS) {
      const items = grouped[group.id];
      if (!items.length) continue;
      const section = document.createElement('section');
      section.className = `rag3-group rag3-${group.id}`;
      section.innerHTML = `
        <h3>${escapeHtml(group.title)} <span>${items.length}</span></h3>
        <p class="panel-note">${escapeHtml(group.hint)}</p>
        <ol>${items.slice(0, 30).map(itemLine).join('')}</ol>
        ${items.length > 30 ? `<p class="panel-note">${items.length - 30} résultat(s) supplémentaire(s) non affiché(s) dans ce groupe.</p>` : ''}
      `;
      container.appendChild(section);
    }
  }

  function groupedMarkdown() {
    const results = window.rag2?.state?.results || [];
    const grouped = groupResults(results);
    const lines = ['# RAG 3 — Dossier regroupé', '', `${results.length} résultat(s)`, ''];
    for (const group of GROUPS) {
      const items = grouped[group.id];
      if (!items.length) continue;
      lines.push(`## ${group.title}`, '');
      for (const item of items) {
        const fields = fieldsOf(item);
        const meta = [sourceOf(item), typeOf(item), importanceOf(item), proofOf(item)].filter(Boolean).join(' ; ');
        lines.push(`- ${titleOf(item)}${meta ? ` — ${meta}` : ''}`);
        if (fields.citation_originale) lines.push(`  Citation : « ${stringify(fields.citation_originale)} »`);
      }
      lines.push('');
    }
    return lines.join('\n');
  }

  async function copyGroupedMarkdown() {
    const text = groupedMarkdown();
    try {
      await navigator.clipboard.writeText(text);
      const copy = $('rag3-copy');
      if (copy) {
        const previous = copy.textContent;
        copy.textContent = 'Copié';
        setTimeout(() => { copy.textContent = previous; }, 1200);
      }
    } catch (error) {
      console.warn('Clipboard unavailable', error);
    }
  }

  function patchRag2() {
    if (!window.rag2 || window.rag2.__rag3Patched) return false;
    const originalPerformSearch = window.rag2.performSearch;
    window.rag2.performSearch = function patchedPerformSearch() {
      const output = originalPerformSearch.apply(this, arguments);
      setTimeout(renderGroups, 0);
      return output;
    };
    window.rag2.__rag3Patched = true;
    return true;
  }

  function bindPassiveRefresh() {
    const form = $('search-form');
    if (form) form.addEventListener('submit', () => setTimeout(renderGroups, 10));
    for (const id of ['kind','chapter-filter','source-filter','type-filter','importance-filter','proof-filter','concept-filter','motif-filter','top']) {
      const node = $(id);
      if (node) node.addEventListener('change', () => setTimeout(renderGroups, 10));
    }
    for (const button of document.querySelectorAll('.example-query')) {
      button.addEventListener('click', () => setTimeout(renderGroups, 10));
    }
  }

  function initRag3() {
    ensurePanel();
    patchRag2();
    bindPassiveRefresh();
    renderGroups();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initRag3);
  } else {
    setTimeout(initRag3, 0);
  }

  window.rag3 = {renderGroups, groupResults, groupedMarkdown};
})();
