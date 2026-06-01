/* Pictogrammes SVG inline par catégorie d'acteur (registre PERSON-).
   24x24, trait fin 1.5, currentColor (stylé en bleu pétrole via le CSS).
   Miroir de apps/song-register/icons.js : un picto unique par catégorie pour la
   lisibilité du groupage, plus un fallback "generic". Clés = valeurs exactes de
   l'enum `categorie` du schéma canonique (schemas/person_canonical.schema.json). */
window.PeopleIcons = (() => {
  const S = body =>
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + body + '</svg>';

  const ICONS = {
    // membre du groupe — personne sur un piédestal (figure centrale du canon)
    membre: S('<circle cx="12" cy="7" r="3.2"/><path d="M6.5 20a5.5 5.5 0 0 1 11 0"/><path d="M5 20h14"/>'),
    // entourage — deux silhouettes proches (cercle intime, famille, proches)
    entourage: S('<circle cx="9" cy="8" r="2.6"/><path d="M4.5 19a4.5 4.5 0 0 1 9 0"/><circle cx="17" cy="9.5" r="2.1"/><path d="M15 19a4 4 0 0 1 6-3.2"/>'),
    // industrie — curseurs de console / faders (production, label, technique)
    industrie: S('<path d="M6 3v6M6 15v6"/><circle cx="6" cy="12" r="2.2"/><path d="M18 3v3M18 12v9"/><circle cx="18" cy="9" r="2.2"/>'),
    // critique / journaliste — plume sur feuille (presse, fanzine, chronique)
    critique_journaliste: S('<path d="M5 21l1-4L17 6a2.1 2.1 0 0 1 3 3L9 20l-4 1z"/><path d="M15 8l1 1"/><path d="M4.5 21H11"/>'),
    // auteur secondaire — livre ouvert (auteur d'une source du corpus)
    auteur_secondaire: S('<path d="M12 6.5C10.5 5 7.5 4.5 4 5v13c3.5-.5 6.5 0 8 1.5"/><path d="M12 6.5C13.5 5 16.5 4.5 20 5v13c-3.5-.5-6.5 0-8 1.5z"/><path d="M12 6.5v13"/>'),
    // influence — étoile rayonnante (figure littéraire/artistique citée)
    influence: S('<path d="M12 3.5l2.4 4.9 5.4.8-3.9 3.8.9 5.4-4.8-2.5-4.8 2.5.9-5.4-3.9-3.8 5.4-.8z"/>'),
    // théoricien mobilisé — buste + bulle d'idée (cadre conceptuel mobilisé)
    theoricien_mobilise: S('<circle cx="10" cy="8" r="3"/><path d="M4.5 20a5.5 5.5 0 0 1 11 0"/><circle cx="18.5" cy="6" r="2.5"/><path d="M16.8 7.7L15 9.5"/>'),
    // fallback — silhouette générique
    generic: S('<circle cx="12" cy="8" r="3.2"/><path d="M5.5 20a6.5 6.5 0 0 1 13 0"/>')
  };

  // Libellés lisibles des catégories (titres de section + facette).
  const LABELS = {
    membre: 'Membres',
    entourage: 'Entourage',
    industrie: 'Industrie',
    critique_journaliste: 'Critiques & journalistes',
    auteur_secondaire: 'Auteurs secondaires',
    influence: 'Influences',
    theoricien_mobilise: 'Théoriciens mobilisés'
  };

  // Ordre d'affichage des sections (consigne étape 9, point 5).
  const ORDER = [
    'membre',
    'entourage',
    'industrie',
    'critique_journaliste',
    'auteur_secondaire',
    'influence',
    'theoricien_mobilise'
  ];

  const svg = categorie => ICONS[categorie] || ICONS.generic;
  const label = categorie => LABELS[categorie] || categorie || 'Autres';
  const order = ORDER;

  return { svg, label, order };
})();
