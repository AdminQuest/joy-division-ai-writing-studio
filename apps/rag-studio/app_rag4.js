// RAG 4 — générateur de prompt de rédaction autonome
// Ce module s'appuie sur les résultats filtrés par RAG 2 et le regroupement RAG 3.
// Il produit un prompt qui reste exploitable même dans une IA n'ayant pas accès au repo,
// car il embarque les informations essentielles des atomes sélectionnés.

(function () {
  function $(id) {
    return document.getElementById(id);
  }

  function stringify(value) {
    if (value === undefined || value === null) return '';
    if (typeof value === 'string') return value;
    try { return JSON.stringify(value, null, 2); } catch (_) { return String(value); }
  }

  function compact(value, max = 900) {
    const text = stringify(value).replace(/\s+/g, ' ').trim();
    return text.length > max ? text.slice(0, max) + '…' : text;
  }

  function fieldsOf(result) {
    return result?.record?.summary_fields || {};
  }

  function idOf(result) {
    return result?.record?.id || '';
  }

  function fullRecordFor(result) {
    const id = idOf(result);
    const records = window.rag2?.state?.records || [];
    return records.find(record => record.id === id) || result?.record || {};
  }

  function fullDataOf(result) {
    const record = fullRecordFor(result);
    return record?.data || record?.summary_fields || fieldsOf(result) || {};
  }

  function titleOf(result) {
    const record = fullRecordFor(result);
    const data = fullDataOf(result);
    const fields = fieldsOf(result);
    return record.id || data.titre || fields.titre || record.heading || '(sans id)';
  }

  function activeFilters() {
    if (window.rag2?.currentFilters) return window.rag2.currentFilters();
    const get = id => $(id)?.value || '';
    return {
      kind: get('kind'),
      chapter: get('chapter-filter'),
      source: get('source-filter'),
      type: get('type-filter'),
      importance: get('importance-filter'),
      proof: get('proof-filter'),
      concept: get('concept-filter'),
      motif: get('motif-filter')
    };
  }

  function filterLine(filters) {
    const parts = [];
    if (filters.chapter) parts.push(`chapitre : ${filters.chapter}`);
    if (filters.source) parts.push(`source : ${filters.source}`);
    if (filters.kind) parts.push(`type documentaire : ${filters.kind}`);
    if (filters.type) parts.push(`type_unite : ${filters.type}`);
    if (filters.importance) parts.push(`importance : ${filters.importance}`);
    if (filters.proof) parts.push(`niveau de preuve : ${filters.proof}`);
    if (filters.concept) parts.push(`concept : ${filters.concept}`);
    if (filters.motif) parts.push(`motif : ${filters.motif}`);
    return parts.length ? parts.join(' ; ') : 'aucun filtre structuré actif';
  }

  function queryText() {
    return $('query')?.value.trim() || '';
  }

  function inferObjective(filters, query) {
    const base = [];
    if (filters.chapter) base.push(`à partir du corpus filtré sur ${filters.chapter}`);
    if (filters.source) base.push(`en mobilisant prioritairement la source ${filters.source}`);
    if (filters.concept) base.push(`autour du concept « ${filters.concept} »`);
    if (filters.motif) base.push(`autour du motif « ${filters.motif} »`);
    if (query) base.push(`sur l’axe lexical « ${query} »`);
    if (!base.length) return 'Rédiger une section du manuscrit à partir du corpus actuellement affiché, en distinguant les faits, les lectures, les mythes, les controverses et les citations.';
    return `Rédiger une section du manuscrit ${base.join(', ')}.`;
  }

  function sourceOf(result) {
    const data = fullDataOf(result);
    const fields = fieldsOf(result);
    return fields.source_label || data.source_label || data.source_id || fields.source_id || '';
  }

  function valueAt(obj, path) {
    let cursor = obj;
    for (const part of path.split('.')) {
      if (!cursor || typeof cursor !== 'object' || !(part in cursor)) return '';
      cursor = cursor[part];
    }
    return cursor;
  }

  function atomBrief(result, index) {
    const record = fullRecordFor(result);
    const data = fullDataOf(result);
    const fields = fieldsOf(result);
    const id = record.id || idOf(result) || `RESULT-${index + 1}`;
    const source = sourceOf(result);
    const type = data.type_unite || fields.type_unite || record.kind || '';
    const importance = data.importance || fields.importance || '';
    const proof = data.niveau_preuve || fields.niveau_preuve || data.fiabilite || data.certainty || fields.certainty || '';
    const summary = data.resume || data.résumé || data.argument || data.description || data.event || data.citation_directe || fields.citation_originale || fields.titre || titleOf(result);
    const role = data.role_argumentatif || data.usage_recommande || data.usage || '';
    const concepts = data.concepts || fields.concepts || '';
    const motifs = data.motifs || fields.motifs || '';
    const risk = data.risque_surinterpretation || data.limites_usage || data.contradictions || '';
    const relations = data.relations || data.liens_interchapitres || '';
    const quote = data.citation_originale || data.citation_directe || fields.citation_originale || data.traduction_editoriale_fr || fields.traduction_editoriale_fr || '';

    const lines = [
      `### ${id} — ${compact(titleOf(result), 160)}`,
      source ? `- Source : ${compact(source, 240)}` : '',
      type ? `- Type documentaire : ${compact(type, 160)}` : '',
      importance ? `- Importance : ${compact(importance, 240)}` : '',
      proof ? `- Niveau de preuve : ${compact(proof, 300)}` : '',
      summary ? `- Contenu utile : ${compact(summary, 1100)}` : '',
      role ? `- Rôle argumentatif : ${compact(role, 700)}` : '',
      concepts ? `- Concepts : ${compact(concepts, 500)}` : '',
      motifs ? `- Motifs : ${compact(motifs, 500)}` : '',
      risk ? `- Prudence / risque : ${compact(risk, 700)}` : '',
      relations ? `- Relations : ${compact(relations, 700)}` : '',
      quote ? `- Citation disponible : « ${compact(quote, 700)} »` : ''
    ].filter(Boolean);

    return lines.join('\n');
  }

  function autonomousCorpusSection(results, max = 45) {
    if (!results?.length) return 'Aucun résultat actuellement sélectionné. Lance d’abord une recherche ou applique un filtre.';
    const shown = results.slice(0, max).map(atomBrief).join('\n\n');
    const hidden = results.length > max ? `\n\n> ${results.length - max} résultat(s) supplémentaire(s) non inclus pour limiter la taille du prompt.` : '';
    return shown + hidden;
  }

  function corpusLines(results, max = 60) {
    if (!results?.length) return ['- Aucun résultat actuellement sélectionné. Lance d’abord une recherche ou applique un filtre.'];
    return results.slice(0, max).map(result => {
      const data = fullDataOf(result);
      const fields = fieldsOf(result);
      const meta = [
        sourceOf(result),
        data.type_unite || fields.type_unite,
        stringify(data.importance || fields.importance).replace(/\n/g, ' '),
        stringify(data.niveau_preuve || fields.niveau_preuve).replace(/\n/g, ' ')
      ].filter(Boolean).join(' ; ');
      return `- ${titleOf(result)}${meta ? ` — ${meta}` : ''}`;
    });
  }

  function citationLines(results, max = 20) {
    const citations = (results || []).filter(result => {
      const data = fullDataOf(result);
      const fields = fieldsOf(result);
      return result.record?.kind === 'quote' || data.citation_originale || data.citation_directe || fields.citation_originale || data.traduction_editoriale_fr;
    });
    if (!citations.length) return ['- Aucune citation directement présente dans les résultats filtrés.'];
    return citations.slice(0, max).map(result => {
      const data = fullDataOf(result);
      const fields = fieldsOf(result);
      const citation = data.citation_originale || data.citation_directe || fields.citation_originale || data.traduction_editoriale_fr || fields.traduction_editoriale_fr || '';
      const status = data.statut_consolidation || data.statut_verification || fields.statut_consolidation || fields.statut_verification || data.niveau_preuve || fields.niveau_preuve || 'statut à vérifier';
      return `- ${titleOf(result)} — statut : ${compact(status, 220)} — « ${compact(citation, 900)} »`;
    });
  }

  function groupedSection() {
    if (window.rag3?.groupedMarkdown) return window.rag3.groupedMarkdown();
    return '# RAG 3 — Dossier regroupé\n\nIndisponible : le module RAG 3 n’est pas chargé.';
  }

  function styleConstraints() {
    return [
      '- Rédiger en français, au présent.',
      '- Employer un style académique, mais nerveux, adapté au projet Joy Division.',
      '- Utiliser les guillemets français.',
      '- Mettre les albums en italique et les titres de chansons entre guillemets français.',
      '- Ne pas inventer de citations ; n’utiliser que les citations explicitement fournies dans le corpus.',
      '- Signaler toute citation dont le statut n’est pas consolidé au lieu de l’intégrer comme preuve ferme.',
      '- Distinguer systématiquement fait établi, témoignage rétrospectif, lecture critique, mythe et controverse.',
      '- Éviter la téléologie morbide : ne pas lire chaque fait à travers la mort de Ian Curtis.',
      '- Éviter les formulations interdites du projet : « Dans le monde d’aujourd’hui… », « À une époque où », « Le rythme s’accélère », « Approfondir », « Non seulement, mais aussi… ».',
      '- Éviter les tricolons mécaniques du type : « il fait ceci, cela, mais aussi cela ».',
      '- Ne pas transformer le dossier documentaire en simple résumé ; construire une progression argumentative.',
      '- Éviter les redondances avec les chapitres voisins ; mentionner les renvois utiles si nécessaire.'
    ];
  }

  function historiographicConstraints() {
    return [
      '- Ne pas confondre causalité et contexte.',
      '- Ne pas transformer un souvenir de musicien en fait objectif sans précaution.',
      '- Ne pas rabattre l’œuvre de Joy Division sur la seule biographie de Curtis.',
      '- Identifier les mythes de fondation et les déconstruire sans les effacer : ils font partie de l’histoire de la réception.',
      '- Quand plusieurs sources convergent, le signaler comme corroboration ; quand elles divergent, formuler la tension documentaire.',
      '- Utiliser les concepts et motifs comme outils d’analyse, non comme slogans.',
      '- Préférer les formulations prudentes lorsque le niveau de preuve est faible, plausible ou rétrospectif.'
    ];
  }

  function generatePrompt() {
    const results = window.rag2?.state?.results || [];
    const filters = activeFilters();
    const query = queryText();
    const objective = inferObjective(filters, query);
    const generatedAt = new Date().toISOString();

    const lines = [
      '# PROMPT DE RÉDACTION — Joy Division',
      '',
      '## 1. Objectif',
      '',
      objective,
      '',
      '## 2. Périmètre du corpus filtré',
      '',
      `- Requête lexicale : ${query ? `« ${query} »` : 'aucune'}`,
      `- Filtres structurés : ${filterLine(filters)}`,
      `- Nombre de résultats : ${results.length}`,
      `- Généré le : ${generatedAt}`,
      '',
      '## 3. Corpus à mobiliser — index rapide',
      '',
      ...corpusLines(results),
      '',
      '## 4. Dossier documentaire autonome',
      '',
      autonomousCorpusSection(results),
      '',
      '## 5. Dossier regroupé par rôle documentaire',
      '',
      groupedSection(),
      '',
      '## 6. Citations disponibles',
      '',
      ...citationLines(results),
      '',
      '## 7. Contraintes historiographiques',
      '',
      ...historiographicConstraints(),
      '',
      '## 8. Contraintes stylistiques du projet',
      '',
      ...styleConstraints(),
      '',
      '## 9. Consigne de rédaction',
      '',
      'À partir du corpus ci-dessus, rédige une section structurée du manuscrit. La section doit être argumentative, non cumulative. Elle doit faire apparaître les tensions documentaires, hiérarchiser les preuves et intégrer les citations seulement lorsque leur statut le permet. Elle doit conserver le style du projet : une prose académique, dense, précise, alternant phrases brèves et phrases plus longues, avec une attention particulière aux images de l’espace, du son, du vide et de la mémoire.',
      '',
      'Ne produis pas une simple fiche. Produis un texte rédigé, directement intégrable après révision dans le manuscrit. N’utilise aucune information extérieure au corpus fourni, sauf si elle est explicitement demandée ensuite.'
    ];

    return lines.join('\n');
  }

  function ensurePanel() {
    let panel = $('rag4-panel');
    if (panel) return panel;
    const resultsPanel = document.querySelector('.results-panel');
    if (!resultsPanel) return null;

    panel = document.createElement('section');
    panel.id = 'rag4-panel';
    panel.className = 'rag4-panel status-card';
    panel.innerHTML = `
      <div class="rag4-header">
        <div>
          <h2>RAG 4 — Prompt de rédaction autonome</h2>
          <p class="panel-note">Génère un prompt qui embarque le contenu utile des atomes sélectionnés.</p>
        </div>
        <div class="rag4-actions">
          <button type="button" id="rag4-refresh">Générer le prompt</button>
          <button type="button" id="rag4-copy">Copier le prompt</button>
        </div>
      </div>
      <textarea id="rag4-output" rows="22" spellcheck="false" placeholder="Le prompt de rédaction apparaîtra ici après une recherche."></textarea>
    `;
    resultsPanel.appendChild(panel);

    $('rag4-refresh')?.addEventListener('click', renderPrompt);
    $('rag4-copy')?.addEventListener('click', copyPrompt);
    return panel;
  }

  function renderPrompt() {
    ensurePanel();
    const output = $('rag4-output');
    if (!output) return;
    output.value = generatePrompt();
  }

  async function copyPrompt() {
    const output = $('rag4-output');
    if (!output) return;
    if (!output.value.trim()) output.value = generatePrompt();
    try {
      await navigator.clipboard.writeText(output.value);
      const button = $('rag4-copy');
      if (button) {
        const previous = button.textContent;
        button.textContent = 'Copié';
        setTimeout(() => { button.textContent = previous; }, 1200);
      }
    } catch (error) {
      console.warn('Clipboard unavailable', error);
    }
  }

  function patchRag2() {
    if (!window.rag2 || window.rag2.__rag4Patched) return false;
    const originalPerformSearch = window.rag2.performSearch;
    window.rag2.performSearch = function patchedPerformSearch() {
      const output = originalPerformSearch.apply(this, arguments);
      setTimeout(renderPrompt, 20);
      return output;
    };
    window.rag2.__rag4Patched = true;
    return true;
  }

  function bindPassiveRefresh() {
    const form = $('search-form');
    if (form) form.addEventListener('submit', () => setTimeout(renderPrompt, 30));
    for (const id of ['kind','chapter-filter','source-filter','type-filter','importance-filter','proof-filter','concept-filter','motif-filter','top']) {
      const node = $(id);
      if (node) node.addEventListener('change', () => setTimeout(renderPrompt, 30));
    }
    for (const button of document.querySelectorAll('.example-query')) {
      button.addEventListener('click', () => setTimeout(renderPrompt, 30));
    }
  }

  function initRag4() {
    ensurePanel();
    patchRag2();
    bindPassiveRefresh();
    renderPrompt();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initRag4);
  } else {
    setTimeout(initRag4, 0);
  }

  window.rag4 = {generatePrompt, renderPrompt, copyPrompt};
})();
