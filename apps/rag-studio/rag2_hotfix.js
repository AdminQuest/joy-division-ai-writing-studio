// RAG 2 hotfix
// Prevents global scoreRecords recursion caused by exposing a wrapper under the
// same global name as the internal function. This file is intentionally small
// and loaded after app.js.

(function () {
  function currentFilters() {
    const get = id => document.getElementById(id)?.value || '';
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

  const originalPerformSearch = window.performSearch;

  if (typeof originalPerformSearch === 'function') {
    window.performSearch = function () {
      return originalPerformSearch();
    };
  }

  // Do not expose a scoreRecords wrapper here. app.js owns the internal search
  // function. The previous global wrapper caused infinite recursion in browsers
  // because top-level function declarations are window properties.
  window.currentRagFilters = currentFilters;
})();
