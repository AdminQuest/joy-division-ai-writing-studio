async function fetchJSON(url){
  const r = await fetch(url);
  if(!r.ok) throw new Error(`HTTP ${r.status}`);
  return await r.json();
}

async function fetchText(url){
  const r = await fetch(url);
  if(!r.ok) throw new Error(`HTTP ${r.status}`);
  return await r.text();
}

const listEl = document.getElementById('chapter-list');
const contentEl = document.getElementById('content');
const titleEl = document.getElementById('doc-title');
const metaEl = document.getElementById('doc-meta');
const rawLink = document.getElementById('raw-link');
const copyBtn = document.getElementById('copy-btn');

let currentMarkdown = '';
let mode = 'api';
let docsCache = [];

copyBtn.addEventListener('click', async () => {
  if(!currentMarkdown) return;
  await navigator.clipboard.writeText(currentMarkdown);
  copyBtn.textContent = 'Copié';
  setTimeout(() => copyBtn.textContent = 'Copier', 1200);
});

function extractTitle(markdown, fallback){
  const line = markdown.split('\n').find(l => l.startsWith('# '));
  return line ? line.replace(/^#\s+/, '').trim() : fallback;
}

async function loadDocsManifest(){
  try{
    const data = await fetchJSON('/api/master-docs');
    mode = 'api';
    return data.documents || [];
  }catch(e){
    const data = await fetchJSON('../../chapters/master_docs.json');
    mode = 'static';
    return data.documents || [];
  }
}

async function loadDoc(chapter){
  let data;

  if(mode === 'api'){
    data = await fetchJSON(`/api/master-doc?chapter=${chapter}`);
    currentMarkdown = data.content;
    titleEl.textContent = data.title;
    metaEl.textContent = data.path;
    rawLink.href = `/api/master-doc-raw?chapter=${chapter}`;
  }else{
    const doc = docsCache.find(d => String(d.chapter) === String(chapter));
    const path = doc?.path || `chapters/${String(chapter).padStart(2, '0')}/document_maitre.md`;
    const staticUrl = `../../${path}`;
    currentMarkdown = await fetchText(staticUrl);
    titleEl.textContent = extractTitle(currentMarkdown, doc?.title || `Chapitre ${chapter}`);
    metaEl.textContent = path;
    rawLink.href = staticUrl;
  }

  contentEl.classList.remove('empty');
  contentEl.textContent = currentMarkdown;

  document.querySelectorAll('.chapter-item').forEach(el => {
    el.classList.toggle('active', el.dataset.chapter === String(chapter));
  });
}

async function init(){
  try{
    docsCache = await loadDocsManifest();
  }catch(e){
    contentEl.textContent = `Impossible de charger les documents maîtres : ${e.message}`;
    return;
  }

  docsCache.forEach(doc => {
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

  if(docsCache.length){
    loadDoc(docsCache[0].chapter);
  }
}

init();
