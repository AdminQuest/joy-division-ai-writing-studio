/* Pictogrammes SVG inline par catégorie de chanson.
   24x24, trait fin 1.5, currentColor (stylé en bleu pétrole via le CSS).
   Chaque catégorie a un picto unique (lisibilité du groupage) ; un fallback
   "generic" (note simple) couvre toute catégorie inattendue.
   Clés = valeurs exactes de l'enum `category` du schéma public. */
window.SongIcons = (() => {
  const S = body =>
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + body + '</svg>';

  const ICONS = {
    // œuvre originale complète — disque vinyle entier (sillon + label + trou)
    'œuvre originale complète': S('<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3"/><circle cx="12" cy="12" r=".7" fill="currentColor" stroke="none"/>'),
    // Warsaw / pré-Joy Division — document épinglé (archive / source fixée)
    'Warsaw / pré-Joy Division': S('<rect x="5" y="6" width="14" height="15" rx="1.5"/><circle cx="12" cy="5" r="2.3"/><path d="M12 7.3v2"/><path d="M9 13h6M9 16h6M9 19h3"/>'),
    // Warsaw / live précoce — micro de scène
    'Warsaw / live précoce': S('<rect x="9" y="2" width="6" height="11" rx="3"/><path d="M5 10v1a7 7 0 0 0 14 0v-1"/><path d="M12 18v3"/><path d="M8 21h8"/>'),
    // démo / répétition — crayon d'esquisse (corps + virole + pointe)
    'démo / répétition': S('<path d="M4 20.5 5.5 15 15.4 5.1a2.1 2.1 0 0 1 3 3L8.5 18 3 19.5"/><path d="M13.5 6.5l3 3"/><path d="M5.5 15 8.5 18"/>'),
    // inédit / instrumental — portée + note (musique abstraite, sans paroles)
    'inédit / instrumental': S('<path d="M3 6.5h12M3 10h12M3 13.5h12M3 17h12"/><ellipse cx="15.7" cy="17" rx="2.3" ry="1.7"/><path d="M18 17V6"/><path d="M18 6c2.4.4 3.4 2 3.4 4"/>'),
    // terminal Joy Division / transition New Order — flèche franchissant un seuil
    'terminal Joy Division / transition New Order': S('<path d="M16 21V5a2 2 0 0 1 4 0v16"/><path d="M14 21h8"/><path d="M3 13h11"/><path d="M10 9l4 4-4 4"/>'),
    // fallback — note simple
    generic: S('<path d="M9 18V5l10-2v13"/><circle cx="6.5" cy="18" r="2.5"/><circle cx="16.5" cy="16" r="2.5"/>')
  };

  // Ordre d'affichage des sections (cœur canonique puis familles Warsaw, démos,
  // inédits, terminal). Les catégories inattendues sont rendues après, via generic.
  const ORDER = [
    'œuvre originale complète',
    'Warsaw / pré-Joy Division',
    'Warsaw / live précoce',
    'démo / répétition',
    'inédit / instrumental',
    'terminal Joy Division / transition New Order'
  ];

  const svg = category => ICONS[category] || ICONS.generic;
  const label = category => category || 'Autres';
  const order = ORDER;

  // Pictos compacts par release_type (page de détail → section "releases").
  // Clés = valeurs exactes du champ release_type de joy-division-releases.
  const RELEASE_ICONS = {
    officiel: S('<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3"/><circle cx="12" cy="12" r=".7" fill="currentColor" stroke="none"/>'),
    bootleg:  S('<rect x="9" y="2" width="6" height="11" rx="3"/><path d="M5 10v1a7 7 0 0 0 14 0v-1"/><path d="M12 18v3"/><path d="M8 21h8"/>'),
    pirate:   S('<path d="M3 7l9-4 9 4-9 4-9-4z"/><path d="M3 7v6l9 4 9-4V7"/><path d="M7 9v5"/>'),
    coffret:  S('<rect x="3" y="7" width="18" height="13" rx="1.5"/><path d="M3 11h18"/><path d="M9 7V4h6v3"/>'),
    livre:    S('<path d="M4 4h9a2 2 0 0 1 2 2v14a1.5 1.5 0 0 0-1.5-1.5H4z"/><path d="M20 4h-3a2 2 0 0 0-2 2v12.5A1.5 1.5 0 0 1 16.5 17H20z"/>'),
    video:    S('<rect x="3" y="6" width="13" height="12" rx="1.5"/><path d="M16 10l5-3v10l-5-3"/>'),
    para:     S('<path d="M20.6 13.3 13.3 20.6a2 2 0 0 1-2.8 0l-7-7V4h9.5l7.6 7.5a2 2 0 0 1 0 2.8z"/><circle cx="7.5" cy="7.5" r="1.3"/>')
  };
  const releaseSvg = type => RELEASE_ICONS[type] || ICONS.generic;
  const releaseLabel = type => type || 'autre';

  return { svg, label, order, releaseSvg, releaseLabel };
})();
