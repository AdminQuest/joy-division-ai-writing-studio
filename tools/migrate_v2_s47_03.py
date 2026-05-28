"""Migration v2 de source_atomisation_03.md (S47-113 → S47-160).

Ce script :
1. Corrige type_unite (valeurs invalides → schéma v2)
2. Corrige statut: interpretation → a_consolider
3. Ajoute les 9 champs v2 manquants avec contenu éditorial déduit du contexte

Règles : ne jamais modifier les champs existants (text, source_id, type, chapitres,
concepts, fiabilite, citation_directe, pages, auteur, titre).
"""

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Mapping type_unite invalide → valeur v2 valide
# ---------------------------------------------------------------------------
TYPE_MAP = {
    "objet_discographique": "production",
    "objet_factory": "production",
    "production_discographique": "production",
    "design_discographique": "esthétique",
    "production_album": "production",
    "single": "production",
    "objet_rare": "production",
    "collection": "culture_musicale",
    "collection_statistique": "culture_musicale",
    "genealogie_culturelle": "culture_musicale",
    "reprise_exterieure": "reception",
    "archive_inedite": "archive",
    "archive_live": "archive",
    "archive_video": "archive",
    "video": "archive",
    "index_chanson": "fait",
    "reception_chanson": "reception",
    "outtakes": "archive",
    "versions_chanson": "fait",
    "statistique_vente": "reception",
    "strategie_distribution": "production",
    "reception_radio": "reception",
    "reception_poll": "reception",
    "reception_commerciale": "reception",
    "reception_design": "reception",
    "reception_musiciens": "reception",
    "conclusion_methodologique": "analyse",
    "synthese_interpretative": "analyse",
}

# ---------------------------------------------------------------------------
# Champs v2 par atome : contenu éditorial déduit du contexte
# ---------------------------------------------------------------------------
V2_DATA = {
    "S47-113": {
        "role_argumentatif": [
            "documenter la première matérialité discographique du groupe",
            "illustrer la constitution précoce du marché collectionneur",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["ideal_for_living", "objet_rare", "enigma_records", "pochette_controverse"],
        "concepts_derives": ["marché_collectionneur", "rareté_discographique"],
    },
    "S47-114": {
        "role_argumentatif": [
            "montrer la réédition corrective comme stratégie identitaire",
            "documenter la trajectoire d'un objet devenu rare",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["ideal_for_living", "anonymous_records", "objet_rare", "redesign_pochette"],
        "concepts_derives": ["réédition", "rareté_discographique"],
    },
    "S47-115": {
        "role_argumentatif": [
            "ancrer l'entrée de Joy Division dans l'économie Factory",
            "documenter le premier objet Factory partagé entre groupes",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "critique"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["factory_sample", "fac2", "digital", "glass", "hannett", "cargo_studios"],
        "concepts_derives": ["économie_Factory", "objet_partagé"],
    },
    "S47-116": {
        "role_argumentatif": [
            "documenter les aléas artisanaux de la production Factory",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "probable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "mineur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["factory_sample", "pressage", "retard_production"],
        "concepts_derives": ["artisanat_Factory", "calendrier_production"],
    },
    "S47-117": {
        "role_argumentatif": [
            "documenter la genèse visuelle du pulsar comme icône",
            "établir la paternité créative de la pochette Saville/Albrecht",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "critique"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["unknown_pleasures", "peter_saville", "pulsar", "design_Factory", "ondes_radio"],
        "concepts_derives": ["design_Factory", "iconographie_scientifique"],
    },
    "S47-118": {
        "role_argumentatif": [
            "établir Hannett comme acteur créatif et non simple technicien",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["martin_hannett", "unknown_pleasures", "synthétiseur", "strawberry_studios"],
        "concepts_derives": ["rôle_créatif_hannett", "production_son"],
    },
    "S47-119": {
        "role_argumentatif": [
            "documenter la chronologie discographique des singles",
            "établir le rôle de Saville dans l'identité visuelle",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["transmission", "novelty", "fac13", "peter_saville", "chronologie_singles"],
        "concepts_derives": ["chronologie_discographique", "design_Factory"],
    },
    "S47-120": {
        "role_argumentatif": [
            "documenter le statut de rareté absolue d'un objet artistique",
            "ancrer l'esthétique européenne de Joy Division",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "critique"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["licht_und_blindheit", "atmosphere", "dead_souls", "sordide_sentimentale", "édition_limitée"],
        "concepts_derives": ["édition_d_art", "rareté_discographique", "esthétique_européenne"],
    },
    "S47-121": {
        "role_argumentatif": [
            "illustrer les formes éditoriales hybrides de l'indépendance britannique",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "probable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["earcom2", "bob_last", "fast_products", "objet_hybride", "indépendance_britannique"],
        "concepts_derives": ["format_hybride", "économie_indépendante"],
    },
    "S47-122": {
        "role_argumentatif": [
            "documenter la stratification matérielle des éditions Factory",
            "établir Still comme objet de collection dès sa sortie",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["still", "peter_saville", "édition_toile", "édition_limitée", "Factory"],
        "concepts_derives": ["stratification_éditoriale", "objet_de_collection"],
    },
    "S47-123": {
        "role_argumentatif": [
            "fournir une donnée quantitative de réception posthume",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["still", "charts", "album_posthume", "réception_commerciale"],
        "concepts_derives": ["réception_posthume", "performance_commerciale"],
    },
    "S47-124": {
        "role_argumentatif": [
            "illustrer la réactivité de Factory face aux dynamiques de marché",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["atmosphere", "she_s_lost_control", "distribution", "import_marché"],
        "concepts_derives": ["stratégie_distribution", "pression_importation"],
    },
    "S47-125": {
        "role_argumentatif": [
            "démontrer la patrimonialisation matérielle précoce de Joy Division",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["checklist_vinyle", "marché_collectionneur", "rareté", "1983"],
        "concepts_derives": ["patrimonialisation_précoce", "culture_collectionneur"],
    },
    "S47-126": {
        "role_argumentatif": [
            "montrer la continuité perçue entre Joy Division et New Order dans la culture collectionneuse",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "probable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "moyen"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["checklist_vinyle", "new_order", "ceremony", "everything_s_gone_green", "continuité"],
        "concepts_derives": ["continuité_Joy_Division_New_Order", "marché_collectionneur"],
    },
    "S47-127": {
        "role_argumentatif": [
            "documenter un détail matériel rare et recherché par les collectionneurs",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["short_circuit", "electric_circus", "vinyle_bleu", "édition_limitée"],
        "concepts_derives": ["vinyle_coloré", "objet_de_collection"],
    },
    "S47-128": {
        "role_argumentatif": [
            "ancrer Joy Division dans la séquence berlinoise et expérimentale de Bowie",
            "documenter une généalogie culturelle indirecte",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["bowie", "low", "warszawa", "warsaw", "influence_berlinoise"],
        "concepts_derives": ["généalogie_culturelle", "influence_bowie", "trilogie_berlinoise"],
    },
    "S47-129": {
        "role_argumentatif": [
            "documenter la première reprise externe d'un titre Joy Division",
            "signaler l'entrée du groupe dans l'esthétique post-disco et art-pop",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["grace_jones", "she_s_lost_control", "reprise", "island_records", "post_disco"],
        "concepts_derives": ["première_reprise", "circulation_répertoire", "diffusion_internationale"],
    },
    "S47-130": {
        "role_argumentatif": [
            "montrer la diffusion pop du répertoire Joy Division hors du cercle post-punk",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "probable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "moyen"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["paul_young", "love_will_tear_us_apart", "reprise_pop", "diffusion_mainstream"],
        "concepts_derives": ["diffusion_pop", "sortie_du_cercle_post_punk"],
    },
    "S47-131": {
        "role_argumentatif": [
            "documenter l'état des archives primitives Warsaw en 1983",
            "signaler un risque d'inexactitude à recouper",
        ],
        "niveau_preuve": {"statut": "fait_partiel", "corroboration": "incertaine", "confiance": "faible"},
        "stabilite": {"statut": "revision_probable", "risque_revision": "eleve"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "moyen"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["warsaw", "archive_studio", "enregistrements_1977", "inédit"],
        "concepts_derives": ["archive_primitive", "mémoire_discographique_incertaine"],
    },
    "S47-132": {
        "role_argumentatif": [
            "cartographier les titres finis restés inédits selon West en 1983",
        ],
        "niveau_preuve": {"statut": "fait_partiel", "corroboration": "probable", "confiance": "moyenne"},
        "stabilite": {"statut": "revision_probable", "risque_revision": "moyen"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "moyen"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["the_drawback", "exercise_one", "sound_of_music", "peel_session", "still"],
        "concepts_derives": ["état_archive_1983", "titres_inédits"],
    },
    "S47-133": {
        "role_argumentatif": [
            "signaler une piste majeure pour les archives live primitives de Warsaw",
        ],
        "niveau_preuve": {"statut": "fait_partiel", "corroboration": "incertaine", "confiance": "faible"},
        "stabilite": {"statut": "revision_probable", "risque_revision": "eleve"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "moyen"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["manor_mobile", "electric_circus", "warsaw", "at_a_later_date", "archive_live"],
        "concepts_derives": ["archive_live_primitive", "enregistrement_complet"],
    },
    "S47-134": {
        "role_argumentatif": [
            "documenter l'existence d'archives filmiques multiples comme base mémorielle",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "probable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["here_are_the_young_men", "films_8mm", "films_16mm", "archive_live", "Factory_video"],
        "concepts_derives": ["mémoire_audiovisuelle", "archive_filmique"],
    },
    "S47-135": {
        "role_argumentatif": [
            "recenser Here Are the Young Men comme document vidéo Factory fondateur",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "probable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["here_are_the_young_men", "Factory_video", "matériaux_live"],
        "concepts_derives": ["vidéogramme_Factory", "mémoire_audiovisuelle"],
    },
    "S47-136": {
        "role_argumentatif": [
            "cartographier les versions disponibles en 1983 pour un titre donné",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "mineur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["a_means_to_an_end", "closer", "still", "versions_studio_live"],
        "concepts_derives": ["cartographie_versions", "discographie_titre"],
    },
    "S47-137": {
        "role_argumentatif": [
            "documenter la logique du flexi gratuit comme objet périphérique Factory",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["incubation", "and_then_again", "komakino", "flexi", "objet_périphérique"],
        "concepts_derives": ["flexi_Factory", "face_cachée_discographie"],
    },
    "S47-138": {
        "role_argumentatif": [
            "tracer la trajectoire d'un morceau culte depuis la rareté absolue vers le canon officiel",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["dead_souls", "sordide_sentimentale", "still", "canonisation"],
        "concepts_derives": ["trajectoire_canonique", "rareté_vers_archive"],
    },
    "S47-139": {
        "role_argumentatif": [
            "suivre la réintégration des premiers titres dans le canon posthume",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["glass", "fac2", "still", "réintégration_canon"],
        "concepts_derives": ["réintégration_canon", "trajectoire_discographique"],
    },
    "S47-140": {
        "role_argumentatif": [
            "documenter un dialogue musical entre groupes mancuniens",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "incertaine", "confiance": "faible"},
        "stabilite": {"statut": "revision_probable", "risque_revision": "moyen"},
        "importance": {"niveau": "mineur"},
        "risque_surinterpretation": {"niveau": "eleve"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["heart_and_soul", "the_passage", "réponse_musicale", "manchester"],
        "concepts_derives": ["dialogue_inter_groupes", "scène_mancunienne"],
    },
    "S47-141": {
        "role_argumentatif": [
            "cartographier les sessions de mars 1980 et identifier les outtakes de Closer",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["the_only_mistake", "something_must_break", "closer", "britannia_row", "still"],
        "concepts_derives": ["outtakes_closer", "sessions_mars_1980"],
    },
    "S47-142": {
        "role_argumentatif": [
            "distinguer les versions d'un titre pour éviter les confusions éditoriales",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "probable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["sound_of_music", "peel_session", "version_studio_inédite", "still"],
        "concepts_derives": ["ambiguïté_versions", "archive_peel"],
    },
    "S47-143": {
        "role_argumentatif": [
            "établir un repère discographique simple pour un titre secondaire",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "mineur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["these_days", "love_will_tear_us_apart", "face_b", "single"],
        "concepts_derives": ["face_b", "repère_discographique"],
    },
    "S47-144": {
        "role_argumentatif": [
            "cartographier les morceaux écartés puis récupérés dans le canon posthume",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "probable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["walked_in_line", "outtake", "still", "unknown_pleasures_sessions"],
        "concepts_derives": ["morceaux_récupérés", "cartographie_outtakes"],
    },
    "S47-145": {
        "role_argumentatif": [
            "stabiliser la position d'un titre dans la discographie officielle",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "mineur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["wilderness", "unknown_pleasures", "album_track"],
        "concepts_derives": ["stabilité_discographique", "titre_album_exclusif"],
    },
    "S47-146": {
        "role_argumentatif": [
            "documenter la complexité des versions d'un titre central",
            "illustrer la circulation du répertoire Joy Division via les reprises",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["she_s_lost_control", "peel_session", "grace_jones", "versions_multiples"],
        "concepts_derives": ["multiplicité_versions", "circulation_répertoire"],
    },
    "S47-147": {
        "role_argumentatif": [
            "documenter Transmission comme titre pivot de la reconnaissance du groupe",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["transmission", "peel_session", "single", "still", "live_favori"],
        "concepts_derives": ["titre_pivot", "reconnaissance_nationale"],
    },
    "S47-148": {
        "role_argumentatif": [
            "structurer l'histoire du marché secondaire Joy Division dès 1983",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["disques_supprimés", "marché_secondaire", "ideal_for_living", "sordide_sentimentale"],
        "concepts_derives": ["marché_secondaire", "rareté_institutionnalisée"],
    },
    "S47-149": {
        "role_argumentatif": [
            "fournir la donnée commerciale majeure du catalogue Joy Division",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "critique"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["love_will_tear_us_apart", "ventes", "charts", "melody_maker"],
        "concepts_derives": ["performance_commerciale", "single_le_plus_vendu"],
    },
    "S47-150": {
        "role_argumentatif": [
            "quantifier la réception posthume de Closer et établir sa supériorité commerciale",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["closer", "charts", "meilleur_album", "réception_posthume"],
        "concepts_derives": ["performance_commerciale_posthume", "album_le_plus_vendu"],
    },
    "S47-151": {
        "role_argumentatif": [
            "proposer le Festive Fifty comme indicateur de popularité affective plus fiable que les charts",
        ],
        "niveau_preuve": {"statut": "interpretation_directe", "corroboration": "probable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "moyen"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["john_peel", "festive_fifty", "popularité_affective", "BBC"],
        "concepts_derives": ["popularité_cultuelle", "indicateur_alternatif"],
    },
    "S47-152": {
        "role_argumentatif": [
            "cartographier la hiérarchie affective des fans au début du culte Joy Division",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "critique"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["festive_fifty_1980", "atmosphere", "love_will_tear_us_apart", "transmission", "decades"],
        "concepts_derives": ["hiérarchie_affective_fans", "culte_Joy_Division"],
    },
    "S47-153": {
        "role_argumentatif": [
            "démontrer la continuité de réception entre Joy Division et New Order",
            "dater la cristallisation du culte Atmosphere",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "critique"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["festive_fifty_1981", "atmosphere", "ceremony", "new_order", "continuité_réception"],
        "concepts_derives": ["continuité_mémorielle", "atmosphere_culte"],
    },
    "S47-154": {
        "role_argumentatif": [
            "établir que la reconnaissance de Joy Division précède la mort de Curtis",
            "invalider l'hypothèse d'une célébrité uniquement posthume",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "critique"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["zigzag", "mai_1980", "reconnaissance_ante_mortem", "unknown_pleasures"],
        "concepts_derives": ["reconnaissance_ante_mortem", "réfutation_mythe_posthume"],
    },
    "S47-155": {
        "role_argumentatif": [
            "documenter la cristallisation mémorielle personnelle de Curtis dans la presse",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "probable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "moyen"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["nme_1980", "ian_curtis", "mythification", "sondage_presse"],
        "concepts_derives": ["canonisation_personnelle", "mémorielle_posthume"],
    },
    "S47-156": {
        "role_argumentatif": [
            "mesurer l'insertion rapide de Curtis dans une mémoire rock plus large",
            "situer Joy Division dans la postérité rock aux côtés de Lennon",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "verifiable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "critique"},
        "risque_surinterpretation": {"niveau": "faible"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["nme_1981", "ian_curtis", "john_lennon", "most_missed_person", "postérité_rock"],
        "concepts_derives": ["mémorielle_postérité", "icône_rock_perdude"],
    },
    "S47-157": {
        "role_argumentatif": [
            "montrer que l'objet visuel Factory continue de produire de la valeur symbolique",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "probable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "secondaire"},
        "risque_surinterpretation": {"niveau": "moyen"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["still", "pochette", "nme_poll", "peter_saville", "design_Factory"],
        "concepts_derives": ["valeur_symbolique_design", "réception_visuelle"],
    },
    "S47-158": {
        "role_argumentatif": [
            "renforcer la thèse du partenariat collectif au-delà de Curtis",
        ],
        "niveau_preuve": {"statut": "fait_documente", "corroboration": "probable", "confiance": "moyenne"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "majeur"},
        "risque_surinterpretation": {"niveau": "moyen"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["bernard_albrecht", "peter_hook", "stephen_morris", "new_order", "compétence_collective"],
        "concepts_derives": ["partenariat_collectif", "réception_instrumentale"],
    },
    "S47-159": {
        "role_argumentatif": [
            "définir la règle d'exploitation de S47 comme archive de réception",
            "prévenir les usages factuels non critiques de West",
        ],
        "niveau_preuve": {"statut": "interpretation_directe", "corroboration": "probable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "critique"},
        "risque_surinterpretation": {"niveau": "moyen"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["historiographie", "réception_critique", "usage_éditorial", "limites_source"],
        "concepts_derives": ["source_de_réception", "limite_factuelle", "usage_critique"],
    },
    "S47-160": {
        "role_argumentatif": [
            "formuler le positionnement critique de West entre culte et backlash",
            "cadrer l'usage du livre pour le projet éditorial",
        ],
        "niveau_preuve": {"statut": "interpretation_directe", "corroboration": "probable", "confiance": "forte"},
        "stabilite": {"statut": "stable", "risque_revision": "faible"},
        "importance": {"niveau": "critique"},
        "risque_surinterpretation": {"niveau": "moyen"},
        "liens_interchapitres": [],
        "liens_citations": [],
        "motifs": ["culte", "backlash", "hyperbole_morbide", "grandeur_musicale", "positionnement_critique"],
        "concepts_derives": ["contre_culte", "positionnement_anti_backlash", "défense_musicale"],
    },
}

# ---------------------------------------------------------------------------
# Statut interpretation → a_consolider
# ---------------------------------------------------------------------------
STATUT_FIX = {"interpretation": "a_consolider"}

# ---------------------------------------------------------------------------
# Patch YAML block
# ---------------------------------------------------------------------------

def render_list(values):
    if not values:
        return "[]\n"
    lines = ""
    for v in values:
        lines += f"  - {v}\n"
    return lines

def render_dict(d):
    lines = ""
    for k, v in d.items():
        lines += f"  {k}: {v}\n"
    return lines

def patch_yaml_block(block_text, atom_id):
    """Patch a YAML block string for the given atom_id."""
    lines = block_text.split("\n")
    new_lines = []

    for line in lines:
        # Fix type_unite
        if line.strip().startswith("type_unite:"):
            val = line.split(":", 1)[1].strip()
            if val in TYPE_MAP:
                line = f"type_unite: {TYPE_MAP[val]}"
        # Fix statut: interpretation
        if line.strip().startswith("statut:"):
            val = line.split(":", 1)[1].strip()
            if val in STATUT_FIX:
                line = f"statut: {STATUT_FIX[val]}"
        new_lines.append(line)

    result = "\n".join(new_lines)

    # Append v2 fields if atom has entry in V2_DATA
    v2 = V2_DATA.get(atom_id)
    if v2:
        extra = ""
        extra += "role_argumentatif:\n" + render_list(v2["role_argumentatif"])
        extra += "niveau_preuve:\n" + render_dict(v2["niveau_preuve"])
        extra += "stabilite:\n" + render_dict(v2["stabilite"])
        extra += "importance:\n" + render_dict(v2["importance"])
        extra += "risque_surinterpretation:\n" + render_dict(v2["risque_surinterpretation"])
        extra += "liens_interchapitres: " + ("[]\n" if not v2["liens_interchapitres"] else "\n" + render_list(v2["liens_interchapitres"]))
        extra += "liens_citations: " + ("[]\n" if not v2["liens_citations"] else "\n" + render_list(v2["liens_citations"]))
        extra += "motifs:\n" + render_list(v2["motifs"])
        extra += "concepts_derives:\n" + render_list(v2["concepts_derives"])
        # Remove trailing newline then add extra
        result = result.rstrip("\n") + "\n" + extra.rstrip("\n")

    return result


def process_file(path):
    content = Path(path).read_text()

    # Find and patch all yaml blocks
    pattern = re.compile(r"(```yaml\n)(.*?)(```)", re.DOTALL)

    def replace_block(m):
        prefix = m.group(1)
        block = m.group(2)
        suffix = m.group(3)

        # Find atom id
        id_match = re.search(r"^id:\s*(\S+)", block, re.MULTILINE)
        if not id_match:
            return m.group(0)

        atom_id = id_match.group(1)
        new_block = patch_yaml_block(block, atom_id)
        return prefix + new_block + "\n" + suffix

    new_content = pattern.sub(replace_block, content)
    Path(path).write_text(new_content)
    print(f"Migré: {path}")


if __name__ == "__main__":
    target = Path("/home/user/joy-division-ai-writing-studio/sources/mike_west_joy_division/source_atomisation_03.md")
    process_file(target)
    print("Migration terminée.")
