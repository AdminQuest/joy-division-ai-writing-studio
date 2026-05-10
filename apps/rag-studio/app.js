async function fetchStatus() {
  const card = document.getElementById('status-card');

  try {
    const response = await fetch('/api/status');
    const data = await response.json();

    if (!data.ok) {
      card.textContent = data.error;
      return;
    }

    const counts = Object.entries(data.counts)
      .map(([kind, count]) => `${kind}: ${count}`)
      .join(' · ');

    card.textContent = `Corpus chargé · ${data.records} enregistrements · ${counts}`;
  } catch (error) {
    card.textContent = `Erreur : ${error.message}`;
  }
}

function clearResults() {
  document.getElementById('results').innerHTML = '';
  document.getElementById('results-meta').textContent = '';
}

function addField(dl, key, value) {
  if (value === undefined || value === null || value === '') {
    return;
  }

  const dt = document.createElement('dt');
  dt.textContent = key;

  const dd = document.createElement('dd');

  if (typeof value === 'object') {
    dd.textContent = JSON.stringify(value, null, 2);
  } else {
    dd.textContent = value;
  }

  dl.appendChild(dt);
  dl.appendChild(dd);
}

function renderResults(data) {
  clearResults();

  const results = document.getElementById('results');
  const meta = document.getElementById('results-meta');
  const template = document.getElementById('result-template');

  meta.textContent = `${data.total_matches} résultat(s)`;

  if (!data.results.length) {
    const empty = document.createElement('div');
    empty.className = 'status-card';
    empty.textContent = 'Aucun résultat.';
    results.appendChild(empty);
    return;
  }

  for (const item of data.results) {
    const node = template.content.cloneNode(true);

    node.querySelector('.result-kind').textContent = item.record.kind;
    node.querySelector('.result-score').textContent = `score ${item.score}`;

    node.querySelector('.result-title').textContent = item.record.id;
    node.querySelector('.result-file').textContent = item.record.file;

    const fields = node.querySelector('.result-fields');

    for (const [key, value] of Object.entries(item.record.summary_fields)) {
      addField(fields, key, value);
    }

    results.appendChild(node);
  }
}

async function performSearch(query, kind, top) {
  const params = new URLSearchParams({
    q: query,
    top,
  });

  if (kind) {
    params.set('kind', kind);
  }

  const results = document.getElementById('results');
  results.innerHTML = '<div class="status-card">Recherche en cours…</div>';

  const response = await fetch(`/api/search?${params.toString()}`);
  const data = await response.json();

  if (!data.ok) {
    results.innerHTML = `<div class="status-card">${data.error}</div>`;
    return;
  }

  renderResults(data);
}

function bindExamples() {
  for (const button of document.querySelectorAll('.example-query')) {
    button.addEventListener('click', () => {
      const query = button.dataset.query;
      document.getElementById('query').value = query;
      performSearch(query, '', 10);
    });
  }
}

function bindForm() {
  const form = document.getElementById('search-form');

  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const query = document.getElementById('query').value.trim();
    const kind = document.getElementById('kind').value;
    const top = document.getElementById('top').value;

    if (!query) {
      return;
    }

    await performSearch(query, kind, top);
  });
}

fetchStatus();
bindExamples();
bindForm();
