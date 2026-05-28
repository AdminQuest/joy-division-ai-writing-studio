/* Pictogrammes SVG inline par famille de lieu.
   24x24, trait fin 1.5, currentColor (stylé en ocre via le CSS).
   Un fallback "generic" (épingle de carte) couvre tout type inattendu. */
window.PlaceIcons = (() => {
  const S = body =>
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + body + '</svg>';

  const ICONS = {
    // ville — skyline (deux immeubles + fenêtres)
    ville: S('<path d="M3 21h18"/><path d="M6 21V6l6-3v18"/><path d="M12 21V10l6 3v8"/><path d="M9 8h.01M9 12h.01M9 16h.01"/>'),
    // quartier — grille de rues / îlots urbains
    quartier: S('<rect x="3" y="3" width="18" height="18" rx="1"/><path d="M3 9h18M3 15h18M9 3v18M15 3v18"/>'),
    // habitat — maison résidentielle
    habitat: S('<path d="M4 11 12 4l8 7"/><path d="M6 10v10h12V10"/><path d="M10 20v-5h4v5"/>'),
    // studio — console de mixage (faders)
    studio: S('<path d="M6 4v6M6 14v6M12 4v3M12 11v9M18 4v9M18 17v3"/><circle cx="6" cy="12" r="2"/><circle cx="12" cy="9" r="2"/><circle cx="18" cy="15" r="2"/>'),
    // salle — micro de scène
    salle: S('<rect x="9" y="2" width="6" height="11" rx="3"/><path d="M5 10v1a7 7 0 0 0 14 0v-1"/><path d="M12 18v3"/><path d="M8 21h8"/>'),
    // commerce — sac de courses / boutique
    commerce: S('<path d="M6 8h12l-1 12H7L6 8z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/>'),
    // education — livre ouvert
    education: S('<path d="M12 6c-2-1.3-4.5-2-7-2v13c2.5 0 5 .7 7 2 2-1.3 4.5-2 7-2V4c-2.5 0-5 .7-7 2z"/><path d="M12 6v13"/>'),
    // sante — croix médicale
    sante: S('<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M12 8v8M8 12h8"/>'),
    // industrie — cheminée d'usine + fumée
    industrie: S('<path d="M3 21V11l5 3V11l5 3V8l5-3v16z"/><path d="M3 21h18"/><path d="M18 5l.5-2"/>'),
    // science — atome
    science: S('<circle cx="12" cy="12" r="1.4"/><ellipse cx="12" cy="12" rx="9" ry="3.6"/><ellipse cx="12" cy="12" rx="9" ry="3.6" transform="rotate(60 12 12)"/><ellipse cx="12" cy="12" rx="9" ry="3.6" transform="rotate(120 12 12)"/>'),
    // infrastructure — pont suspendu
    infrastructure: S('<path d="M3 18h18"/><path d="M5 18V8M19 18V8"/><path d="M5 9c4 4 10 4 14 0"/><path d="M9 18v-5M12 18v-7M15 18v-5"/>'),
    // pouvoir — colonnes / bâtiment officiel
    pouvoir: S('<path d="M3 9l9-5 9 5"/><path d="M4 9h16"/><path d="M6 9v8M10 9v8M14 9v8M18 9v8"/><path d="M3 21h18"/>'),
    // lieu_memoire — stèle commémorative + croix
    lieu_memoire: S('<path d="M6 21V10a6 6 0 0 1 12 0v11"/><path d="M4 21h16"/><path d="M12 7.5v6"/><path d="M9.5 10.5h5"/>'),
    // fallback — épingle de carte
    generic: S('<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>')
  };

  // Libellés FR des sections / familles
  const LABELS = {
    ville: 'Villes', quartier: 'Quartiers', habitat: 'Habitat', studio: 'Studios',
    salle: 'Salles', commerce: 'Commerces', education: 'Lieux d’éducation',
    sante: 'Santé', industrie: 'Industrie', science: 'Sciences',
    infrastructure: 'Infrastructures', pouvoir: 'Pouvoir', lieu_memoire: 'Lieux de mémoire',
    generic: 'Autres lieux'
  };

  // Ordre d'affichage des sections
  const ORDER = ['ville','quartier','habitat','studio','salle','commerce','education',
                 'sante','industrie','science','infrastructure','pouvoir','lieu_memoire','generic'];

  const svg = type => ICONS[type] || ICONS.generic;
  const label = type => LABELS[type] || (type || 'Autres lieux');
  const order = ORDER;

  return { svg, label, order, LABELS };
})();
