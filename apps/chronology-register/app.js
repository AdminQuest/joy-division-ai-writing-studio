const timeline = document.getElementById('timeline');
const statusCard = document.getElementById('status-card');
const resultsMeta = document.getElementById('results-meta');

const searchInput = document.getElementById('search');
const yearFilter = document.getElementById('year-filter');
const typeFilter = document.getElementById('type-filter');
const locationFilter = document.getElementById('location-filter');
const sourceFilter = document.getElementById('source-filter');
const resetButton = document.getElementById('reset-filters');
const downloadButton = document.getElementById('download-csv');

let events = [];

function asText(value) {
  if (value === null || value === undefined) return '';
  return String(value);
}

function eventDate(item) {
  return asText(item?.data?.date);
}

async function loadChronology() {
  try {
    const response = await fetch('../../exports/generated/chronology.json');
    if (!response.ok) throw new Error(`chronology.json introuvable (${response.status})`);

    events = await response.json();

    events.sort((a, b) => eventDate(a).localeCompare(eventDate(b)));

    populateFilters();
    renderEvents(events);

    statusCard.textContent = `${events.length} événement(s) chargés`;
  } catch (error) {
    console.error(error);
    statusCard.textContent = `Erreur lors du chargement de la chronologie : ${error.message}`;
  }
}

function unique(values) {
  return [...new Set(values.map(asText).filter(Boolean))].sort();
}

function addOptions(select, values) {
  values.forEach(value => {
    const option = document.createElement('option');
    option.value = value;
    option.textContent = value;
    select.appendChild(option);
  });
}

function populateFilters() {
  addOptions(yearFilter, unique(events.map(e => eventDate(e).slice(0, 4))));
  addOptions(typeFilter, unique(events.map(e => e.data?.type)));
  addOptions(locationFilter, unique(events.map(e => e.data?.location)));

  const allSources = unique(
    events.flatMap(e => e.data?.sources || [])
  );

  addOptions(sourceFilter, allSources);
}

function renderEvents(items) {
  timeline.innerHTML = '';
  resultsMeta.textContent = `${items.length} résultat(s)`;

  items.forEach(item => {
    const data = item.data || {};
    const date = eventDate(item);

    const block = document.createElement('article');
    block.className = 'timeline-item';

    const people = (data.people || []).map(p => `<li>${asText(p)}</li>`).join('');
    const songs = (data.songs || []).map(s => `<li>${asText(s)}</li>`).join('');
    const sources = (data.sources || []).map(s => `<span class="badge">${asText(s)}</span>`).join('');

    block.innerHTML = `
      <div class="timeline-date">${date || 'Date inconnue'}</div>

      <div class="timeline-event">${data.event || ''}</div>

      <div class="timeline-meta">
        <span class="badge">${data.type || 'type inconnu'}</span>
        <span class="badge">${data.location || 'lieu inconnu'}</span>
        <span class="badge">${data.precision_date || 'précision inconnue'}</span>
        <span class="badge">certitude : ${data.certainty || 'non précisée'}</span>
      </div>

      <div class="timeline-meta">
        ${sources}
      </div>

      <div class="timeline-lists">
        <div>
          <h4>Personnes</h4>
          <ul>${people || '<li>—</li>'}</ul>
        </div>

        <div>
          <h4>Chansons</h4>
          <ul>${songs || '<li>—</li>'}</ul>
        </div>
      </div>
    `;

    timeline.appendChild(block);
  });
}

function filterEvents() {
  const query = searchInput.value.toLowerCase();
  const year = yearFilter.value;
  const type = typeFilter.value;
  const location = locationFilter.value;
  const source = sourceFilter.value;

  const filtered = events.filter(item => {
    const data = item.data || {};
    const date = eventDate(item);

    const haystack = [
      item.id,
      date,
      data.event,
      data.type,
      data.location,
      ...(data.people || []),
      ...(data.songs || []),
      ...(data.sources || [])
    ]
      .map(asText)
      .join(' ')
      .toLowerCase();

    const matchesQuery = !query || haystack.includes(query);
    const matchesYear = !year || date.startsWith(year);
    const matchesType = !type || data.type === type;
    const matchesLocation = !location || data.location === location;
    const matchesSource = !source || (data.sources || []).includes(source);

    return matchesQuery && matchesYear && matchesType && matchesLocation && matchesSource;
  });

  renderEvents(filtered);
}

function exportCSV() {
  const rows = [['id', 'date', 'event', 'type', 'location', 'people', 'songs', 'sources']];

  const visibleIds = [...document.querySelectorAll('.timeline-item')].map(item => {
    const date = item.querySelector('.timeline-date')?.innerText || '';
    const event = item.querySelector('.timeline-event')?.innerText || '';
    return { date, event };
  });

  visibleIds.forEach(({ date, event }) => {
    const match = events.find(item => eventDate(item) === date && (item.data?.event || '') === event);
    if (!match) return;
    const data = match.data || {};
    rows.push([
      match.id,
      eventDate(match),
      data.event,
      data.type,
      data.location,
      (data.people || []).join(' | '),
      (data.songs || []).join(' | '),
      (data.sources || []).join(' | ')
    ]);
  });

  const csv = rows
    .map(row => row.map(v => `"${String(v || '').replace(/"/g, '""')}"`).join(','))
    .join('\n');

  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);

  const link = document.createElement('a');
  link.href = url;
  link.download = 'registre_chronologique.csv';
  link.click();

  URL.revokeObjectURL(url);
}

[searchInput, yearFilter, typeFilter, locationFilter, sourceFilter]
  .forEach(el => el.addEventListener('input', filterEvents));

resetButton.addEventListener('click', () => {
  searchInput.value = '';
  yearFilter.value = '';
  typeFilter.value = '';
  locationFilter.value = '';
  sourceFilter.value = '';
  renderEvents(events);
});

downloadButton.addEventListener('click', exportCSV);

loadChronology();
