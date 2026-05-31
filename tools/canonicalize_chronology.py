#!/usr/bin/env python3
"""Étape 6 — brique d'identité de la chronologie : canonicalisation EVENT-,
réconciliation same_as, classification (categorie) et précision de date
(date_precision). STRICTEMENT ADDITIF — aucun identifiant legacy n'est renommé,
aucune donnée existante n'est réécrite ; on insère des champs optionnels.

Le travail est découpé en trois phases idempotentes (commits distincts) :

  --phase classification  -> insère `categorie` sur chaque entrée (500)
  --phase canon           -> écrit registers/chronology/events_canonical.md et
                             insère `same_as: EVENT-…` sur les entrées legacy
                             des jalons réconciliés
  --phase precision       -> insère `date_precision` (+ `date_debut`/`date_fin`
                             pour les intervalles) sur chaque entrée

Conformité :
- forme canonique EVENT-<SLUG> : sémantique (l'événement, pas le lieu),
  source-agnostique, SANS date dans l'ID (NAMING_CONVENTIONS §10.2) ;
- same_as porté par le legacy, pointant vers le canonique (cross_registres §1) ;
- seuls les JALONS reçoivent un EVENT- ; les concerts ordinaires gardent leur
  ID et migreront vers CONCERT- (étape 10) ; la réception posthume est relocalisée
  en étape 11.

Le détail des règles de classification et d'inférence de précision est documenté
dans docs/audits/audit_unitaire_chronologie_12b-3.md (§ post-canonicalisation).
"""
from __future__ import annotations

import argparse
import collections
import glob
import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
CHRONO_DIR = REPO / "registers" / "chronology"
CANON_FILE = CHRONO_DIR / "events_canonical.md"

# --------------------------------------------------------------------------- #
# Canonical jalons (hand-curated from the audit clusters). members = legacy ids
# reconciled by same_as toward the canonical. Sex Pistols : deux gigs distincts,
# désambiguïsés par qualificateur ORDINAL sémantique (jamais par date).
# --------------------------------------------------------------------------- #
CANON = {
    "EVENT-NAISSANCE-IAN-CURTIS": dict(
        date="1956-07-15", precision="jour",
        label="Naissance de Ian Curtis",
        members=["CHR-1956-001", "CHR-S76-1956-001"]),
    "EVENT-SEX-PISTOLS-LESSER-FREE-TRADE-HALL-PREMIER": dict(
        date="1976-06-04", precision="jour",
        label="Premier concert des Sex Pistols au Lesser Free Trade Hall",
        members=["CHR-1976-001", "CHR-S10-1976-001",
                 "CHR-S41-TL2-1976-06-04-LFTH",
                 "CHR-S41-1976-06-04-LESSER-FREE-TRADE-HALL"]),
    "EVENT-SEX-PISTOLS-LESSER-FREE-TRADE-HALL-SECOND": dict(
        date="1976-07-20", precision="jour",
        label="Second concert des Sex Pistols au Lesser Free Trade Hall",
        members=["CHR-S41-1976-07-20-SECOND-PISTOLS-LFTH",
                 "CHR-S45-1976-07-20-SEX-PISTOLS",
                 "CHR-S75-1976-002", "CHR-S76-1976-002"]),
    "EVENT-WARSAW-PREMIER-CONCERT-ELECTRIC-CIRCUS": dict(
        date="1977-05-29", precision="jour",
        label="Premier concert de Warsaw à l'Electric Circus",
        members=["CHR-S10-1977-001",
                 "CHR-S41-TL2-1977-05-29-FIRST-WARSAW-GIG-REVIEW",
                 "CHR-S41-1977-05-29-WARSAW-FIRST-GIG-ELECTRIC-CIRCUS",
                 "CHR-S45-1977-05-29-WARSAW-ELECTRIC-CIRCUS",
                 "CHR-S76-1977-003"]),
    "EVENT-PREMIER-CONCERT-JOY-DIVISION-PIPS": dict(
        date="1978-01-25", precision="jour",
        label="Premier concert sous le nom Joy Division (Pips)",
        members=["CHR-S10-1978-001",
                 "CHR-S41-1978-01-PIPS-FIRST-JOY-DIVISION-GIG",
                 "CHR-S41-TL3-1978-01-25-PIPS-JOY-DIVISION",
                 "CHR-S45-1978-01-25-PIPS-FIRST-JD",
                 "CHR-S76-1978-001"]),
    "EVENT-ARRIVEE-STEPHEN-MORRIS": dict(
        date="1977-08", precision="mois",
        label="Arrivée de Stephen Morris (batteur)",
        prudence=("S41 date l'arrivée à « 1977-08 » (mois), retenu comme date la "
                  "plus précise ; S45 ne donne que « 1977 » (année). "
                  "CHR-S35-P05-1977-ETE-001 (Morris voit l'annonce en vitrine de "
                  "Jones's) est un candidat-membre à arbitrer."),
        members=["CHR-S41-1977-08-STEVE-MORRIS-JOINS",
                 "CHR-S45-1977-STEPHEN-MORRIS-RECRUTEMENT"]),
    "EVENT-SORTIE-A-FACTORY-SAMPLE": dict(
        date="1979-01", precision="mois",
        label="Sortie de A Factory Sample (FAC 2)",
        members=["CHR-1979-001", "CHR-S41-1979-01-A-FACTORY-SAMPLE-RELEASE",
                 "CHR-S10-1978-006"]),
    "EVENT-SORTIE-UNKNOWN-PLEASURES": dict(
        date="1979-06-14", precision="jour",
        label="Sortie de l'album Unknown Pleasures (FACT 10)",
        prudence=("S41 porte deux entrées de sortie (1979-06 « critical acclaim » "
                  "et 1979-06-14 « FACT 10 release ») : duplication intra-source "
                  "réconciliée. Lecture critique de S34 conservée distincte "
                  "(reception_posthume)."),
        members=["CHR-1979-002",
                 "CHR-S41-1979-06-UP-RELEASE-CRITICAL-ACCLAIM",
                 "CHR-S41-1979-06-14-UP-FACT10-RELEASE",
                 "CHR-S75-1979-006"]),
    "EVENT-DERNIER-CONCERT-BIRMINGHAM": dict(
        date="1980-05-02", precision="jour",
        label="Dernier concert de Joy Division (Birmingham University)",
        members=["CHR-1980-002",
                 "CHR-S41-1980-05-02-BIRMINGHAM-HIGH-HALL-LAST-GIG",
                 "CHR-S45-1980-05-02-BIRMINGHAM-FINAL-GIG",
                 "CHR-S75-1980-008", "CHR-S76-1980-027"]),
    "EVENT-MORT-IAN-CURTIS": dict(
        date="1980-05-18", precision="jour",
        label="Mort de Ian Curtis",
        prudence=("Les entrées adjacentes du 16-18 mai (derniers jours, dernier "
                  "trajet, notification à Hook par la police, retour d'Annik "
                  "Honoré) sont conservées comme jalons-facettes distincts, non "
                  "fusionnés. CHR-S76-1980-031 (découverte du corps) est traité "
                  "comme la consignation S76 du décès."),
        members=["CHR-1980-003", "CHR-S41-1980-05-18-CURTIS-SUICIDE",
                 "CHR-S75-1980-009", "CHR-S76-1980-031"]),
    "EVENT-SORTIE-CLOSER": dict(
        date="1980-07-18", precision="jour",
        label="Sortie posthume de l'album Closer",
        members=["CHR-1980-004", "CHR-S41-1980-CLOSER-RELEASE-POSTHUMOUS"]),

    # --- 2e canonicalisation (étape 6, passe d'arbitrage) ----------------- #
    "EVENT-PREMIERES-DEMOS-WARSAW-PENNINE-SOUND": dict(
        date="1977-07-18", precision="jour",
        label="Premières démos de Warsaw à Pennine Sound Studios",
        members=["CHR-S41-1977-07-18-WARSAW-DEMO-PENNINE", "CHR-S75-1977-001",
                 "CHR-S76-1977-005"]),
    "EVENT-DERNIER-CONCERT-WARSAW-SWINGING-APPLE": dict(
        date="1977-12-31", precision="jour",
        label="Dernier concert sous le nom Warsaw (Swinging Apple, Liverpool)",
        members=["CHR-S41-TL2-1977-12-31-SWINGING-APPLE-LAST-WARSAW",
                 "CHR-S45-1977-12-31-SWINGING-APPLE"]),
    "EVENT-SESSIONS-RCA-ARROW-STUDIOS": dict(
        date="1978-05", precision="mois",
        label="Sessions de l'album avorté RCA / Arrow Studios",
        prudence=("Périmètre retenu : sessions d'enregistrement à Arrow Studios "
                  "pour RCA. Le contact RCA/Swan autour d'une reprise "
                  "(CHR-S41-1978-05-RCA-SWAN-INTERZONE) et l'accord de management "
                  "Gretton (CHR-S41-TL3-1978-05-GRETTON-MANAGER) sont des "
                  "événements distincts, non fusionnés ici."),
        members=["CHR-1978-001", "CHR-S41-1978-05-ARROW-STUDIOS-RCA",
                 "CHR-S41-TL3-1978-05-03-04-ARROW-STUDIOS", "CHR-S76-1978-005",
                 "CHR-S45-1978-04-RCA-ARROW", "CHR-S75-1978-006",
                 "CHR-S10-1978-003"]),
    "EVENT-DEBUT-TELEVISION-GRANADA-SHADOWPLAY": dict(
        date="1978-09-20", precision="jour",
        label="Débuts télévisés de Joy Division (Granada Reports, « Shadowplay »)",
        members=["CHR-S10-1978-005", "CHR-S41-1978-09-20-GRANADA-REPORTS-SHADOWPLAY",
                 "CHR-S41-TL3-1978-09-20-GRANADA-SHADOWPLAY",
                 "CHR-S45-1978-GRANADA-SHADOWPLAY"]),
    "EVENT-ENREGISTREMENT-A-FACTORY-SAMPLE-CARGO": dict(
        date="1978-10-11", precision="jour",
        label="Enregistrement de « Digital » et « Glass » (A Factory Sample, Cargo Studios)",
        members=["CHR-S41-TL3-1978-10-11-CARGO-FACTORY-SAMPLE", "CHR-S75-1978-007",
                 "CHR-S76-1978-016"]),
    "EVENT-COUVERTURE-NME-IAN-CURTIS": dict(
        date="1979-01-13", precision="jour",
        label="Ian Curtis en couverture du NME",
        members=["CHR-S45-1979-01-13-NME-COVER", "CHR-S75-1979-001"]),
    "EVENT-DIAGNOSTIC-EPILEPSIE-IAN-CURTIS": dict(
        date="1979-01-23", precision="jour",
        label="Diagnostic d'épilepsie de Ian Curtis",
        members=["CHR-S41-1979-01-23-EPILEPSY-DIAGNOSIS",
                 "CHR-S41-1979-01-23-CURTIS-EPILEPSY-DIAGNOSIS",
                 "CHR-S45-1979-01-23-SPECIALIST-EPILEPSY", "CHR-S76-1979-004"]),
    "EVENT-PREMIERE-PEEL-SESSION": dict(
        date="1979-01-31", precision="jour",
        label="Première John Peel Session de Joy Division",
        members=["CHR-S41-1979-01-31-FIRST-PEEL-SESSION", "CHR-S75-1979-002",
                 "CHR-S76-1979-006", "CHR-S45-1979-01-PEEL-SESSION-1"]),
    "EVENT-NAISSANCE-NATALIE-CURTIS": dict(
        date="1979-04-16", precision="jour",
        label="Naissance de Natalie Curtis",
        members=["CHR-S41-1979-04-16-NATALIE-CURTIS-BORN",
                 "CHR-S45-1979-04-16-NATALIE-BIRTH", "CHR-S76-1979-011"]),
    "EVENT-DEUXIEME-PEEL-SESSION": dict(
        date="1979-11-26", precision="jour",
        label="Deuxième John Peel Session de Joy Division",
        prudence=("Deux entrées S41 (session ; « Love Will Tear Us Apart » y est "
                  "enregistrée) — duplication intra-source réconciliée."),
        members=["CHR-S41-1979-11-26-SECOND-PEEL-SESSION",
                 "CHR-S41-1979-11-26-SECOND-PEEL-LWTUA"]),
    "EVENT-FETE-FACTORY-NOUVEL-AN": dict(
        date="1979-12-31", precision="jour",
        label="Fête Factory du Nouvel An (Oldham Street)",
        prudence=("Cadrages divergents du même soir : S41 le décrit comme une "
                  "fête Factory où Gretton tente de vendre des parts ; S76 le "
                  "présente comme le dernier réveillon de Ian Curtis."),
        members=["CHR-S41-1979-12-31-FACTORY-OFFICE-PARTY", "CHR-S76-1979-026"]),
    "EVENT-OVERDOSE-PHENOBARBITAL-IAN-CURTIS": dict(
        date="1980-04-07", precision="jour",
        label="Overdose de phénobarbital de Ian Curtis",
        members=["CHR-S45-1980-04-07-PHENOBARBITONE-OVERDOSE", "CHR-S75-1980-006"]),
    "EVENT-CONCERT-DERBY-HALL-BURY": dict(
        date="1980-04-08", precision="jour",
        label="Concert du Derby Hall, Bury (interrompu, état critique de Curtis)",
        members=["CHR-1980-001", "CHR-S45-1980-04-08-DERBY-HALL-BURY-RIOT"]),

    # --- 3e passe : B1 (singletons-ancres) + flags tranchés + B2 (clusters) --- #
    # Biographie / formation
    "EVENT-NAISSANCE-BERNARD-SUMNER": dict(
        date="1956-01-04", precision="jour", label="Naissance de Bernard Sumner",
        members=["CHR-S10-1956-001"]),
    "EVENT-NAISSANCE-PETER-HOOK": dict(
        date="1956-02-13", precision="jour", label="Naissance de Peter Hook",
        members=["CHR-S41-1956-HOOK-BIRTH-SALFORD"]),
    "EVENT-RENCONTRE-SUMNER-HOOK-SALFORD-GRAMMAR": dict(
        date="1967", precision="annee",
        label="Rencontre de Bernard Sumner et Peter Hook (Salford Grammar School)",
        prudence="Datation divergente : S41 « 1967 » ; S10 « début des années 1970 ».",
        members=["CHR-S41-1967-SALFORD-GRAMMAR-MEETS-SUMNER", "CHR-S10-1970S-002"]),
    "EVENT-MARIAGE-IAN-DEBORAH-CURTIS": dict(
        date="1975-08-23", precision="jour",
        label="Mariage de Ian Curtis et Deborah Woodruff",
        members=["CHR-S76-1975-001"]),
    "EVENT-RECRUTEMENT-IAN-CURTIS": dict(
        date="1976-12", precision="mois",
        label="Ian Curtis devient le chanteur du groupe",
        prudence="S10 situe le recrutement via une annonce déposée chez Virgin (fin 1976).",
        members=["CHR-S41-1976-12-CURTIS-JOINS", "CHR-S10-1976-003"]),
    # Nom
    "EVENT-CHANGEMENT-NOM-WARSAW-JOY-DIVISION": dict(
        date="1977-12", precision="mois",
        label="Changement de nom : Warsaw devient Joy Division",
        prudence="La collision avec « Warsaw Pakt » (CHR-S41-1977-WARSAW-PAKT-NAME-COLLISION) est la cause documentée du changement.",
        members=["CHR-S41-1977-JOY-DIVISION-NAME-STABILIZED",
                 "CHR-S45-1978-01-AN-IDEAL-NAME-CHANGE",
                 "CHR-S41-1977-WARSAW-PAKT-NAME-COLLISION"]),
    # Lieu de répétition
    "EVENT-INSTALLATION-TJ-DAVIDSONS": dict(
        date="1977", precision="annee",
        label="Installation du groupe à T. J. Davidson's (local de répétition)",
        members=["CHR-S41-1977-TJ-DAVIDSONS-PRACTICE-ROOM", "CHR-S76-1978-017"]),
    # Line-up
    "EVENT-DEPART-TONY-TABAC": dict(
        date="1977-06-25", precision="jour",
        label="Départ de Tony Tabac (batterie)",
        members=["CHR-S41-1977-06-25-TONY-TABAC-LAST-GIG"]),
    # An Ideal for Living
    "EVENT-ENREGISTREMENT-AN-IDEAL-FOR-LIVING": dict(
        date="1977-12", precision="mois",
        label="Enregistrement de l'EP An Ideal for Living (Pennine Sound)",
        members=["CHR-S41-1977-PENNINE-AN-IDEAL-SESSION", "CHR-S45-1977-12-PENNINE-AN-IDEAL",
                 "CHR-S41-TL2-1977-12-14-AN-IDEAL-SESSIONS", "CHR-S76-1977-010",
                 "CHR-S10-1978-004"]),
    "EVENT-SORTIE-AN-IDEAL-FOR-LIVING-7-POUCES": dict(
        date="1978-06-03", precision="jour",
        label="Sortie de An Ideal for Living, 7 pouces original (Enigma PSS 139)",
        members=["CHR-S41-TL3-1978-06-03-AN-IDEAL-SEVEN-INCH", "CHR-S75-1978-003"]),
    "EVENT-REEDITION-AN-IDEAL-FOR-LIVING-12-POUCES": dict(
        date="1978-10-10", precision="jour",
        label="Réédition de An Ideal for Living en 12 pouces (Anonymous ANON1)",
        members=["CHR-S41-TL3-1978-10-10-AN-IDEAL-TWELVE-INCH",
                 "CHR-S41-1978-06-AIL-12-INCH-RABID", "CHR-S75-1978-004",
                 "CHR-S76-1978-010"]),
    # Short Circuit
    "EVENT-ENREGISTREMENT-SHORT-CIRCUIT-ELECTRIC-CIRCUS": dict(
        date="1977-10-02", precision="jour",
        label="Captation pour Short Circuit (dernière soirée de l'Electric Circus)",
        members=["CHR-S41-1977-10-02-ELECTRIC-CIRCUS-SHORT-CIRCUIT",
                 "CHR-S41-TL2-1977-10-02-SHORT-CIRCUIT-COLD-ENTRY"]),
    "EVENT-SORTIE-SHORT-CIRCUIT-LIVE": dict(
        date="1978-06-09", precision="jour",
        label="Sortie de Short Circuit – Live at the Electric Circus",
        members=["CHR-S41-TL3-1978-06-09-SHORT-CIRCUIT"]),
    # Management / Factory
    "EVENT-ROB-GRETTON-DEVIENT-MANAGER": dict(
        date="1978-05", precision="mois",
        label="Rob Gretton devient le manager de Joy Division",
        members=["CHR-S41-TL3-1978-05-GRETTON-MANAGER", "CHR-S45-1978-GRETTON-MANAGER",
                 "CHR-S76-1978-007"]),
    "EVENT-PREMIERE-SOIREE-FACTORY": dict(
        date="1978-05-19", precision="jour",
        label="Première soirée Factory (Russell Club)",
        members=["CHR-S76-1978-013"]),
    # TV / radio
    "EVENT-SESSION-PICCADILLY-RADIO": dict(
        date="1979-06-04", precision="jour",
        label="Session Piccadilly Radio",
        members=["CHR-S41-1979-06-04-PICCADILLY-RADIO",
                 "CHR-S41-1979-06-PICCADILLY-RADIO-CHANCE-ATROCITY"]),
    "EVENT-TELEVISION-WHATS-ON-SHES-LOST-CONTROL": dict(
        date="1979", precision="annee",
        label="Enregistrement télévisé « She's Lost Control » (What's On / Granada)",
        members=["CHR-S41-1979-GRANADA-WHATS-ON-SLC"]),
    "EVENT-PERFORMANCE-BBC2-SOMETHING-ELSE": dict(
        date="1979-09", precision="mois",
        label="Performance BBC2 « Something Else » (« Transmission » / « She's Lost Control »)",
        prudence="Diffusion le 15 septembre 1979 (S76).",
        members=["CHR-S76-1979-016", "CHR-S75-1979-010"]),
    # Sessions d'enregistrement
    "EVENT-SESSIONS-UNKNOWN-PLEASURES-STRAWBERRY": dict(wave="b2",
        date="1979-04", precision="mois",
        label="Sessions d'enregistrement de Unknown Pleasures (Strawberry Studios)",
        members=["CHR-S41-1979-03-31-05-02-UP-STRAWBERRY",
                 "CHR-S41-1979-04-STRAWBERRY-UP-SESSIONS",
                 "CHR-S45-1979-04-UNKNOWN-PLEASURES-STRAWBERRY", "CHR-S75-1979-004",
                 "CHR-S76-1979-010", "CHR-S10-1979-002"]),
    "EVENT-SESSIONS-TRANSMISSION": dict(wave="b2",
        date="1979-07", precision="mois",
        label="Sessions d'enregistrement de « Transmission »",
        prudence="Deux studios : sessions Central Sound puis version single à Strawberry.",
        members=["CHR-S41-1979-07-CENTRAL-SOUND-TRANSMISSION",
                 "CHR-S41-1979-07-01-CENTRAL-SOUND-TRANSMISSION", "CHR-S75-1979-009",
                 "CHR-S41-1979-07-28-08-04-STRAWBERRY-TRANSMISSION"]),
    "EVENT-SESSIONS-LICHT-UND-BLINDHEIT": dict(wave="b2",
        date="1979-10", precision="intervalle", debut="1979-10", fin="1979-11",
        label="Sessions « Atmosphere » / « Dead Souls » (Licht und Blindheit, Cargo Studios)",
        members=["CHR-S41-1979-10-ATMOSPHERE-LICHT-UND-BLINDHEIT",
                 "CHR-S41-1979-10-11-CARGO-SORDIDE-ATMOSPHERE", "CHR-S75-1979-012",
                 "CHR-S76-1979-024"]),
    "EVENT-SESSIONS-CLOSER-BRITANNIA-ROW": dict(wave="b2",
        date="1980-03", precision="mois",
        label="Sessions d'enregistrement de Closer (Britannia Row Studios)",
        members=["CHR-S41-1980-CLOSER-BRITANNIA-ROW-SESSIONS",
                 "CHR-S45-1980-03-CLOSER-BRITANNIA-ROW", "CHR-S75-1980-004",
                 "CHR-S10-1980-002", "CHR-S76-1980-016"]),
    # Tournées
    "EVENT-TOURNEE-BUZZCOCKS": dict(wave="b2",
        date="1979", precision="annee",
        label="Tournée britannique des Buzzcocks (Joy Division en première partie)",
        members=["CHR-S45-1979-08-BUZZCOCKS-TOUR-DAY-JOB",
                 "CHR-S41-1979-BUZZCOCKS-TOUR-PROFESSIONAL",
                 "CHR-S45-1979-MOUNTFORD-HALL-BUZZCOCKS"]),
    "EVENT-TOURNEE-EUROPEENNE-1980": dict(wave="b2",
        date="1980-01", precision="mois",
        label="Tournée européenne de Joy Division",
        members=["CHR-S41-1980-01-EUROPEAN-TOUR-ANNIK",
                 "CHR-S45-1980-01-EUROPEAN-TOUR-DEPART", "CHR-S75-1980-002"]),
    # Santé
    "EVENT-TENTATIVE-SUICIDE-RETOUR-EUROPE": dict(wave="b2",
        date="1980-01", precision="mois",
        label="Tentative de suicide au retour de la tournée européenne (Pernod / couteau)",
        prudence="Datation divergente : S41/S45 « janvier 1980 » ; S75 « février 1980 ».",
        members=["CHR-S41-1980-POST-EUROPE-PERNOD-KNIFE", "CHR-S45-1980-01-RETURN-PERNOD-BIBLE",
                 "CHR-S75-1980-003"]),
    # Iconographie
    "EVENT-SEANCE-PHOTO-CUMMINS-PRINCESS-PARKWAY": dict(
        date="1979-01-06", precision="jour",
        label="Séance photo de Kevin Cummins (Princess Parkway)",
        members=["CHR-S41-1979-01-06-CUMMINS-PRINCESS-PARKWAY"]),
    "EVENT-SEANCE-PHOTO-CORBIJN": dict(
        date="1979-11", precision="mois",
        label="Première séance photo d'Anton Corbijn",
        members=["CHR-S41-1979-11-CORBIJN-PHOTO-SESSION"]),
    "EVENT-POCHETTE-CLOSER-STAGLIENO": dict(
        date="1980-03", precision="mois",
        label="Conception de la pochette de Closer (photographie de Staglieno, Saville)",
        members=["CHR-S76-1980-019", "CHR-S41-1980-SAVILLE-STAGLIENO-CLOSER-LWTUA"]),
    "EVENT-TOURNAGE-VIDEO-LOVE-WILL-TEAR-US-APART": dict(
        date="1980-04", precision="mois",
        label="Tournage de la vidéo « Love Will Tear Us Apart » (T. J. Davidson's)",
        members=["CHR-S45-1980-04-25-LWTUA-VIDEO", "CHR-S41-1980-04-MAY-LWTUA-VIDEO-TJ-DAVIDSONS"]),
    # Funérailles
    "EVENT-FUNERAILLES-IAN-CURTIS": dict(
        date="1980-05", precision="mois",
        label="Funérailles et crémation de Ian Curtis",
        prudence="Crémation le 23 mai 1980 (S76) ; wake Factory à Palatine Road.",
        members=["CHR-S41-1980-05-FUNERAL-AND-WAKE", "CHR-S76-1980-033"]),

    # --- Clôture du socle (étape 6) : derniers flags ---------------------- #
    # B1 — clusters denses 1979-10 / LWTUA
    "EVENT-SORTIE-FAC13-TRANSMISSION": dict(
        date="1979-10", precision="mois",
        label="Sortie du single « Transmission » / « Novelty » (FAC 13)",
        prudence=("Seule mention legacy : une entrée-résumé d'octobre 1979 "
                  "(CHR-S41-1979-10-EARCOM-FAC13-SORDIDE-BUZZCOCKS) couvrant aussi "
                  "Earcom 2, Sordide Sentimental et le début de tournée Buzzcocks ; "
                  "rattachée ici à FAC 13 comme sortie dominante (membership mince)."),
        members=["CHR-S41-1979-10-EARCOM-FAC13-SORDIDE-BUZZCOCKS"]),
    "EVENT-SORTIE-EARCOM-2": dict(
        date="1979-10", precision="mois",
        label="Parution de « Autosuggestion » / « From Safety to Where…? » sur Earcom 2",
        members=["CHR-S75-1979-007"]),
    "EVENT-ENREGISTREMENT-LOVE-WILL-TEAR-US-APART": dict(
        date="1980-01", precision="intervalle", debut="1980-01", fin="1980-03",
        label="Enregistrement et mixage de « Love Will Tear Us Apart »",
        prudence=("Version Pennine initiale (janvier) puis reprise et mix à "
                  "Strawberry (mars) ; le tournage vidéo est un événement distinct."),
        members=["CHR-S41-1980-LWTUA-PENNINE-STRAWBERRY-MIX", "CHR-S76-1980-002",
                 "CHR-S76-1980-013"]),
    # B2 — composantes non-concert des bundles
    "EVENT-PREMIERE-CRISE-EPILEPTIQUE-IAN-CURTIS": dict(
        date="1978-12-27", precision="jour",
        label="Première crise épileptique majeure de Ian Curtis (retour du Hope & Anchor)",
        prudence=("Composante non-concert du bundle du 27/12/1978 ; la composante "
                  "concert (premier concert londonien) reste résiduelle, taguée "
                  "a_scinder_etape_10."),
        members=["CHR-1978-002", "CHR-S41-1978-12-M1-LUTON-FIRST-FIT",
                 "CHR-S45-1978-12-27-HOPE-AND-ANCHOR-FIRST-FIT", "CHR-S75-1978-008",
                 "CHR-S76-1978-019", "CHR-S10-1978-007"]),
    "EVENT-RENCONTRE-ANNIK-HONORE": dict(
        date="1979-08-13", precision="jour",
        label="Entrée d'Annik Honoré dans l'entourage de Joy Division (Nashville Rooms)",
        prudence=("Composante non-concert du bundle du 13/08/1979 ; la composante "
                  "concert reste résiduelle, taguée a_scinder_etape_10."),
        members=["CHR-S41-1979-08-13-NASHVILLE-ANNIK",
                 "CHR-S41-1979-08-13-NASHVILLE-ANNIK-ATMOSPHERE", "CHR-S76-1979-019"]),
    "EVENT-CRISE-RAINBOW-THEATRE": dict(
        date="1980-04-04", precision="jour",
        label="Crise de Ian Curtis au Rainbow Theatre (stroboscopes)",
        prudence=("Composante non-concert du bundle du 04/04/1980 ; la composante "
                  "concert reste résiduelle, taguée a_scinder_etape_10."),
        members=["CHR-S41-1980-04-04-RAINBOW-FIT-MOONLIGHT-INSISTENCE",
                 "CHR-S75-1980-005"]),
    "EVENT-DEMOS-GENETIC-EDEN-STUDIOS": dict(
        date="1979-03-04", precision="jour",
        label="Démos pour Genetic à Eden Studios (Martin Rushent)",
        prudence=("Composante non-concert du bundle du 04/03/1979 ; la composante "
                  "concert (gig au Marquee, CHR-S41-1979-03-04-EDEN-GENETIC-MARQUEE) "
                  "reste résiduelle, taguée a_scinder_etape_10."),
        members=["CHR-S41-1979-03-04-EDEN-GENETIC-MARQUEE", "CHR-S75-1979-003",
                 "CHR-S76-1979-007", "CHR-S41-1979-EDEN-STUDIOS-RUSHENT-DEMOS"]),
    # B3 — genèse du duo
    "EVENT-GENESE-DUO-SUMNER-HOOK": dict(
        date="1976", precision="annee",
        label="Bernard Sumner et Peter Hook commencent à jouer ensemble (genèse du groupe)",
        members=["CHR-S10-1976-002"]),
}

# id legacy -> canonique
MEMBER_TO_CANON = {m: c for c, d in CANON.items() for m in d["members"]}

# --------------------------------------------------------------------------- #
# Classification (categorie) — règles documentées dans l'audit.
# --------------------------------------------------------------------------- #
URBAN_CONTEXT_SOURCES = {"S02", "S05", "S06", "S12", "S20"}
RECEPTION_SOURCES = {"S29", "S34"}
_milestone = re.compile(
    r"sex pistols|lesser free trade hall|premier concert|first gig|dernier concert|"
    r"last gig|avant-dernier|derni[eè]re soir|farewell|sous le nom joy division|"
    r"premier .*joy division|first .*joy division|dernier .*warsaw|last .*warsaw", re.I)
_notperf = re.compile(
    r"\b(fit|crise|overdose|van|accident|article|mentionne|presse|review|sounds|nme|"
    r"enregistre|enregistrement|session|sortie|publication|signe|signature|emprunte|"
    r"ach[eè]te|d[eé]m[eé]nage|assiste|assistent|voit|se rend)\b", re.I)
_perf = re.compile(r"\b(joue|jouent)\b|\bconcert (de|du|au|à|des|sous)\b|^concert\b", re.I)


def source_of(rid):
    m = re.match(r"CHR-(S\d+)", rid)
    return m.group(1) if m else "MASTER"


def year_of(date, rid):
    m = re.search(r"(\d{4})", date) or re.search(r"-(\d{4})", rid)
    return int(m.group(1)) if m else None


def classify(rid, date, event, certainty, types):
    """Return (categorie, flag_or_None). Members of a canonical jalon are forced
    jalon (identity overrides heuristic)."""
    if rid in MEMBER_TO_CANON:
        return "jalon", None
    src = source_of(rid)
    cert = (certainty or "").lower()
    if src in RECEPTION_SOURCES or cert.startswith("interpretation") or "source_secondaire" in cert:
        return "reception_posthume", None
    y = year_of(date, rid)
    if y and y > 1980:
        return "reception_posthume", None
    if src == "MASTER":
        return "jalon", None
    if src in URBAN_CONTEXT_SOURCES:
        return "jalon", "context_urbain"
    is_perf = ("concert" in (types or "")) or bool(_perf.search(event or ""))
    is_mile = bool(_milestone.search(event or "") or _milestone.search(rid))
    if is_perf and _notperf.search(event or ""):
        return "jalon", "perf_mixte"
    if is_perf and not is_mile:
        return "concert_a_migrer", None
    if is_perf and is_mile:
        return "jalon", "jalon_concert_significatif"
    return "jalon", None


# --------------------------------------------------------------------------- #
# Reclassements (passe d'arbitrage) — décisions validées, appliquées par
# --phase reclassify. Réécrit la valeur de `categorie` (jamais en double).
#  (a) context_urbain -> nouvelle catégorie `contexte` (dérivé du flag) ;
#  (b)/(c) basculement explicite vers concert_a_migrer, entrée par entrée.
# Les entrées NON listées ici restent dans leur catégorie courante (jalon).
# --------------------------------------------------------------------------- #
CATEGORIES = ("jalon", "concert_a_migrer", "reception_posthume", "contexte")

# (b) perf_mixte -> concert_a_migrer : gigs ordinaires (la remarque accolée
#     ne porte pas un fait marquant distinct).
PERF_TO_CONCERT = {
    "CHR-S41-1977-09-14-MIDDLESBROUGH-BOB-LAST",
    "CHR-S41-1979-08-02-YMCA-LONDON",
    "CHR-S41-1979-10-03-LEEDS-UNIVERSITY-BUZZCOCKS",
    "CHR-S41-1979-10-16-PLAN-K-BRUSSELS",
    "CHR-S45-1978-11-CHECK-INN-ALTRINCHAM",
    "CHR-S45-1980-04-02-04-MOONLIGHT-RAINBOW",
    "CHR-S76-1978-011",
    "CHR-S76-1976-003",
}
# (c) jalon_concert_significatif -> concert_a_migrer : simple proximité ordinale,
#     pas de transition de signification réelle (décisions validées).
SIG_TO_CONCERT = {
    "CHR-S41-1980-04-19-DERBY-AJANTA-ANNIK",
    "CHR-S41-1976-12-09-ELECTRIC-CIRCUS-HATE-COAT",
    "CHR-S41-1978-01-03-PIPS-AFTERGAP",
    "CHR-S41-TL2-1977-06-SQUAT-SEQUENCE",
}


# (A3b) concerts d'autres artistes auxquels assiste un membre (JD/Warsaw ne joue
#       pas) : repères formatifs -> contexte.
ATTEND_OTHERS_TO_CONTEXTE = {
    "CHR-S10-1974-001",        # Sumner voit Lou Reed
    "CHR-S35-P03-1972-001",    # Morris voit Hawkwind
    "CHR-S35-P03-1972-002",    # Morris voit Bowie
    "CHR-S35-P05-1977-05-26",  # Morris voit Television & Blondie
    "CHR-S76-1972-002",        # Curtis voit Bowie
    "CHR-S76-1977-001",        # Curtis voit Iggy Pop
}

# (B1) singletons captés par le filtre d'ancre mais en fait CONTEXTUELS : sorties
#      / faits d'autres artistes servant de repère + flags tranchés -> contexte.
CONTEXTE_B1 = {
    "CHR-S35-P03-1972-003",    # sortie Ziggy Stardust (Bowie)
    "CHR-S35-P05-1977-01-001", # sortie Low (Bowie)
    "CHR-S41-TL2-1977-01-29-SPIRAL-SCRATCH",  # sortie Spiral Scratch (Buzzcocks)
    "CHR-S41-TL2-1976-12-01-GRUNDY-ANARCHY",  # épisode Grundy / Sex Pistols
    "CHR-S41-TL2-1977-11-PANIK-RAINY-CITY",   # sortie Panik / Rainy City
    "CHR-S45-1976-08-MONT-DE-MARSAN",         # festival Mont de Marsan
    "CHR-S10-1970-001",        # mort de Jimi Hendrix
    "CHR-S35-P05-1975-002",    # Reading Festival 1975
    "CHR-S35-P05-1976-001",    # Pistols à la TV (So It Goes)
    # B3 (clôture) : Manchester Musicians' Collective -> contexte (scène, non-jalon).
    "CHR-S41-1978-SUMMER-MUSICIANS-COLLECTIVE",
    "CHR-S45-1978-BAND-ON-THE-WALL-COLLECTIVE",
}


def reclass_target(rid, date, event, cert, types):
    """Nouvelle catégorie si l'entrée est reclassée, sinon None (inchangée)."""
    cat, flag = classify(rid, date, event, cert, types)
    if flag == "context_urbain":
        return "contexte"
    # (A3a) entrées des registres urbains hors ère 1976-1980 (aujourd'hui
    #       reception_posthume car postérieures) : contexte, pas réception.
    if cat == "reception_posthume" and re.match(r"CHR-(S\d+)", rid) \
            and re.match(r"CHR-(S\d+)", rid).group(1) in URBAN_CONTEXT_SOURCES:
        return "contexte"
    if rid in ATTEND_OTHERS_TO_CONTEXTE or rid in CONTEXTE_B1:
        return "contexte"
    if rid in PERF_TO_CONCERT or rid in SIG_TO_CONCERT:
        return "concert_a_migrer"
    return None


# (A5) bundles gig + fait distinct (un seul enregistrement) : restent jalon mais
# étiquetés pour scission au registre CONCERT- (étape 10). NON canonicalisés.
BUNDLE_SPLIT_ETAPE_10 = {
    # Hope & Anchor 1978-12-27 — premier concert londonien + première crise
    "CHR-S10-1978-007", "CHR-S45-1978-12-27-HOPE-AND-ANCHOR-FIRST-FIT",
    "CHR-S75-1978-008", "CHR-S76-1978-019",
    "CHR-S41-TL3-1978-12-27-HOPE-ANCHOR-REVIEW",  # facette gig pure du même soir
    # Nashville Rooms 1979-08-13 — gig + entrée d'Annik Honoré
    "CHR-S41-1979-08-13-NASHVILLE-ANNIK",
    "CHR-S41-1979-08-13-NASHVILLE-ANNIK-ATMOSPHERE", "CHR-S76-1979-019",
    # Rainbow 1980-04-04 — gig + crise (stroboscopes)
    "CHR-S41-1980-04-04-RAINBOW-FIT-MOONLIGHT-INSISTENCE", "CHR-S75-1980-005",
    # Genetic/Marquee 1979-03-04 — session démos Genetic + gig au Marquee
    "CHR-S41-1979-03-04-EDEN-GENETIC-MARQUEE",
}



# --------------------------------------------------------------------------- #
# date_precision — inférence honnête depuis la date (jamais plus précis que la
# source). Énum : {jour, mois, saison, annee, circa, intervalle}.
# --------------------------------------------------------------------------- #
_MONTHS = {"janvier", "février", "fevrier", "mars", "avril", "mai", "juin",
           "juillet", "août", "aout", "septembre", "octobre", "novembre",
           "décembre", "decembre"}
_season = re.compile(r"\b(été|ete|hiver|printemps|automne|noël|noel|summer|spring|winter|autumn|fall)\b", re.I)
_approx = re.compile(r"approx|circa|inferred|to_verify|overnight|^after_|^before_|during_|same_|around|environ|vers|fin |début |debut |milieu", re.I)


def precision(date, prec):
    """Return (date_precision, debut, fin)."""
    d = (date or "").strip().strip('"')
    p = (prec or "").strip().lower()
    # intervals (ISO or decade-as-range)
    m = (re.match(r"^(\d{4}-\d{2}-\d{2})\s*[/]\s*(\d{4}-\d{2}-\d{2})$", d)
         or re.match(r"^(\d{4}-\d{2})\s*[/]\s*(\d{4}-\d{2})$", d)
         or re.match(r"^(\d{4})[/](\d{4})$", d))
    if m:
        return "intervalle", m.group(1), m.group(2)
    m = re.match(r"^(\d{4})-(\d{4})$", d)
    if m:
        return "intervalle", m.group(1), m.group(2)
    if re.search(r"\d{4}.*[/].*\d{4}", d):
        parts = re.split(r"[/]", d)
        return "intervalle", parts[0].strip(), parts[-1].strip()
    if "range" in p or p in ("exact_range", "date_range", "month_range", "approximate_range"):
        return "intervalle", "", ""
    if _season.search(d) or p in ("saison", "season") or "spring" in p or "summer" in p or "winter" in p or "autumn" in p:
        return "saison", "", ""
    md = re.search(r"années?\s*(\d{4})", d)
    if "décennie" in p or "decade" in p or md:
        if md and re.fullmatch(r"années\s*\d{4}", d.strip()):
            y = int(md.group(1))
            return "intervalle", str(y), str(y + 9)
        return "circa", "", ""
    if re.search(r"xxe|seconde moitié|moitié", d, re.I) or "à préciser" in d.lower() or "a preciser" in d.lower():
        return "circa", "", ""
    if _approx.search(p):
        return "circa", "", ""
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", d):
        return "jour", "", ""
    if re.fullmatch(r"\d{4}-\d{2}", d):
        return "mois", "", ""
    if re.fullmatch(r"\d{4}", d):
        return "annee", "", ""
    if re.match(r"^\d{1,2}\s+[a-zéûôA-Za-zàâ]+\s+\d{4}$", d):
        return "jour", "", ""
    if re.match(r"^[A-Za-zéûôàâ]+\s+\d{4}$", d) and d.split()[0].lower() in _MONTHS:
        return "mois", "", ""
    if re.search(r"fin |début |debut |milieu|circa|environ|vers", d, re.I):
        return "circa", "", ""
    return "circa", "", ""


# --------------------------------------------------------------------------- #
# Parse: collect every entry's id/date/precision_date/event/certainty/type.
# --------------------------------------------------------------------------- #
FENCE = re.compile(r"```yaml\s*(.*?)\s*```", re.S)


def parse_entries():
    entries = {}  # id -> dict(date, prec, event, cert, types)
    for f in sorted(glob.glob(str(CHRONO_DIR / "*.md"))):
        if Path(f).name == CANON_FILE.name:
            continue
        md = Path(f).read_text(encoding="utf-8")
        for blk in FENCE.findall(md):
            try:
                data = yaml.safe_load(blk)
            except Exception:
                continue
            if not isinstance(data, dict):
                continue
            items = []
            for k, v in data.items():
                if isinstance(v, list) and any(isinstance(x, dict) and "id" in x for x in v):
                    items += [x for x in v if isinstance(x, dict) and "id" in x]
            if not items and "id" in data and (data.get("date") or data.get("event")
                                               or data.get("evenement") or data.get("label")):
                items = [data]
            for it in items:
                rid = str(it["id"])
                if not rid.startswith("CHR-"):
                    continue
                ev = str(it.get("event") or it.get("evenement") or it.get("label") or "").replace("\n", " ")
                t = it.get("type")
                t = "|".join(t) if isinstance(t, list) else str(t or "")
                entries[rid] = dict(
                    date=str(it.get("date", "")).strip(),
                    prec=str(it.get("precision_date", "")).strip(),
                    event=ev,
                    cert=str(it.get("certainty") or it.get("statut") or "").strip(),
                    types=t)
    return entries


# --------------------------------------------------------------------------- #
# Line-splice insertion (append-only, minimal diff, idempotent).
# --------------------------------------------------------------------------- #
ID_LINE = re.compile(r"^(\s*)(- )?id:\s*(\S+)\s*$")


def entry_span_end(lines, start):
    """Index (exclusive) where the entry starting at `start` ends: next id-line,
    closing fence, or dedent below the id's field indent."""
    field_indent = lines[start].index("id:")
    i = start + 1
    while i < len(lines):
        ln = lines[i]
        if ID_LINE.match(ln):
            break
        if ln.strip() == "```":
            break
        if ln.strip() and (len(ln) - len(ln.lstrip())) < field_indent and not ln.lstrip().startswith("- "):
            break
        i += 1
    return i


def has_field(lines, start, end, indent, key):
    pat = re.compile(r"^\s*" + re.escape(key) + r":")
    for i in range(start, end):
        if pat.match(lines[i]) and (len(lines[i]) - len(lines[i].lstrip())) == indent:
            return True
    return False


def transform_file(path, entries, phase, stats, member_map=None):
    member_map = member_map if member_map is not None else MEMBER_TO_CANON
    lines = path.read_text(encoding="utf-8").split("\n")
    out = []
    i = 0
    while i < len(lines):
        out.append(lines[i])
        m = ID_LINE.match(lines[i])
        if not m:
            i += 1
            continue
        rid = m.group(3).strip('"')
        if not rid.startswith("CHR-") or rid not in entries:
            i += 1
            continue
        indent = lines[i].index("id:")
        end = entry_span_end(lines, i)
        e = entries[rid]
        inserts = []
        if phase == "classification":
            cat, _ = classify(rid, e["date"], e["event"], e["cert"], e["types"])
            if not has_field(lines, i, end, indent, "categorie"):
                inserts.append(("categorie", cat))
        elif phase == "canon":
            if rid in member_map and not has_field(lines, i, end, indent, "same_as"):
                inserts.append(("same_as", member_map[rid]))
                stats["same_as"] += 1
        elif phase == "precision":
            dp, db, fi = precision(e["date"], e["prec"])
            if not has_field(lines, i, end, indent, "date_precision"):
                inserts.append(("date_precision", dp))
                if dp == "intervalle" and db:
                    inserts.append(("date_debut", db))
                    inserts.append(("date_fin", fi))
        elif phase == "tag":
            if rid in BUNDLE_SPLIT_ETAPE_10 and not has_field(lines, i, end, indent, "a_scinder_etape_10"):
                inserts.append(("a_scinder_etape_10", "true"))
                stats["tagged"] += 1
        for key, val in inserts:
            out.append(" " * indent + f"{key}: {val}")
        i += 1
    new = "\n".join(out)
    if new != path.read_text(encoding="utf-8"):
        path.write_text(new, encoding="utf-8")
        stats["files"] += 1


def reclassify_file(path, entries, stats):
    """Réécrit la valeur des lignes `categorie:` selon reclass_target (pas
    d'insertion : la catégorie existe déjà depuis la phase classification)."""
    lines = path.read_text(encoding="utf-8").split("\n")
    cur_id = None
    cur_indent = None
    changed = False
    cat_pat = re.compile(r"^(\s*)categorie:\s*(\S+)\s*$")
    for idx, ln in enumerate(lines):
        m = ID_LINE.match(ln)
        if m:
            cur_id = m.group(3).strip('"')
            cur_indent = ln.index("id:")
            continue
        cm = cat_pat.match(ln)
        if cm and cur_id in entries and len(cm.group(1)) == cur_indent:
            e = entries[cur_id]
            tgt = reclass_target(cur_id, e["date"], e["event"], e["cert"], e["types"])
            if tgt and tgt != cm.group(2):
                lines[idx] = " " * cur_indent + f"categorie: {tgt}"
                changed = True
                stats[tgt] += 1
    if changed:
        path.write_text("\n".join(lines), encoding="utf-8")
        stats["files"] += 1


def write_canonical_file(entries, canon=None):
    canon = canon if canon is not None else CANON
    lines = [
        "# Registre chronologique — identités canoniques d'événements (EVENT-)",
        "",
        "> Brique d'identité (étape 6). Chaque entrée ci-dessous est un **jalon**",
        "> canonique `EVENT-<SLUG>` : slug sémantique, source-agnostique, **sans date",
        "> dans l'ID** (la date est un champ). Les identifiants legacy `CHR-…` qui",
        "> désignent le même jalon portent `same_as: EVENT-…` dans leur fichier source",
        "> (réconciliation additive, sans renommage — cf. cross_registres.md §1).",
        "> `membres_reconcilies` liste ces legacy à titre de traçabilité.",
        "",
        "---",
        "",
    ]
    for cid, d in canon.items():
        srcs = sorted({source_of(m) for m in d["members"]},
                      key=lambda s: (s != "MASTER", s))
        lines.append(f"## {cid} — {d['label']}")
        lines.append("")
        lines.append("```yaml")
        lines.append(f"id: {cid}")
        lines.append("type_unite: chronology_event")
        lines.append("categorie: jalon")
        lines.append(f"date: \"{d['date']}\"")
        lines.append(f"date_precision: {d['precision']}")
        if d.get("debut"):
            lines.append(f"date_debut: {d['debut']}")
            lines.append(f"date_fin: {d['fin']}")
        lines.append(f"event: >")
        lines.append(f"  {d['label']}.")
        lines.append("sources:")
        for s in srcs:
            lines.append(f"  - {s}")
        lines.append("membres_reconcilies:")
        for mem in d["members"]:
            lines.append(f"  - {mem}")
        if d.get("prudence"):
            lines.append(f"prudence_methodologique: >")
            lines.append(f"  {d['prudence']}")
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("")
    CANON_FILE.write_text("\n".join(lines), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", required=True,
                    choices=["classification", "canon", "precision", "reclassify",
                             "tag", "report", "check"])
    ap.add_argument("--wave", choices=["all", "b1", "b2"], default="all",
                    help="canon : restreint aux canoniques de la vague (b1 exclut "
                         "les EVENT- tagués wave=b2). Défaut : all.")
    args = ap.parse_args()

    entries = parse_entries()

    # Integrity: every declared canonical member must exist.
    missing = [m for m in MEMBER_TO_CANON if m not in entries]
    if missing:
        print("ERREUR : membres canoniques introuvables :", missing, file=sys.stderr)
        return 2

    stats = collections.Counter()

    if args.phase == "check":
        # Vérification de cohérence légère (pas un validateur de schéma) :
        #  1. tout same_as résout vers un EVENT- canonique existant ;
        #  2. aucune date ISO impossible ; 3. aucun intervalle inversé.
        canon = set(CANON)
        edges = impossible = inverted = 0
        problems = []
        for f in sorted(glob.glob(str(CHRONO_DIR / "*.md"))):
            md = Path(f).read_text(encoding="utf-8")
            for blk in FENCE.findall(md):
                try:
                    data = yaml.safe_load(blk)
                except Exception:
                    continue
                if not isinstance(data, dict):
                    continue
                items = []
                for k, v in data.items():
                    if isinstance(v, list) and any(isinstance(x, dict) and "id" in x for x in v):
                        items += [x for x in v if isinstance(x, dict) and "id" in x]
                if not items and "id" in data:
                    items = [data]
                for it in items:
                    sa = it.get("same_as")
                    if sa:
                        edges += 1
                        if str(sa) not in canon:
                            problems.append(f"same_as non résolu: {it.get('id')} -> {sa}")
                    db, fi = str(it.get("date_debut", "")), str(it.get("date_fin", ""))
                    if db and fi and db > fi:
                        inverted += 1
                        problems.append(f"intervalle inversé: {it.get('id')} {db}/{fi}")
                    for iso in re.findall(r"\d{4}-\d{2}-\d{2}", str(it.get("date", ""))):
                        _, mo, da = (int(x) for x in iso.split("-"))
                        if not (1 <= mo <= 12 and 1 <= da <= 31):
                            impossible += 1
                            problems.append(f"date impossible: {it.get('id')} {iso}")
        print(f"same_as: {edges} | impossibles: {impossible} | inversés: {inverted}")
        for p in problems:
            print("  ✗", p)
        return 1 if problems else 0

    if args.phase == "report":
        cats = collections.Counter()
        flags = collections.defaultdict(list)
        precs = collections.Counter()
        for rid, e in entries.items():
            cat, fl = classify(rid, e["date"], e["event"], e["cert"], e["types"])
            cats[cat] += 1
            if fl:
                flags[fl].append(rid)
            dp, _, _ = precision(e["date"], e["prec"])
            precs[dp] += 1
        print("entrées            :", len(entries))
        print("categorie          :", dict(cats))
        print("date_precision     :", dict(precs))
        print("canoniques EVENT-  :", len(CANON))
        print("arêtes same_as     :", len(MEMBER_TO_CANON))
        print("flags (à arbitrer) :", {k: len(v) for k, v in flags.items()})
        for k, v in flags.items():
            print(f"\n--- flag: {k} ({len(v)}) ---")
            for rid in sorted(v):
                print("   ", rid)
        return 0

    member_map = MEMBER_TO_CANON
    if args.phase == "canon":
        if args.wave == "b1":
            active = {c: d for c, d in CANON.items() if d.get("wave") != "b2"}
        else:
            active = dict(CANON)
        # restreint la pose des same_as aux membres des canoniques actifs
        member_map = {m: c for c, d in active.items() for m in d["members"]}
        write_canonical_file(entries, active)
        print(f"écrit {CANON_FILE.relative_to(REPO)} ({len(active)} EVENT-, vague {args.wave})")

    for f in sorted(glob.glob(str(CHRONO_DIR / "*.md"))):
        p = Path(f)
        if p.name == CANON_FILE.name:
            continue
        if args.phase == "reclassify":
            reclassify_file(p, entries, stats)
        else:
            transform_file(p, entries, args.phase, stats, member_map)

    if args.phase == "reclassify":
        moved = {k: stats[k] for k in CATEGORIES if stats[k]}
        print(f"phase reclassify : {stats['files']} fichier(s), reclassements -> {moved}")
    else:
        print(f"phase {args.phase} : {stats['files']} fichier(s) modifié(s)"
              + (f", {stats['same_as']} same_as" if args.phase == "canon" else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
