#!/usr/bin/env python3
"""
Migration v2 — S71 (Flowers, Dreams Never End)

Injecte les 9 champs v2 obligatoires dans chaque atome S71-A*
et corrige les 9 type_unite invalides.

Approche : text-based (regex), sans re-sérialisation YAML.
"""

from __future__ import annotations

import re
from pathlib import Path

SOURCE_FILE = Path(__file__).resolve().parents[1] / "sources" / "flowers" / "source.md"

# ---------------------------------------------------------------------------
# Corrections de type_unite
# ---------------------------------------------------------------------------
TYPE_MAP = {
    "methode": "analyse",
    "contexte": "analyse",
    "chronologie": "fait",
    "management": "production",
}

# ---------------------------------------------------------------------------
# Données v2 par atome
# ---------------------------------------------------------------------------
V2_DATA = {
    "S71-A001": {
        "role_argumentatif": ["documenter la réception américaine comme entrée générationelle dans le corpus"],
        "niveau_preuve": {"statut": "source_unique", "corroboration": "non_verifie", "confiance": "faible"},
        "stabilite": {"statut": "a_confirmer", "risque_revision": "moyen"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "forte"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["reception_americaine", "new_wave_radio", "new_order", "joy_division_apres_coup"],
        "concepts_derives": ["entree_generationnelle"],
    },
    "S71-A002": {
        "role_argumentatif": ["documenter la posture d'écriture de Flowers comme fan documenté"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["fanzine", "biographie", "culture_fan", "enquete_amateur"],
        "concepts_derives": ["posture_fan_documente"],
    },
    "S71-A003": {
        "role_argumentatif": ["replacer l'enfance de Hook et Sumner dans le contexte industriel de Manchester"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["manchester", "declin_industriel", "enfance_ouvriere", "peter_hook", "bernard_sumner"],
        "concepts_derives": ["contexte_industriel_manchester"],
    },
    "S71-A004": {
        "role_argumentatif": ["documenter le concert des Sex Pistols comme déclencheur fondateur de la vocation musicale du groupe"],
        "niveau_preuve": {"statut": "source_unique", "corroboration": "non_verifie", "confiance": "faible"},
        "stabilite": {"statut": "a_confirmer", "risque_revision": "moyen"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "moyenne"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["sex_pistols", "free_trade_hall", "punk", "autorisation_musicale"],
        "concepts_derives": ["concert_fondateur"],
    },
    "S71-A005": {
        "role_argumentatif": ["documenter les origines autodidactes du groupe et l'achat des instruments"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["stiff_kittens", "apprentissage_autodidacte", "black_swan_pub", "instruments"],
        "concepts_derives": ["formation_groupe"],
    },
    "S71-A006": {
        "role_argumentatif": ["documenter l'écart culturel de Curtis et sa contribution littéraire au groupe"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "moyenne"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["ian_curtis", "culture_litteraire", "jg_ballard", "william_burroughs"],
        "concepts_derives": ["formation_intellectuelle"],
    },
    "S71-A007": {
        "role_argumentatif": ["documenter le premier concert et le changement de nom vers Warsaw"],
        "niveau_preuve": {"statut": "source_unique", "corroboration": "non_verifie", "confiance": "faible"},
        "stabilite": {"statut": "a_confirmer", "risque_revision": "moyen"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "moyenne"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["electric_circus", "warsaw", "tony_tabac", "buzzcocks", "paul_morley"],
        "concepts_derives": ["nom_groupe"],
    },
    "S71-A008": {
        "role_argumentatif": ["documenter la première perception de Gretton comme manager potentiel"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["rob_gretton", "rafters", "concert_sauvage", "decouverte_groupe"],
        "concepts_derives": ["decouverte_manageriale"],
    },
    "S71-A009": {
        "role_argumentatif": ["identifier le premier accomplissement artistique de Warsaw comme rupture avec la posture punk"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "moyenne"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["novelty", "maturite_artistique", "autoreflexivite", "cause_musicale"],
        "concepts_derives": ["premier_accomplissement_artistique"],
    },
    "S71-A010": {
        "role_argumentatif": ["documenter la première session en studio comme état sonore du groupe"],
        "niveau_preuve": {"statut": "source_unique", "corroboration": "non_verifie", "confiance": "faible"},
        "stabilite": {"statut": "a_confirmer", "risque_revision": "moyen"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["pennine_sound_studios", "premiere_demo", "one_take", "steve_brotherdale"],
        "concepts_derives": ["premiere_session_studio"],
    },
    "S71-A011": {
        "role_argumentatif": ["documenter la stabilisation du line-up avec l'arrivée de Stephen Morris"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["stephen_morris", "steve_brotherdale", "the_panik", "stabilisation_lineup"],
        "concepts_derives": ["recrutement_definitif"],
    },
    "S71-A012": {
        "role_argumentatif": ["documenter la naissance de la réputation d'ambiguïté politique du groupe"],
        "niveau_preuve": {"statut": "source_unique", "corroboration": "non_verifie", "confiance": "faible"},
        "stabilite": {"statut": "a_confirmer", "risque_revision": "moyen"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "forte"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["electric_circus", "rudolf_hess", "nazi_rumours", "short_circuit", "paul_morley"],
        "concepts_derives": ["ambiguite_politique"],
    },
    "S71-A013": {
        "role_argumentatif": ["proposer une lecture métaphorique du nom Joy Division comme exploitation industrielle"],
        "niveau_preuve": {"statut": "source_unique", "corroboration": "non_verifie", "confiance": "faible"},
        "stabilite": {"statut": "a_confirmer", "risque_revision": "moyen"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "forte"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["house_of_dolls", "joy_division_nom", "obscurite", "prostitution_metaphorique"],
        "concepts_derives": ["origine_nom_interpretation"],
    },
    "S71-A014": {
        "role_argumentatif": ["documenter la rencontre décisive avec Wilson et Gretton comme moment fondateur de l'alliance Factory"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["pips", "stiff_test", "tony_wilson", "rob_gretton", "rafters"],
        "concepts_derives": ["rencontre_fondatrice_factory"],
    },
    "S71-A015": {
        "role_argumentatif": ["documenter l'échec RCA et la récupération des bandes comme fondement de l'indépendance artistique"],
        "niveau_preuve": {"statut": "source_unique", "corroboration": "non_verifie", "confiance": "faible"},
        "stabilite": {"statut": "a_confirmer", "risque_revision": "moyen"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["rca_album", "derek_branwood", "interzone", "contrat_defavorable", "rob_gretton_manager"],
        "concepts_derives": ["independance_artistique"],
    },
    "S71-A016": {
        "role_argumentatif": ["documenter la naissance de l'identité Factory comme refus du modèle commercial"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["factory_club", "tony_wilson", "alan_erasmus", "peter_saville", "russell_club"],
        "concepts_derives": ["identite_factory"],
    },
    "S71-A017": {
        "role_argumentatif": ["documenter la lecture anti-fasciste du graphisme d'An Ideal for Living et ses malentendus"],
        "niveau_preuve": {"statut": "source_unique", "corroboration": "non_verifie", "confiance": "faible"},
        "stabilite": {"statut": "a_confirmer", "risque_revision": "moyen"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "forte"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["an_ideal_for_living", "enigma", "graphisme_fascisant", "anti_fascisme", "collector"],
        "concepts_derives": ["ambiguite_visuelle"],
    },
    "S71-A018": {
        "role_argumentatif": ["documenter la naissance sonore du label Factory et le rôle fondateur de Hannett"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["a_factory_sample", "martin_hannett", "digital", "glass", "factory_records"],
        "concepts_derives": ["son_factory"],
    },
    "S71-A019": {
        "role_argumentatif": ["documenter le lien entre performance scénique, épilepsie et réception du groupe à Londres"],
        "niveau_preuve": {"statut": "source_unique", "corroboration": "non_verifie", "confiance": "faible"},
        "stabilite": {"statut": "a_confirmer", "risque_revision": "moyen"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "moyenne"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["hope_and_anchor", "danse_de_curtis", "epilepsie", "shes_lost_control", "strobes"],
        "concepts_derives": ["maladie_et_performance"],
    },
    "S71-A020": {
        "role_argumentatif": ["documenter la Peel Session comme accès national et déploiement sonore sans ajouts RCA"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["john_peel", "bbc_radio_one", "peel_session", "transmission", "audience_nationale"],
        "concepts_derives": ["exposition_nationale"],
    },
    "S71-A021": {
        "role_argumentatif": ["documenter le choix Factory contre Warner comme stratégie fondatrice d'indépendance"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["martin_rushent", "genetic_records", "warner_brothers", "independance", "factory_records"],
        "concepts_derives": ["strategie_independance"],
    },
    "S71-A022": {
        "role_argumentatif": [
            "analyser Unknown Pleasures comme esthétique du désenchantement",
            "documenter la viabilité économique relative de Factory",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "moyenne"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["unknown_pleasures", "martin_hannett", "peter_saville", "pulsar", "desenchantement"],
        "concepts_derives": ["esthetique_desenchantement"],
    },
    "S71-A023": {
        "role_argumentatif": ["documenter la stratégie de silence médiatique comme posture d'autonomie du sens"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "moyenne"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["presse_musicale", "sens_ouvert", "refus_interviews", "autonomie_du_public"],
        "concepts_derives": ["strategie_mediatique"],
    },
    "S71-A024": {
        "role_argumentatif": ["documenter les jalons chronologiques de 1979 comme accumulation de tension physique"],
        "niveau_preuve": {"statut": "source_unique", "corroboration": "non_verifie", "confiance": "faible"},
        "stabilite": {"statut": "a_confirmer", "risque_revision": "moyen"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["piccadilly_radio", "granada_tv", "transmission", "nashville_club", "accident_de_van"],
        "concepts_derives": ["tension_tournee"],
    },
    "S71-A025": {
        "role_argumentatif": ["documenter la rareté des images filmées et leur rôle dans la construction du mythe"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["fac_9", "malcolm_whitehead", "plan_k", "here_are_the_young_men", "rarete_audiovisuelle"],
        "concepts_derives": ["mythe_image"],
    },
    "S71-A026": {
        "role_argumentatif": ["interpréter le choix du groupe vers la noirceur comme bifurcation esthétique délibérée"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "forte"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["transmission", "novelty", "autosuggestion", "from_safety_to_where", "darkness"],
        "concepts_derives": ["choix_esthetique_obscurite"],
    },
    "S71-A027": {
        "role_argumentatif": ["analyser la tension entre forme pop parfaite et contenu conjugal tragique"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "moyenne"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["love_will_tear_us_apart", "twenty_four_hours", "pop_parfaite", "mariage", "destin"],
        "concepts_derives": ["tension_pop_tragique"],
    },
    "S71-A028": {
        "role_argumentatif": ["documenter la convergence entre tournée européenne, relation amoureuse et dégradation de la santé de Curtis"],
        "niveau_preuve": {"statut": "source_unique", "corroboration": "non_verifie", "confiance": "faible"},
        "stabilite": {"statut": "a_confirmer", "risque_revision": "moyen"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "moyenne"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["tournee_europeenne", "annik_honore", "closer", "britannia_row", "sante_de_curtis"],
        "concepts_derives": ["crise_biographique"],
    },
    "S71-A029": {
        "role_argumentatif": ["lire Closer comme espace de renversement : Curtis guide de l'abîme au lieu d'être guidé"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "forte"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["closer", "atrocity_exhibition", "isolation", "passover", "decades"],
        "concepts_derives": ["inversion_identitaire"],
    },
    "S71-A030": {
        "role_argumentatif": ["documenter la tentative d'art total autour d'Atmosphere et Dead Souls et ses limites"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["sordide_sentimental", "licht_und_blindheit", "total_art", "atmosphere", "dead_souls"],
        "concepts_derives": ["art_total_discographique"],
    },
    "S71-A031": {
        "role_argumentatif": ["documenter la dégradation physique de Curtis sur scène comme insoutenabilité croissante"],
        "niveau_preuve": {"statut": "source_unique", "corroboration": "non_verifie", "confiance": "faible"},
        "stabilite": {"statut": "a_confirmer", "risque_revision": "moyen"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "moyenne"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["rainbow_theatre", "moonlight_club", "epilepsie", "sister_ray", "degradation_physique"],
        "concepts_derives": ["insoutenabilite_scenique"],
    },
    "S71-A032": {
        "role_argumentatif": ["documenter la convergence des projets printaniers 1980 et l'imminence de la rupture"],
        "niveau_preuve": {"statut": "source_unique", "corroboration": "non_verifie", "confiance": "faible"},
        "stabilite": {"statut": "a_confirmer", "risque_revision": "moyen"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["tournee_americaine_annulee", "ceremony", "in_a_lonely_place", "love_will_tear_us_apart_video", "tj_davidson"],
        "concepts_derives": ["projets_interrompus"],
    },
    "S71-A033": {
        "role_argumentatif": ["documenter les trois effets de la mort de Curtis : culte, annulation, nécessité de recommencer"],
        "niveau_preuve": {"statut": "source_unique", "corroboration": "non_verifie", "confiance": "faible"},
        "stabilite": {"statut": "a_confirmer", "risque_revision": "moyen"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "forte"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["mort_de_ian_curtis", "john_peel", "death_cult", "new_order", "rupture_continuite"],
        "concepts_derives": ["mythification_posthume"],
    },
    "S71-A034": {
        "role_argumentatif": ["documenter la réception posthume de LWTA et Closer comme problème éthique d'exploitation commerciale"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "moyenne"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["reception_posthume", "closer", "love_will_tear_us_apart", "peter_saville", "exploitation_commerciale"],
        "concepts_derives": ["industrie_post_mortem"],
    },
    "S71-A035": {
        "role_argumentatif": ["documenter New Order comme respect d'une promesse et impossible échappée de l'héritage Joy Division"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["new_order", "western_works", "beach_club", "situationnisme", "nom_du_groupe"],
        "concepts_derives": ["heritage_impossible"],
    },
    "S71-A036": {
        "role_argumentatif": ["documenter l'arrivée de Gillian Gilbert comme redistribution du deuil et des fonctions instrumentales"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["gillian_gilbert", "redistribution_instrumentale", "procession", "ceremony", "nouveau_depart"],
        "concepts_derives": ["transition_musicale"],
    },
    "S71-A037": {
        "role_argumentatif": ["juger Movement comme disque de transition inabouti encore prisonnier du son Joy Division"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "forte"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["movement", "martin_hannett", "heritage_joy_division", "voix_de_sumner", "rupture_difficile"],
        "concepts_derives": ["transition_musicale_inachevee"],
    },
    "S71-A038": {
        "role_argumentatif": ["identifier Temptation comme moment où Sumner rompt avec l'imitation de Curtis et trouve sa voix propre"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "moyenne"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["temptation", "taboo_number_7", "voix_de_sumner", "rupture_avec_joy_division", "spontaneite"],
        "concepts_derives": ["affranchissement_vocal"],
    },
    "S71-A039": {
        "role_argumentatif": ["documenter la Hacienda comme utopie institutionnelle et gouffre économique financé par New Order"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["hacienda", "factory_club", "ben_kelly", "economie_de_factory", "scene_mancunienne"],
        "concepts_derives": ["utopie_institutionnelle"],
    },
    "S71-A040": {
        "role_argumentatif": ["documenter Blue Monday comme rupture historique ouvrant un nouvel ordre de musique dance"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "moyenne"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["blue_monday", "dance_rock", "synthetiseur", "peter_saville", "hacienda"],
        "concepts_derives": ["musique_dance_rock"],
    },
    "S71-A041": {
        "role_argumentatif": ["documenter la maturité de Power, Corruption and Lies et son anti-commercialisme esthétique de surface"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["power_corruption_and_lies", "peter_saville", "code_couleur", "age_of_consent", "your_silent_face"],
        "concepts_derives": ["esthetique_anti_commerciale"],
    },
    "S71-A042": {
        "role_argumentatif": ["documenter le concert d'anniversaire Gretton comme geste de guérison publique"],
        "niveau_preuve": {"statut": "source_unique", "corroboration": "non_verifie", "confiance": "faible"},
        "stabilite": {"statut": "a_confirmer", "risque_revision": "moyen"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "moyenne"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["memoire_joy_division", "love_will_tear_us_apart", "rob_gretton", "healing"],
        "concepts_derives": ["memoire_collective"],
    },
    "S71-A043": {
        "role_argumentatif": ["documenter l'accord Qwest comme paradoxe d'indépendance sous licence d'une major"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["qwest", "quincy_jones", "warner_brothers", "licence_americaine", "controle_artistique"],
        "concepts_derives": ["independance_paradoxale"],
    },
    "S71-A044": {
        "role_argumentatif": ["lire Low-Life comme équilibre entre dance music, amour, douleur et mémoire de Curtis"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "moyenne"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["low_life", "elegia", "aids", "perfect_kiss", "love_vigilantes"],
        "concepts_derives": ["memoire_deuil_musical"],
    },
    "S71-A045": {
        "role_argumentatif": ["documenter le refus de jouer un rôle promotionnel comme constante d'intégrité de New Order"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["the_perfect_kiss_video", "jonathan_demme", "michael_shamberg", "refus_de_mimer", "integrite"],
        "concepts_derives": ["integrite_mediatique"],
    },
    "S71-A046": {
        "role_argumentatif": ["documenter le retour discographique de 1988 comme réouverture du culte de Curtis"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "forte"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["substance_joy_division", "atmosphere_video", "anton_corbijn", "peter_saville", "culte_de_curtis"],
        "concepts_derives": ["culte_posthume"],
    },
    "S71-A047": {
        "role_argumentatif": ["relier Technique à la culture acid house et au retour du geste de danser"],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [], "liens_citations": [],
        "motifs": ["technique", "acid_house", "ibiza", "hacienda", "ecstasy"],
        "concepts_derives": ["culture_dance"],
    },
}

# ---------------------------------------------------------------------------
# Rendering helpers
# ---------------------------------------------------------------------------

def render_v2_fields(data: dict) -> str:
    """Render the 9 v2 fields as YAML text (no leading newline, trailing newline)."""
    lines = []

    # role_argumentatif
    lines.append("role_argumentatif:")
    for item in data["role_argumentatif"]:
        lines.append(f'  - "{item}"')

    # niveau_preuve
    np = data["niveau_preuve"]
    lines.append("niveau_preuve:")
    lines.append(f"  statut: {np['statut']}")
    lines.append(f"  corroboration: {np['corroboration']}")
    lines.append(f"  confiance: {np['confiance']}")

    # stabilite
    st = data["stabilite"]
    lines.append("stabilite:")
    lines.append(f"  statut: {st['statut']}")
    lines.append(f"  risque_revision: {st['risque_revision']}")

    # importance
    lines.append("importance:")
    lines.append(f"  niveau: {data['importance']['niveau']}")

    # risque_surinterpretation
    lines.append("risque_surinterpretation:")
    lines.append(f"  niveau: {data['risque_surinterpretation']['niveau']}")

    # liens_interchapitres
    if data["liens_interchapitres"]:
        lines.append("liens_interchapitres:")
        for item in data["liens_interchapitres"]:
            lines.append(f"  - {item}")
    else:
        lines.append("liens_interchapitres: []")

    # liens_citations
    if data["liens_citations"]:
        lines.append("liens_citations:")
        for item in data["liens_citations"]:
            lines.append(f"  - {item}")
    else:
        lines.append("liens_citations: []")

    # motifs
    lines.append("motifs:")
    for item in data["motifs"]:
        lines.append(f"  - {item}")

    # concepts_derives
    lines.append("concepts_derives:")
    for item in data["concepts_derives"]:
        lines.append(f"  - {item}")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Core migration
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

# Matches a full ```yaml ... ``` block, capturing (prefix_before_closing_fence, atom_id_if_present)
# We'll process block by block using a split approach.

BLOCK_RE = re.compile(r"(```yaml\n)(.*?)(```)", re.DOTALL)


def extract_atom_id(block_body: str) -> str | None:
    """Return the atom id (e.g. S71-A001) if present in the block."""
    m = re.search(r"^id:\s*(S71-A\d+)\s*$", block_body, re.MULTILINE)
    if m:
        return m.group(1)
    return None


def fix_type_unite(block_body: str, atom_id: str) -> str:
    """Replace invalid type_unite values according to TYPE_MAP."""
    def replacer(m):
        old_val = m.group(1)
        new_val = TYPE_MAP.get(old_val)
        if new_val:
            return f"type_unite: {new_val}"
        return m.group(0)
    return re.sub(r"^type_unite:\s*(\S+)\s*$", replacer, block_body, flags=re.MULTILINE)


def inject_v2_fields(block_body: str, v2_data: dict) -> str:
    """
    Inject v2 fields at the end of the yaml block body (before the closing ```).
    Only inject fields that are not already present.
    """
    missing = [f for f in REQUIRED_FIELDS if not re.search(rf"^{f}[:\s]", block_body, re.MULTILINE)]
    if not missing:
        return block_body  # nothing to do

    # Render all v2 fields (we inject only the missing ones)
    rendered = render_v2_fields(v2_data)

    # Strip trailing newline from block_body so we can append cleanly
    body = block_body.rstrip("\n")
    body += "\n" + rendered
    return body


def migrate_content(content: str) -> tuple[str, int, list[str]]:
    """
    Process the full file content.
    Returns (new_content, atoms_modified_count, errors).
    """
    atoms_modified = 0
    errors = []

    def process_block(m: re.Match) -> str:
        nonlocal atoms_modified

        opening = m.group(1)   # "```yaml\n"
        body = m.group(2)       # yaml content
        closing = m.group(3)    # "```"

        atom_id = extract_atom_id(body)
        if atom_id is None:
            # Not an atom block (e.g. source metadata block) — leave unchanged
            return m.group(0)

        if atom_id not in V2_DATA:
            errors.append(f"WARNING: {atom_id} has no V2_DATA entry — skipped")
            return m.group(0)

        new_body = body

        # 1. Fix type_unite if needed
        new_body = fix_type_unite(new_body, atom_id)

        # 2. Inject v2 fields
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
