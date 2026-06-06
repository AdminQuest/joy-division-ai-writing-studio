const state = {
  batchItems: []
};

const $ = id => document.getElementById(id);
const text = value => String(value || '').trim();
const oneLine = value => text(value).replace(/\s+/g, ' ');
const splitList = value => text(value).split(',').map(item => item.trim()).filter(Boolean);
const escHtml = value => text(value)
  .replace(/&/g, '&amp;')
  .replace(/</g, '&lt;')
  .replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;');

function shellQuote(value) {
  const raw = text(value);
  if (!raw) return "''";
  return "'" + raw.replace(/'/g, "'\"'\"'") + "'";
}

function command(parts) {
  return parts.filter(Boolean).join(' ');
}

function option(flag, value) {
  return text(value) ? `${flag} ${shellQuote(value)}` : '';
}

function readPerson() {
  return {
    family: 'person',
    name: text($('person-name').value),
    category: text($('person-category').value),
    roles: splitList($('person-roles').value),
    sources: splitList($('person-sources').value),
    note: text($('person-note').value)
  };
}

function readOrg() {
  return {
    family: 'org',
    name: text($('org-name').value),
    category: text($('org-category').value),
    country: text($('org-country').value),
    jd_relation: text($('org-jd-relation').value),
    sources: splitList($('org-sources').value),
    last_verified: text($('org-last-verified').value),
    relation_notes: text($('org-note').value)
  };
}

function readSource() {
  return {
    title: text($('source-title').value),
    author: text($('source-author').value),
    type: text($('source-type').value),
    year: text($('source-year').value),
    reference: text($('source-reference').value),
    note: text($('source-note').value)
  };
}

function cleanObject(input) {
  const output = {};
  Object.entries(input).forEach(([key, value]) => {
    if (Array.isArray(value)) {
      if (value.length) output[key] = value;
    } else if (text(value)) {
      output[key] = value;
    }
  });
  return output;
}

function personCommand() {
  const item = readPerson();
  return command([
    'python3 tools/m2_add_person.py',
    option('--name', item.name),
    option('--category', item.category),
    item.roles.map(role => option('--role', role)).join(' '),
    option('--sources', item.sources.join(',')),
    option('--note', item.note),
    '--pr-summary'
  ]);
}

function orgCommand() {
  const item = readOrg();
  return command([
    'python3 tools/m2_add_org.py',
    option('--name', item.name),
    option('--category', item.category),
    option('--country', item.country),
    option('--jd-relation', item.jd_relation),
    option('--sources', item.sources.join(',')),
    option('--last-verified', item.last_verified),
    option('--relation-notes', item.relation_notes),
    '--pr-summary'
  ]);
}

function sourceCommand() {
  const item = readSource();
  const base = command([
    'python3 tools/m2_integrate_source.py',
    option('--title', item.title),
    option('--author', item.author),
    option('--type', item.type),
    option('--year', item.year),
    option('--reference', item.reference),
    '--pr-summary'
  ]);
  return item.note ? `${base}\n# notes: ${oneLine(item.note)}` : base;
}

function batchPayload() {
  return {
    campaign: text($('batch-campaign').value) || 'campagne-m2',
    items: state.batchItems.map(cleanObject)
  };
}

function renderBatch() {
  const list = $('batch-list');
  if (!state.batchItems.length) {
    list.innerHTML = '<p class="m2-empty">Aucun item PERSON ou ORG dans la campagne.</p>';
  } else {
    list.innerHTML = state.batchItems.map((item, index) => {
      const label = item.name || `item-${index + 1}`;
      const meta = item.family === 'person'
        ? [item.category, item.sources.join(',')].filter(Boolean).join(' - ')
        : [item.category, item.country, item.sources.join(',')].filter(Boolean).join(' - ');
      return `<div class="m2-batch-item">
        <div><strong>${escHtml(item.family.toUpperCase())} - ${escHtml(label)}</strong><span>${escHtml(meta)}</span></div>
        <button class="m2-btn m2-btn--ghost" type="button" data-remove-batch="${index}">Retirer</button>
      </div>`;
    }).join('');
  }

  $('batch-json-output').textContent = JSON.stringify(batchPayload(), null, 2);
  $('batch-command-output').textContent = 'python3 tools/m2_batch_prevalidation.py path/to/campaign.json';
}

function setStatus(message) {
  $('m2-status').textContent = message;
}

function addBatchItem(item) {
  state.batchItems.push(item);
  renderBatch();
  setStatus(`${item.family.toUpperCase()} ajoute au batch.`);
}

async function copyOutput(id) {
  const value = $(id).textContent;
  if (!value) {
    setStatus('Aucune sortie a copier.');
    return;
  }
  try {
    await navigator.clipboard.writeText(value);
    setStatus('Sortie copiee.');
  } catch (_error) {
    const range = document.createRange();
    range.selectNodeContents($(id));
    const selection = window.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
    setStatus('Sortie selectionnee.');
  }
}

function activateTab(name) {
  document.querySelectorAll('[data-tab]').forEach(button => {
    button.classList.toggle('is-active', button.dataset.tab === name);
  });
  document.querySelectorAll('[data-panel]').forEach(panel => {
    panel.hidden = panel.dataset.panel !== name;
  });
}

function bindEvents() {
  document.querySelectorAll('[data-tab]').forEach(button => {
    button.addEventListener('click', () => activateTab(button.dataset.tab));
  });

  document.querySelector('[data-action="person-command"]').addEventListener('click', () => {
    $('person-output').textContent = personCommand();
    setStatus('Commande PERSON generee.');
  });
  document.querySelector('[data-action="org-command"]').addEventListener('click', () => {
    $('org-output').textContent = orgCommand();
    setStatus('Commande ORG generee.');
  });
  document.querySelector('[data-action="source-command"]').addEventListener('click', () => {
    $('source-output').textContent = sourceCommand();
    setStatus('Commande SOURCE LONGUE generee.');
  });
  document.querySelector('[data-action="person-batch"]').addEventListener('click', () => addBatchItem(readPerson()));
  document.querySelector('[data-action="org-batch"]').addEventListener('click', () => addBatchItem(readOrg()));
  document.querySelector('[data-action="clear-batch"]').addEventListener('click', () => {
    state.batchItems = [];
    renderBatch();
    setStatus('Batch vide.');
  });
  $('batch-campaign').addEventListener('input', renderBatch);

  document.addEventListener('click', event => {
    const copyButton = event.target.closest('[data-copy]');
    if (copyButton) copyOutput(copyButton.dataset.copy);

    const removeButton = event.target.closest('[data-remove-batch]');
    if (removeButton) {
      state.batchItems.splice(Number(removeButton.dataset.removeBatch), 1);
      renderBatch();
      setStatus('Item retire du batch.');
    }
  });
}

function init() {
  $('person-output').textContent = personCommand();
  $('org-output').textContent = orgCommand();
  $('source-output').textContent = sourceCommand();
  renderBatch();
  bindEvents();
}

init();
