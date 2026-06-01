#!/usr/bin/env python3
"""Génère registers/places/concert_venues_lot3.md (étape 10, phase 2-B).

59 venues de concerts (lot 3) + 1 alias (SALFORD-TECHNICAL-COLLEGE → S83-004).
Données = lot 3 validé par l'humain. Coordonnées WGS84, geo_precision ∈ enum
gelé {exacte,rue,quartier,ville,region}. reference_croisee omis (vide pour ce lot).
Conforme à schemas/places.schema.yaml. Usage unique, traçable.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (id, label, type, lat, lng, geo_precision, prudence_methodologique)
V = [
("PLACE-9-30-CLUB-WASHINGTON","9:30 Club, Washington DC","salle",38.89733,-77.02450,"exacte","Original 9:30 Club, 930 F Street NW, Washington DC. Concert prévu, tournée américaine annulée."),
("PLACE-ACTIONSPACE-LONDON","Action Space, London","salle",51.52131,-0.13052,"exacte","Action Space, 16 Chenies Street, London WC1. Adresse issue d'un programme d'époque."),
("PLACE-AJANTA-THEATRE-DERBY","Ajanta Theatre, Derby","salle",52.91890,-1.47690,"quartier","Ancien cinéma ; localisation fine à confirmer par plan historique."),
("PLACE-AMERICAN-INDIAN-CENTER-SF","American Indian Center, San Francisco","salle",37.76919,-122.42217,"exacte","225 Valencia Street, San Francisco. Concert prévu, tournée américaine annulée."),
("PLACE-ASTORIA-EDINBURGH","Astoria, Edinburgh","salle",55.94670,-3.20410,"quartier","Salle disparue ; localisation approximée, adresse fine à documenter."),
("PLACE-BAND-ON-THE-WALL","Band on the Wall, Manchester","salle",53.48514,-2.23488,"exacte","25 Swan Street, Manchester. Salle toujours existante."),
("PLACE-BOLTON-INSTITUTE-OF-TECHNOLOGY","Bolton Institute of Technology","education",53.57550,-2.42920,"quartier","Bolton Institute / University of Bolton, Deane Road. Concert listé mais annulé. Coordonnée de campus."),
("PLACE-BOOKIES-DETROIT","Bookies Club, Detroit","salle",42.41810,-83.08060,"rue","Concert prévu, tournée américaine annulée. Adresse précise à confirmer."),
("PLACE-BOWDON-VALE-YOUTH-CLUB","Bowdon Vale Youth Club, Altrincham","salle",53.38130,-2.36220,"quartier","Adresse exacte non stabilisée."),
("PLACE-BRUNEL-UNIVERSITY","Brunel University, Uxbridge","education",51.53285,-0.47275,"quartier","Concert du 15 novembre 1978. Coordonnée de campus, salle exacte non précisée."),
("PLACE-CAIRD-HALL-DUNDEE","Caird Hall, Dundee","salle",56.45961,-2.97055,"exacte","City Square, Dundee. Salle municipale."),
("PLACE-CAPITOL-ABERDEEN","Capitol Theatre, Aberdeen","salle",57.14577,-2.10531,"exacte","Union Street, Aberdeen. Ancien cinéma / théâtre."),
("PLACE-CITY-HALL-CORK","Cork City Hall","salle",51.89785,-8.46537,"exacte","Anglesea Street, Cork."),
("PLACE-DUFFYS-MINNEAPOLIS","Duffy's, Minneapolis","salle",44.94890,-93.28820,"rue","Concert prévu, tournée américaine annulée. Adresse précise à confirmer."),
("PLACE-FAN-CLUB-LEEDS","The Fan Club, Leeds","salle",53.79840,-1.54390,"quartier","The Fan Club / Brannigan's, Leeds. Salle disparue ; localisation fine à vérifier."),
("PLACE-FLIPPERS-LOS-ANGELES","Flipper's Roller Boogie Palace, Los Angeles","salle",34.08370,-118.34610,"quartier","Concert prévu, tournée américaine annulée. Adresse exacte à confirmer."),
("PLACE-HIGH-WYCOMBE-TOWN-HALL","High Wycombe Town Hall","salle",51.62861,-0.74902,"exacte","Queen Victoria Road."),
("PLACE-HURRAH-NEW-YORK","Hurrah, New York","salle",40.76480,-73.97610,"quartier","Concert prévu, tournée américaine annulée. Localisation associée à West 62nd Street ; à confirmer."),
("PLACE-KELLYS-MANCHESTER","Kelly's, Manchester","salle",53.49120,-2.24010,"rue","Amber Street, Manchester. Club disparu."),
("PLACE-LANTAREN-ROTTERDAM","Club Lantaren, Rotterdam","salle",51.91816,4.47661,"exacte","Gouvernestraat 133, Rotterdam. Concert européen du 16 janvier 1980."),
("PLACE-LEEDS-UNIVERSITY","University of Leeds","education",53.80670,-1.55500,"quartier","Coordonnée de campus, salle exacte à préciser selon la date du concert."),
("PLACE-LIMIT-CLUB-SHEFFIELD","The Limit Club, Sheffield","salle",53.37990,-1.47130,"rue","Club disparu ; adresse à confirmer."),
("PLACE-LIVERPOOL-EMPIRE","Liverpool Empire Theatre","salle",53.40854,-2.97841,"exacte","Lime Street, Liverpool. Théâtre toujours existant. Aucune fiche concert correspondante dans le registre actuel."),
("PLACE-LOCARNO-BRISTOL","Locarno, Bristol","salle",51.45720,-2.59280,"quartier","Salle disparue ; localisation fine à vérifier."),
("PLACE-MANCHESTER-APOLLO","Manchester Apollo","salle",53.46918,-2.22285,"exacte","Stockport Road, Ardwick. Salle toujours existante. Fiches concerts sous « Apollo Theatre »."),
("PLACE-MOUNTFORD-HALL-LIVERPOOL","Mountford Hall, Liverpool","salle",53.40555,-2.96691,"exacte","Liverpool Guild of Students. Salle universitaire stable."),
("PLACE-NEW-THEATRE-OXFORD","New Theatre Oxford","salle",51.75353,-1.26176,"exacte","George Street. Théâtre toujours existant."),
("PLACE-NEWCASTLE-CITY-HALL","Newcastle City Hall","salle",54.97770,-1.61360,"exacte","Northumberland Road. Salle toujours existante."),
("PLACE-NEWCASTLE-GUILDHALL","Newcastle Guildhall","salle",54.96980,-1.61080,"exacte","Quayside. Bâtiment historique protégé. Fiches concerts sous « Guildhall » et « Guild Hall »."),
("PLACE-ODEON-BIRMINGHAM","Odeon, Birmingham","salle",52.47990,-1.89820,"quartier","New Street. Bâtiment démoli ou transformé ; localisation historique."),
("PLACE-ODEON-CANTERBURY","Odeon, Canterbury","salle",51.27970,1.07920,"quartier","Adresse fine à confirmer."),
("PLACE-ODEON-EDINBURGH","Odeon, Edinburgh","salle",55.94720,-3.20400,"quartier","Secteur Clerk Street. Localisation historique (Cinema Treasures #2322)."),
("PLACE-OLDHAM-TOWER-CLUB","Tower Club, Oldham","salle",53.54090,-2.11130,"quartier","Adresse précise à confirmer. Aucune fiche concert correspondante dans le registre actuel."),
("PLACE-OLYMPIA-DUBLIN","Olympia Theatre, Dublin","salle",53.34430,-6.26600,"exacte","Dame Street. Théâtre toujours existant."),
("PLACE-PAARD-VAN-TROJE-THE-HAGUE","Paard van Troje, Den Haag","salle",52.07864,4.31333,"exacte","Prinsegracht 12, Den Haag. Salle toujours existante."),
("PLACE-PAVILION-HEMEL-HEMPSTEAD","Pavilion, Hemel Hempstead","salle",51.75240,-0.47250,"quartier","Adresse fine à confirmer."),
("PLACE-PIPERS-CYPRUS-TAVERN","Piper's, Manchester","salle",53.48040,-2.23960,"rue","Spring Gardens, Manchester. Ne pas confondre avec Cyprus Tavern — Joy Division Central signale explicitement cette confusion."),
("PLACE-PLAYHOUSE-THEATRE-NOTTINGHAM","Nottingham Playhouse","salle",52.95391,-1.15422,"exacte","Wellington Circus. Théâtre stable."),
("PLACE-ROCK-GARDEN-MIDDLESBROUGH","Rock Garden, Middlesbrough","salle",54.57630,-1.23540,"quartier","Localisation fine à confirmer."),
("PLACE-ROYALTY-THEATRE-LONDON","Royalty Theatre, London","salle",51.51160,-0.12820,"quartier","Lieu disparu ou reconverti ; localisation historique à confirmer."),
("PLACE-RUSSELL-CLUB","Russell Club / Factory, Hulme","salle",53.46770,-2.25610,"rue","Royce Road, Hulme. Club démoli ; situé près de Royce Road / Clayburn Street. Lieu des Factory nights — « The Factory I » dans le registre des concerts (≠ The Factory II)."),
("PLACE-SCALA-CINEMA-LONDON","Scala, London","salle",51.53084,-0.12036,"exacte","275 Pentonville Road. Ancien cinéma, salle actuelle."),
("PLACE-SHEFFIELD-POLYTECHNIC","Sheffield Polytechnic","education",53.38140,-1.46630,"quartier","Sheffield Hallam University. Coordonnée de campus central."),
("PLACE-SOPHIA-GARDENS-CARDIFF","Sophia Gardens Pavilion, Cardiff","salle",51.48610,-3.19120,"quartier","Ancien pavillon démoli."),
("PLACE-SOUTHAMPTON-UNIVERSITY","University of Southampton","education",50.93440,-1.39580,"quartier","Highfield Campus. Salle exacte à préciser."),
("PLACE-ST-ANDREWS-UNIVERSITY","University of St Andrews","education",56.34170,-2.79280,"quartier","Coordonnée de campus, salle exacte à préciser."),
("PLACE-ST-GEORGES-HALL-BRADFORD","St George's Hall, Bradford","salle",53.79343,-1.75276,"exacte","Salle toujours existante."),
("PLACE-STARWOOD-LOS-ANGELES","The Starwood, Los Angeles","salle",34.09020,-118.38530,"quartier","West Hollywood. Concert prévu, tournée américaine annulée. Localisation historique à confirmer."),
("PLACE-STOCKPORT-COLLEGE","Stockport College","education",53.40860,-2.15870,"quartier","Site modernisé ; localisation approximée. Fiches concerts sous « Stockport Tech »."),
("PLACE-TIER-3-NEW-YORK","Tier 3, New York","salle",40.71970,-74.00470,"quartier","Concert prévu, tournée américaine annulée. Localisation associée à Tribeca ; à confirmer."),
("PLACE-TIFFANYS-LEICESTER","Tiffany's, Leicester","salle",52.63700,-1.13270,"quartier","Salle disparue ; localisation fine à confirmer."),
("PLACE-TOP-RANK-READING","Top Rank, Reading","salle",51.45620,-0.97110,"quartier","Salle disparue ; adresse fine à confirmer."),
("PLACE-TOP-RANK-SHEFFIELD","Top Rank, Sheffield","salle",53.38100,-1.46820,"quartier","Salle disparue ; adresse fine à confirmer."),
("PLACE-ULSTER-HALL-BELFAST","Ulster Hall, Belfast","salle",54.59401,-5.93008,"exacte","Bedford Street. Salle toujours existante."),
("PLACE-UNIVERSITY-OF-KENT","University of Kent, Canterbury","education",51.29650,1.06310,"quartier","Coordonnée de campus, salle exacte à préciser."),
("PLACE-UNIVERSITY-OF-LONDON-UNION","University of London Union","education",51.52210,-0.13070,"exacte","Malet Street, London. Ancien ULU."),
("PLACE-WEST-RUNTON-PAVILION","West Runton Pavilion, Norfolk","salle",52.93530,1.24410,"quartier","Salle disparue ; site approximatif."),
("PLACE-WINTER-GARDENS-MALVERN","Winter Gardens, Malvern","salle",52.11125,-2.33037,"exacte","Complexe culturel stabilisé."),
("PLACE-YMCA-LONDON","YMCA, London","salle",51.50940,-0.13110,"quartier","Adresse précise à établir selon l'événement."),
]

def q(s): return '"' + s.replace('"', '\\"') + '"'

lines = [
"# Registre lieux — Venues de concerts (lot 3, étape 10)",
"",
"Promotion en entrées `PLACE-` des salles de concerts géolocalisées (lot 3).",
"Coordonnées WGS84 curées (recoupées sources d'époque / Cinema Treasures /",
"Joy Division Central). `geo_precision` ∈ {exacte, rue, quartier, ville, region}.",
"Câblées aux fiches concerts via `place_id` (cf. registers/concerts/).",
"",
"```yaml",
"type_unite: registre_lieux",
"statut: integration_directe",
"```",
"",
"```yaml",
"places:",
]
for (pid,label,typ,lat,lng,prec,prud) in V:
    lines += [
        f"  - id: {pid}",
        f"    label: {q(label)}",
        f"    type: {typ}",
        f"    lat: {lat}",
        f"    lng: {lng}",
        f"    geo_precision: {prec}",
        f"    prudence_methodologique: {q(prud)}",
        "",
    ]
# Alias : Salford Technical College → canonique PLACE-S83-004 (Salford Technical School)
lines += [
    "  # Alias : même institution que PLACE-S83-004 (Salford Technical School).",
    "  # Coordonnée portée par le canonique (S83). Concerts « Salford College of Technology ».",
    "  - id: PLACE-SALFORD-TECHNICAL-COLLEGE",
    '    label: "Salford Technical College"',
    "    type: education",
    "    same_as: PLACE-S83-004",
    "```",
    "",
]
out = ROOT / "registers" / "places" / "concert_venues_lot3.md"
out.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
print(f"écrit {out.relative_to(ROOT)} — {len(V)} venues + 1 alias")
