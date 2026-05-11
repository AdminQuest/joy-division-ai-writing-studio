const ORIGINAL_RENDER_RESULTS = window.renderResults;
const RESULTS_STATE = {
  all: [],
  currentPage: 1,
  perPage: 10,
  totalMatches: 0,
};

function renderPagination(totalPages) {
  const container = document.getElementById('pagination');
  container.innerHTML = '';

  if (totalPages <= 1) {
    return;
  }

  const prev = document.createElement('button');
  prev.textContent = '←';
  prev.disabled = RESULTS_STATE.currentPage === 1;
  prev.addEventListener('click', () => {
    RESULTS_STATE.currentPage -= 1;
    rerenderPage();
  });
  container.appendChild(prev);

  for (let i = 1; i <= totalPages; i++) {
    const btn = document.createElement('button');
    btn.textContent = i;

    if (i === RESULTS_STATE.currentPage) {
      btn.classList.add('active');
    }

    btn.addEventListener('click', () => {
      RESULTS_STATE.currentPage = i;
      rerenderPage();
    });

    container.appendChild(btn);
  }

  const next = document.createElement('button');
  next.textContent = '→';
  next.disabled = RESULTS_STATE.currentPage === totalPages;
  next.addEventListener('click', () => {
    RESULTS_STATE.currentPage += 1;
    rerenderPage();
  });
  container.appendChild(next);
}

function rerenderPage() {
  const start = (RESULTS_STATE.currentPage - 1) * RESULTS_STATE.perPage;
  const end = start + RESULTS_STATE.perPage;

  ORIGINAL_RENDER_RESULTS({
    total_matches: RESULTS_STATE.totalMatches,
    results: RESULTS_STATE.all.slice(start, end),
  });

  renderPagination(Math.ceil(RESULTS_STATE.all.length / RESULTS_STATE.perPage));
}

window.renderResults = function(data) {
  RESULTS_STATE.all = data.results || [];
  RESULTS_STATE.totalMatches = data.total_matches || RESULTS_STATE.all.length;
  RESULTS_STATE.currentPage = 1;
  RESULTS_STATE.perPage = Number(document.getElementById('top')?.value || 10);

  rerenderPage();
};
