from typing import Any, Dict, List

SCHEMA_REQUIRED_FIELDS = {
    'atom': [
        'id','source_id','auteur','titre','type_unite','concepts','chapitres',
        'statut','fiabilite','role_argumentatif','niveau_preuve','stabilite',
        'importance','risque_surinterpretation','liens_interchapitres',
        'liens_citations','motifs','concepts_derives'
    ],
    # Backbone structurel du registre citations (étape 8b-1). Identité = source
    # + ordinal (conservée, aucun renommage). `kind`, `texte`, `type` (et `page`)
    # sont dérivés par build_registers.normalize_quote_record. L'ancien socle
    # (citation_originale/langue_originale/statut_verification) devient optionnel.
    # Attribution + split fin paraphrase/concept = 8b-2.
    'quote': ['id','kind','source_id','texte','type'],
    'chronology': ['id','date','event','type','sources','certainty'],
    # Identité canonique d'événement (registre chronologique, étape 6).
    # Enregistrement d'IDENTITÉ : type/certainty/location/people sont OPTIONNELS
    # (portés par les membres legacy, atteignables par same_as). La contrainte
    # temporelle (date XOR date_debut+date_fin) est vérifiée à part.
    'chronology_event': ['id','type_unite','label','date_precision','membres_reconcilies'],
    # Identité canonique de concert (registre concerts, étape 7b). Discriminée
    # par le préfixe d'ID CONCERT- (les entrées legacy JD-CONCERT- gardent leur
    # schéma joydiv propre — cf. validate_against_schema). `lieu` est une réf
    # PLACE- ; la contrainte temporelle (date XOR date_debut+date_fin) et la
    # non-vacuité de `membres_reconcilies` sont vérifiées à part. `statut` est
    # optionnel (présent pour les concerts annulés).
    'concert': ['id','type_unite','label','date_precision','lieu','membres_reconcilies'],
    'person': ['id','name','role','sources'],
    'song': ['song','themes','sources','chapters']
}

SCHEMA_CONTROLLED_VALUES = {
    'atom': {
        'statut': {'verifie','a_verifier','a_reverifier','a_consolider'},
        'fiabilite': {'forte','moyenne','faible'},
        'type_unite': {
            'fait','lecture','concept','citation_clef','mythe','controverse',
            'biographie','production','concert','reception','memoire','santé',
            'relation','politique','esthétique','archive','sociologie','analyse',
            'psychologie_sociale','culture_musicale','domesticité',
            # Ajouts D.6 (étape 2) : prudence documentaire transversale et
            # atome de renvoi croisé entre sources. Tenir synchronisé avec
            # schemas/atom.schema.yaml (controlled_values.type_unite).
            'prudence_methodologique','reference_croisee'
        }
    },
    'quote': {
        'type': {'verbatim','non_verbatim'},
        'langue_originale': {'en','fr','de','it'}
    },
    'chronology': {
        'certainty': {'strong','medium','weak'}
    }
}

NESTED_REQUIRED = {
    'niveau_preuve': ['statut','corroboration','confiance'],
    'stabilite': ['statut','risque_revision'],
    'importance': ['niveau'],
    'risque_surinterpretation': ['niveau']
}

LIST_FIELDS = {
    'role_argumentatif',
    'liens_interchapitres',
    'liens_citations',
    'motifs',
    'concepts_derives',
    'concepts',
    'chapitres'
}

def validate_against_schema(kind: str, data: Dict[str, Any]) -> List[str]:
    diagnostics: List[str] = []

    # Les identités canoniques EVENT-<SLUG> (chronology_event) suivent un schéma
    # distinct du chronology legacy. Discriminé par le préfixe d'ID EVENT- : les
    # entrées legacy S29/S34 (ID CHR-, type_unite chronology_event) restent du
    # chronology legacy et conservent leurs requis.
    schema_key = kind
    if kind == 'chronology' and str(data.get('id', '')).startswith('EVENT-'):
        schema_key = 'chronology_event'

    # Le kind `concert` couvre deux schémas : l'identité canonique CONCERT-
    # (validée ici) et le legacy JD-CONCERT- (schéma joydiv propre, NON validé
    # par ce module — il a son schemas/concert_v1.yaml). On ne contraint donc
    # que les ID canoniques CONCERT-.
    if kind == 'concert' and not str(data.get('id', '')).startswith('CONCERT-'):
        return diagnostics

    for key in SCHEMA_REQUIRED_FIELDS.get(schema_key, []):
        if key not in data:
            diagnostics.append(f'Missing required field: {key}')

    if schema_key in ('chronology_event', 'concert'):
        has_date = 'date' in data
        has_interval = 'date_debut' in data and 'date_fin' in data
        if has_date == has_interval:
            diagnostics.append(
                f'{schema_key} requires exactly one of `date` or `date_debut`+`date_fin`')
        membres = data.get('membres_reconcilies')
        if not isinstance(membres, list) or len(membres) < 1:
            diagnostics.append(f'{schema_key}: `membres_reconcilies` must be a non-empty list')

    for field_name in LIST_FIELDS:
        if field_name in data and not isinstance(data[field_name], list):
            diagnostics.append(f'Field must be a list: {field_name}')

    for field_name, allowed_values in SCHEMA_CONTROLLED_VALUES.get(kind, {}).items():
        if field_name not in data:
            continue

        value = data[field_name]

        if isinstance(value, list):
            invalid = [item for item in value if item not in allowed_values]
            if invalid:
                diagnostics.append(f'Invalid values for {field_name}: {invalid}')
        else:
            if value not in allowed_values:
                diagnostics.append(f'Invalid value for {field_name}: {value}')

    if kind == 'atom':
        for nested_field, required_subfields in NESTED_REQUIRED.items():
            nested = data.get(nested_field)

            if nested is None:
                continue

            if not isinstance(nested, dict):
                diagnostics.append(f'Field must be an object/dict: {nested_field}')
                continue

            for subfield in required_subfields:
                if subfield not in nested:
                    diagnostics.append(f'Missing nested field: {nested_field}.{subfield}')

    return diagnostics
