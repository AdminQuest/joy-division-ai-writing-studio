async function fetchJSON(url){
  const r = await fetch(url);
  if(!r.ok) throw new Error(`HTTP ${r.status}`);
  return await r.json();
}

const listEl = document.getElementById('chapter-list');
const contentEl = document.getElementById('content');
const titleEl = document.getElementById('doc-title');
const metaEl = document.getElementById('doc-meta');
const rawLink = document.getElementById('raw-link');
const copyBtn = document.getElementById('copy-btn');

let currentMarkdown = '';

copyBtn.addEventListener('click', async () => {
  if(!currentMarkdown) return;
  await navigator.clipboard.writeText(currentMarkdown);
  copyBtn.textContent = 'Copié';
  setTimeout(() => copyBtn.textContent = 'Copier', 1200);
});

async function loadDoc(chapter){
  const data = await fetchJSON(`/api/master-doc?chapter=${chapter}`);

  currentMarkdown = data.content;

  titleEl.textContent = data.title;
  metaEl.textContent = data.path;
  rawLink.href = `/api/master-doc-raw?chapter=${chapter}`;

  contentEl.classList.remove('empty');
  contentEl.textContent = data.content;

  document.querySelectorAll('.chapter-item').forEach(el => {
    el.classList.toggle('active', el.dataset.chapter === String(chapter));
  });
}

async function init(){
  const docs = await fetchJSON('/api/master-docs');

  docs.documents.forEach(doc => {
    const item = document.createElement('div');
    item.className = 'chapter-item';
    item.dataset.chapter = doc.chapter;
    item.innerHTML = `
      <div class="chapter-num">Chapitre ${doc.chapter}</div>
      <div class="chapter-title">${doc.title}</div>
    `;

    item.addEventListener('click', () => loadDoc(doc.chapter));
    listEl.appendChild(item);
  });

  if(docs.documents.length){
    loadDoc(docs.documents[0].chapter);
  }
}

init();
