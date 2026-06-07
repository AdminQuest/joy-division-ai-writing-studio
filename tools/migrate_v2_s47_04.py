#!/usr/bin/env python3
"""
Migration v2 — S47 (Mike West, Joy Division) — source_atomisation_04.md

Injecte les 9 champs v2 obligatoires dans chaque atome S47-161 à S47-200
et corrige les type_unite et statut invalides.

Approche : text-based (regex), sans re-sérialisation YAML.
"""

from __future__ import annotations

import re
from pathlib import Path

SOURCE_FILE = (
    Path(__file__).resolve().parents[1]
    / "sources"
    / "mike_west_joy_division"
    / "source_atomisation_04.md"
)

# ---------------------------------------------------------------------------
# Corrections de type_unite (valeurs globales, hors cas per-atome)
# ---------------------------------------------------------------------------
TYPE_MAP = {
    "lieu_biographique": "biographie",
    "lieu_scene": "sociologie",
    "lieu_archive": "archive",
    "lieu_bascule": "fait",
    "lieu_studio": "production",
    "lieu_radio": "archive",
    "lieu_terminal": "fait",
    "acteur_media": "reception",
    "acteur_scene": "fait",
    "acteur_critique": "reception",
    "acteurs_objet": "reception",
    "acteur_reprise": "reception",
    "micro_chronologie": "fait",
    "citation_repere": "citation_clef",
    "vigilance_erreur": "prudence_methodologique",
    "vigilance_ocr": "prudence_methodologique",
    "vigilance_actualisation": "prudence_methodologique",
    "vigilance_interpretative": "prudence_methodologique",
    "synthese_critique": "analyse",
    "synthese_documentaire": "analyse",
}

# Per-atome overrides pour type_unite (cas où la valeur dépend du contenu)
TYPE_MAP_PER_ATOM = {
    "S47-170": {"acteur": "reception"},   # Wilson : acteur-passeur médiatique
    "S47-171": {"acteur": "production"},  # Gretton : manager
    "S47-172": {"acteur": "production"},  # Hannett : producteur
    "S47-196": {"idee_directrice": "lecture"},
    "S47-197": {"idee_directrice": "reception"},
    "S47-198": {"idee_directrice": "lecture"},
}

# ---------------------------------------------------------------------------
# Corrections de statut
# ---------------------------------------------------------------------------
STATUT_MAP = {
    "interpretation": "a_consolider",
    "verifie_fragment": "a_verifier",
    "consolide": "a_consolider",
}

# ---------------------------------------------------------------------------
# Données v2 par atome
# ---------------------------------------------------------------------------
V2_DATA = {
    "S47-161": {
        "role_argumentatif": ["ancrer Macclesfield comme point géographique de départ biographique pour Curtis et Morris"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["macclesfield", "origines_biographiques", "ian_curtis", "stephen_morris"],
        "concepts_derives": ["geographie_personnelle"],
    },
    "S47-162": {
        "role_argumentatif": ["documenter Manchester comme infrastructure d'apprentissage musical collectif plutôt que simple décor"],
        "niveau_preuve": {"statut": "source_unique", "corroboration": "non_verifie", "confiance": "moyenne"},
        "stabilite": {"statut": "a_confirmer", "risque_revision": "moyen"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "moyenne"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["manchester", "scene_musicale", "apprentissage_collectif", "infrastructure_punk"],
        "concepts_derives": ["geographie_musicale"],
    },
    "S47-163": {
        "role_argumentatif": ["documenter l'Electric Circus comme lieu multifonctionnel : premier concert, fermeture symbolique, première trace discographique"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["electric_circus", "premier_concert", "short_circuit", "fermeture_symbolique"],
        "concepts_derives": ["lieu_archive_musical"],
    },
    "S47-164": {
        "role_argumentatif": ["situer Rafters comme scène de la rencontre décisive avec Gretton et Wilson, pivot managérial"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["rafters", "rob_gretton", "tony_wilson", "management", "stiff_chiswick_test"],
        "concepts_derives": ["bascule_manageriale"],
    },
    "S47-165": {
        "role_argumentatif": ["documenter Strawberry Studios comme lieu de l'alchimie sonore d'Unknown Pleasures sous Hannett"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["strawberry_studios", "martin_hannett", "unknown_pleasures", "production_sonore"],
        "concepts_derives": ["alchimie_sonore_factory"],
    },
    "S47-166": {
        "role_argumentatif": ["documenter Cargo Studios comme double seuil Factory : premiers titres puis session automne 1979"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["cargo_studios", "digital", "atmosphere", "dead_souls", "factory_records"],
        "concepts_derives": ["laboratoire_passages"],
    },
    "S47-167": {
        "role_argumentatif": ["situer Britannia Row comme espace de la réussite artistique ultime de Joy Division avec Closer"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["britannia_row", "closer", "tension_humaine", "derniere_mutation_sonore"],
        "concepts_derives": ["studio_terminal"],
    },
    "S47-168": {
        "role_argumentatif": ["établir les sessions Peel à Maida Vale comme corpus autonome, non secondaire, à traiter comme canon parallèle"],
        "niveau_preuve": {"statut": "source_unique", "corroboration": "non_verifie", "confiance": "moyenne"},
        "stabilite": {"statut": "a_confirmer", "risque_revision": "moyen"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "moyenne"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["maida_vale", "john_peel", "peel_sessions", "versions_alternatives", "canon_parallele"],
        "concepts_derives": ["corpus_radio_autonome"],
    },
    "S47-169": {
        "role_argumentatif": ["documenter le Birmingham University High Hall comme lieu du dernier concert et source live de Still"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["birmingham", "high_hall", "dernier_concert", "still", "2_mai_1980"],
        "concepts_derives": ["lieu_terminal_live"],
    },
    "S47-170": {
        "role_argumentatif": ["montrer l'évolution de Wilson de présentateur TV à architecte de l'écosystème Factory autour de Joy Division"],
        "niveau_preuve": {"statut": "source_unique", "corroboration": "non_verifie", "confiance": "moyenne"},
        "stabilite": {"statut": "a_confirmer", "risque_revision": "moyen"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "moyenne"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["tony_wilson", "factory_records", "television", "legitimation", "media"],
        "concepts_derives": ["acteur_passeur"],
    },
    "S47-171": {
        "role_argumentatif": ["définir Gretton comme membre non musicien élargissant le collectif Joy Division au-delà du quatuor"],
        "niveau_preuve": {"statut": "source_unique", "corroboration": "non_verifie", "confiance": "moyenne"},
        "stabilite": {"statut": "a_confirmer", "risque_revision": "moyen"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "moyenne"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["rob_gretton", "management", "collectif_elargi", "non_playing_member"],
        "concepts_derives": ["gouvernance_groupe"],
    },
    "S47-172": {
        "role_argumentatif": ["qualifier Hannett de cinquième membre de facto de Joy Division par son rôle de sculpteur sonore"],
        "niveau_preuve": {"statut": "source_unique", "corroboration": "non_verifie", "confiance": "moyenne"},
        "stabilite": {"statut": "a_confirmer", "risque_revision": "moyen"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "forte"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["martin_hannett", "production", "cinquieme_membre", "factory_sound"],
        "concepts_derives": ["producteur_comme_auteur"],
    },
    "S47-173": {
        "role_argumentatif": ["documenter le rôle multi-couche de Peel : enregistrement, diffusion, réception et annonce du décès de Curtis"],
        "niveau_preuve": {"statut": "source_unique", "corroboration": "non_verifie", "confiance": "moyenne"},
        "stabilite": {"statut": "a_confirmer", "risque_revision": "moyen"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "moyenne"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["john_peel", "peel_sessions", "festive_fifty", "radio_1", "mediateur_culturel"],
        "concepts_derives": ["acteur_media_central"],
    },
    "S47-174": {
        "role_argumentatif": ["situer Pete Shelley comme premier validateur punk de Warsaw puis contrepoint lors de la tournée Buzzcocks"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["pete_shelley", "buzzcocks", "warsaw", "punk", "validation_initiale"],
        "concepts_derives": ["pont_punk_postpunk"],
    },
    "S47-175": {
        "role_argumentatif": ["enregistrer la formulation critique précoce de Bell inscrivant Unknown Pleasures dans la généalogie des grands disques anglais"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["max_bell", "nme", "unknown_pleasures", "critique_musicale", "strange_days"],
        "concepts_derives": ["reception_critique_precoce"],
    },
    "S47-176": {
        "role_argumentatif": ["attester l'intérêt critique précoce de Savage autour de Digital et Unknown Pleasures en 1979"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["john_savage", "melody_maker", "digital", "unknown_pleasures", "critique_1979"],
        "concepts_derives": ["cartographie_critique_1979"],
    },
    "S47-177": {
        "role_argumentatif": ["affirmer avec Thrills que Joy Division dépasse les règles ordinaires du rock alternatif"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["adrian_thrills", "nme", "transmission", "factory", "reception_heroique"],
        "concepts_derives": ["depassement_regles_rock"],
    },
    "S47-178": {
        "role_argumentatif": ["illustrer la réception critique extrême et prométhéenne de Joy Division comme symptôme rhétorique à employer prudemment"],
        "niveau_preuve": {"statut": "source_unique", "corroboration": "non_verifie", "confiance": "faible"},
        "stabilite": {"statut": "a_confirmer", "risque_revision": "moyen"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "forte"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["neil_norman", "nme", "reception_extreme", "prometheen", "rhetorique_exces"],
        "concepts_derives": ["symptome_reception"],
    },
    "S47-179": {
        "role_argumentatif": ["documenter la réception sacralisante européenne de Sordide Sentimental comme projet d'art total autour d'Atmosphere et Dead Souls"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["sordide_sentimental", "atmosphere", "dead_souls", "art_total", "reception_europeenne"],
        "concepts_derives": ["sacralisation_europeenne"],
    },
    "S47-180": {
        "role_argumentatif": ["documenter comment la reprise par Grace Jones déplace Joy Division vers une esthétique cosmopolite dub/disco/art-pop"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["grace_jones", "shes_lost_control", "reprise", "dub", "disco", "cosmopolite"],
        "concepts_derives": ["migration_genre_musical"],
    },
    "S47-181": {
        "role_argumentatif": ["synthétiser les événements fondateurs 1976-1977 : choc punk, formation, premier concert, première trace discographique"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["chronologie", "1976", "1977", "sex_pistols", "electric_circus", "formation_groupe"],
        "concepts_derives": ["phase_fondatrice"],
    },
    "S47-182": {
        "role_argumentatif": ["synthétiser l'émergence de Joy Division en 1978 : identité, management, premier album, naissance de Factory"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["chronologie", "1978", "joy_division", "factory", "an_ideal_for_living", "management"],
        "concepts_derives": ["emergence_joy_division"],
    },
    "S47-183": {
        "role_argumentatif": ["synthétiser l'année pivot 1979 : Peel Sessions, Unknown Pleasures, Transmission, tournée Buzzcocks"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["chronologie", "1979", "unknown_pleasures", "transmission", "peel_sessions", "buzzcocks"],
        "concepts_derives": ["annee_pivot"],
    },
    "S47-184": {
        "role_argumentatif": ["synthétiser l'année tragique 1980 : Closer, mort de Curtis, publications posthumes, refus de continuer"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["chronologie", "1980", "closer", "ian_curtis", "mort", "new_order", "love_will_tear_us_apart"],
        "concepts_derives": ["annee_tragique"],
    },
    "S47-185": {
        "role_argumentatif": ["synthétiser la période 1981-1983 : New Order s'émancipe pendant que Joy Division devient culte"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["chronologie", "1981", "1983", "new_order", "still", "ceremony", "culte"],
        "concepts_derives": ["emancipation_new_order"],
    },
    "S47-186": {
        "role_argumentatif": ["ancrer la formule de Mick Middles comme titre structurant du chapitre 4 et évaluation précoce de Joy Division"],
        "niveau_preuve": {"statut": "source_unique", "corroboration": "non_verifie", "confiance": "faible"},
        "stabilite": {"statut": "a_confirmer", "risque_revision": "moyen"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "moyenne"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["mick_middles", "sounds", "citation_critique", "annees_1980", "groundwork"],
        "concepts_derives": ["citation_structurante"],
    },
    "S47-187": {
        "role_argumentatif": ["documenter la formule d'Ian Wood reliant le malaise urbain à la précision affective de Joy Division"],
        "niveau_preuve": {"statut": "source_unique", "corroboration": "non_verifie", "confiance": "faible"},
        "stabilite": {"statut": "a_confirmer", "risque_revision": "moyen"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "moyenne"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["ian_wood", "nme", "urban_malaise", "deadly_accurate", "manchester"],
        "concepts_derives": ["exactitude_affective"],
    },
    "S47-188": {
        "role_argumentatif": ["documenter la réception scénique de Curtis comme personnage du perdant crédible et vulnérable"],
        "niveau_preuve": {"statut": "source_unique", "corroboration": "non_verifie", "confiance": "faible"},
        "stabilite": {"statut": "a_confirmer", "risque_revision": "moyen"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "forte"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["ian_curtis", "nme", "loser", "scene", "vulnerabilite"],
        "concepts_derives": ["reception_scenique_curtis"],
    },
    "S47-189": {
        "role_argumentatif": ["documenter la filiation comparatiste de Max Bell entre Unknown Pleasures et Strange Days des Doors"],
        "niveau_preuve": {"statut": "source_unique", "corroboration": "non_verifie", "confiance": "faible"},
        "stabilite": {"statut": "a_confirmer", "risque_revision": "moyen"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "moyenne"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["max_bell", "unknown_pleasures", "strange_days", "the_doors", "filiation_comparatiste"],
        "concepts_derives": ["reception_comparatiste"],
    },
    "S47-190": {
        "role_argumentatif": ["documenter l'évaluation de Thrills légitimant Factory et Joy Division comme prétendants sérieux"],
        "niveau_preuve": {"statut": "source_unique", "corroboration": "non_verifie", "confiance": "faible"},
        "stabilite": {"statut": "a_confirmer", "risque_revision": "moyen"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["adrian_thrills", "nme", "transmission", "factory", "legitimation_critique"],
        "concepts_derives": ["legitimation_factory"],
    },
    "S47-191": {
        "role_argumentatif": ["enregistrer la formule extrême de Neil Norman comme symptôme de la réception prométhéenne de Joy Division"],
        "niveau_preuve": {"statut": "source_unique", "corroboration": "non_verifie", "confiance": "faible"},
        "stabilite": {"statut": "a_confirmer", "risque_revision": "moyen"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "forte"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["neil_norman", "nme", "dieu", "rhetorique_extreme", "prometheen"],
        "concepts_derives": ["reception_promethéenne"],
    },
    "S47-192": {
        "role_argumentatif": ["alerter sur l'erreur 'Saul Herzog' au lieu de Werner Herzog dans S47, imposant vérification avant toute citation"],
        "niveau_preuve": {"statut": "source_unique", "corroboration": "non_verifie", "confiance": "faible"},
        "stabilite": {"statut": "a_confirmer", "risque_revision": "forte"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["werner_herzog", "stroszek", "erreur_nom_propre", "vigilance_documentaire"],
        "concepts_derives": ["alerte_methodologique"],
    },
    "S47-193": {
        "role_argumentatif": ["signaler les scories typographiques et erreurs OCR dans S47, imposant vérification visuelle avant citation"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["ocr", "typographie", "erreur_mineure", "vigilance_documentaire"],
        "concepts_derives": ["regle_methode_s47"],
    },
    "S47-194": {
        "role_argumentatif": ["signaler que les statistiques de West reflètent un état de connaissance arrêté au début des années 1980"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["statistiques", "ventes", "1983", "actualisation_requise"],
        "concepts_derives": ["donnee_historique_datee"],
    },
    "S47-195": {
        "role_argumentatif": ["signaler la tension interne de S47 entre rhétorique de démystification et remythification simultanée"],
        "niveau_preuve": {"statut": "source_unique", "corroboration": "non_verifie", "confiance": "moyenne"},
        "stabilite": {"statut": "a_confirmer", "risque_revision": "moyen"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "forte"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["mythe", "demystification", "rhetorique_exception", "contradiction_source"],
        "concepts_derives": ["lecture_critique_s47"],
    },
    "S47-196": {
        "role_argumentatif": ["proposer la lecture de Closer comme commencement d'une phase artistique nouvelle immédiatement interrompue"],
        "niveau_preuve": {"statut": "source_unique", "corroboration": "non_verifie", "confiance": "moyenne"},
        "stabilite": {"statut": "a_confirmer", "risque_revision": "moyen"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "forte"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["closer", "commencement_interrompu", "lecture_non_teleologique", "futur_empeche"],
        "concepts_derives": ["axe_interpretatif"],
    },
    "S47-197": {
        "role_argumentatif": ["documenter que la canonisation de Joy Division est déjà rapide et contemporaine de New Order dès 1983"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["culte", "legende", "1983", "posterite", "reception_rapide"],
        "concepts_derives": ["canonisation_precoce"],
    },
    "S47-198": {
        "role_argumentatif": ["poser le garde-fou méthodologique contre la réduction de Joy Division à la seule figure de Curtis"],
        "niveau_preuve": {"statut": "source_unique", "corroboration": "non_verifie", "confiance": "moyenne"},
        "stabilite": {"statut": "a_confirmer", "risque_revision": "moyen"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "moyenne"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["ian_curtis", "collectif", "groupe", "sumner", "hook", "morris", "hannett"],
        "concepts_derives": ["collectivite_joy_division"],
    },
    "S47-199": {
        "role_argumentatif": ["synthétiser la valeur critique de S47 comme antidote partiel au romantisme morbide rappelant l'énergie et l'intégrité"],
        "niveau_preuve": {"statut": "source_unique", "corroboration": "non_verifie", "confiance": "moyenne"},
        "stabilite": {"statut": "a_confirmer", "risque_revision": "moyen"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "forte"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["romantisme_morbide", "demystification", "espoir", "integrite", "volonte"],
        "concepts_derives": ["antidote_romantisme"],
    },
    "S47-200": {
        "role_argumentatif": ["clôturer l'atomisation de S47 et définir ses conditions d'usage : archive de réception précoce à haute valeur contextuelle"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["atomisation", "mike_west", "reception_precoce", "archive", "methode"],
        "concepts_derives": ["cloture_atomisation_s47"],
    },
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

REQUIRED_FIELDS = [
    "role_argumentatif",
    "niveau_preuve",
    "stabilite",
    "importance",
    "risque_surinterpretation",
    "liens_interchapitres",
    "liens_citations",
    "motifs",
    "concepts_derives",
]

BLOCK_RE = re.compile(r"(```yaml\n)(.*?)(```)", re.DOTALL)


def extract_atom_id(block_body: str) -> str | None:
    m = re.search(r"^id:\s*(S47-\d+)\s*$", block_body, re.MULTILINE)
    if m:
        return m.group(1)
    return None


def fix_type_unite(block_body: str, atom_id: str) -> str:
    per_atom = TYPE_MAP_PER_ATOM.get(atom_id, {})
    combined = {**TYPE_MAP, **per_atom}

    def replacer(m):
        old_val = m.group(1)
        new_val = combined.get(old_val)
        if new_val:
            return f"type_unite: {new_val}"
        return m.group(0)

    return re.sub(r"^type_unite:\s*(\S+)\s*$", replacer, block_body, flags=re.MULTILINE)


def fix_statut(block_body: str) -> str:
    def replacer(m):
        old_val = m.group(1)
        new_val = STATUT_MAP.get(old_val)
        if new_val:
            return f"statut: {new_val}"
        return m.group(0)

    return re.sub(r"^statut:\s*(\S+)\s*$", replacer, block_body, flags=re.MULTILINE)


def render_v2_fields(data: dict) -> str:
    lines = []

    lines.append("role_argumentatif:")
    for item in data["role_argumentatif"]:
        lines.append(f'  - "{item}"')

    np = data["niveau_preuve"]
    lines.append("niveau_preuve:")
    lines.append(f"  statut: {np['statut']}")
    lines.append(f"  corroboration: {np['corroboration']}")
    lines.append(f"  confiance: {np['confiance']}")

    st = data["stabilite"]
    lines.append("stabilite:")
    lines.append(f"  statut: {st['statut']}")
    lines.append(f"  risque_revision: {st['risque_revision']}")

    lines.append("importance:")
    lines.append(f"  niveau: {data['importance']['niveau']}")

    lines.append("risque_surinterpretation:")
    lines.append(f"  niveau: {data['risque_surinterpretation']['niveau']}")

    if data["liens_interchapitres"]:
        lines.append("liens_interchapitres:")
        for item in data["liens_interchapitres"]:
            lines.append(f"  - {item}")
    else:
        lines.append("liens_interchapitres: []")

    if data["liens_citations"]:
        lines.append("liens_citations:")
        for item in data["liens_citations"]:
            lines.append(f"  - {item}")
    else:
        lines.append("liens_citations: []")

    lines.append("motifs:")
    for item in data["motifs"]:
        lines.append(f"  - {item}")

    lines.append("concepts_derives:")
    for item in data["concepts_derives"]:
        lines.append(f"  - {item}")

    return "\n".join(lines) + "\n"


def inject_v2_fields(block_body: str, v2_data: dict) -> str:
    missing = [f for f in REQUIRED_FIELDS if not re.search(rf"^{f}[:\s]", block_body, re.MULTILINE)]
    if not missing:
        return block_body
    body = block_body.rstrip("\n")
    body += "\n" + render_v2_fields(v2_data)
    return body


def migrate_content(content: str) -> tuple[str, int, list[str]]:
    atoms_modified = 0
    errors = []

    def process_block(m: re.Match) -> str:
        nonlocal atoms_modified

        opening = m.group(1)
        body = m.group(2)
        closing = m.group(3)

        atom_id = extract_atom_id(body)
        if atom_id is None:
            return m.group(0)

        if atom_id not in V2_DATA:
            errors.append(f"WARNING: {atom_id} has no V2_DATA entry — skipped")
            return m.group(0)

        new_body = body
        new_body = fix_type_unite(new_body, atom_id)
        new_body = fix_statut(new_body)
        new_body = inject_v2_fields(new_body, V2_DATA[atom_id])

        atoms_modified += 1
        return opening + new_body + closing

    new_content = BLOCK_RE.sub(process_block, content)
    return new_content, atoms_modified, errors


def main():
    print(f"Reading {SOURCE_FILE} ...")
    content = SOURCE_FILE.read_text(encoding="utf-8")

    new_content, count, errors = migrate_content(content)

    for err in errors:
        print(err)

    SOURCE_FILE.write_text(new_content, encoding="utf-8")
    print(f"Done. {count} atom(s) migrated to v2.")

    if errors:
        print(f"{len(errors)} warning(s) encountered.")


if __name__ == "__main__":
    main()
