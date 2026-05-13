// RAG 4 — générateur de prompt de rédaction
// Ce module s'appuie sur les résultats filtrés par RAG 2 et, si disponible,
// sur le regroupement Markdown produit par RAG 3. Il ne rédige pas le chapitre :
// il prépare un prompt exploitable dans ChatGPT, Claude ou NotebookLM.

(function () {
  function $(id) {
    return document.getElementById(id);
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

  function corpusLines(results, max = 60) {
    if (!results?.length) return ['- Aucun résultat actuellement sélectionné. Lance d’abord une recherche ou applique un filtre.'];
    return results.slice(0, max).map(result => {
      const fields = fieldsOf(result);
      const meta = [
        fields.source_label || fields.source_id,
        fields.type_unite,
        stringify(fields.importance).replace(/\n/g, ' '),
        stringify(fields.niveau_preuve).replace(/\n/g, ' ')
      ].filter(Boolean).join(' ; ');
      return `- ${titleOf(result)}${meta ? ` — ${meta}` : ''}`;
    });
  }

  function citationLines(results, max = 20) {
    const citations = (results || []).filter(result => {
      const fields = fieldsOf(result);
      return result.record?.kind === 'quote' || fields.citation_originale || fields.traduction_editoriale_fr;
    });
    if (!citations.length) return ['- Aucune citation directement présente dans les résultats filtrés.'];
    return citations.slice(0, max).map(result => {
      const fields = fieldsOf(result);
      const citation = fields.citation_originale || fields.traduction_editoriale_fr || '';
      const status = fields.statut_consolidation || fields.statut_verification || fields.niveau_preuve || 'statut à vérifier';
      return `- ${titleOf(result)} — statut : ${stringify(status).replace(/\n/g, ' ')} — « ${stringify(citation).replace(/\n/g, ' ')} »`;
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
      '## 3. Corpus à mobiliser',
      '',
      ...corpusLines(results),
      '',
      '## 4. Dossier regroupé par rôle documentaire',
      '',
      groupedSection(),
      '',
      '## 5. Citations disponibles',
      '',
      ...citationLines(results),
      '',
      '## 6. Contraintes historiographiques',
      '',
      ...historiographicConstraints(),
      '',
      '## 7. Contraintes stylistiques du projet',
      '',
      ...styleConstraints(),
      '',
      '## 8. Consigne de rédaction',
      '',
      'À partir du corpus ci-dessus, rédige une section structurée du manuscrit. La section doit être argumentative, non cumulative. Elle doit faire apparaître les tensions documentaires, hiérarchiser les preuves et intégrer les citations seulement lorsque leur statut le permet. Elle doit conserver le style du projet : une prose académique, dense, précise, alternant phrases brèves et phrases plus longues, avec une attention particulière aux images de l’espace, du son, du vide et de la mémoire.',
      '',
      'Ne produis pas une simple fiche. Produis un texte rédigé, directement intégrable après révision dans le manuscrit.'
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
          <h2>RAG 4 — Prompt de rédaction</h2>
          <p class="panel-note">Génère un prompt à partir du corpus filtré et du dossier regroupé.</p>
        </div>
        <div class="rag4-actions">
          <button type="button" id="rag4-refresh">Générer le prompt</button>
          <button type="button" id="rag4-copy">Copier le prompt</button>
        </div>
      </div>
      <textarea id="rag4-output" rows="18" spellcheck="false" placeholder="Le prompt de rédaction apparaîtra ici après une recherche."></textarea>
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
