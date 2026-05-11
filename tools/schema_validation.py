from typing import Any, Dict, List

SCHEMA_REQUIRED_FIELDS = {
    'atom': [
        'id','source_id','auteur','titre','type_unite','concepts','chapitres',
        'statut','fiabilite','role_argumentatif','niveau_preuve','stabilite',
        'importance','risque_surinterpretation','liens_interchapitres',
        'liens_citations','motifs','concepts_derives'
    ],
    'quote': ['id','source_id','citation_originale','langue_originale','statut_verification'],
    'chronology': ['id','date','event','type','sources','certainty'],
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
            'psychologie_sociale','culture_musicale','domesticité'
        }
    },
    'quote': {
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

    for key in SCHEMA_REQUIRED_FIELDS.get(kind, []):
        if key not in data:
            diagnostics.append(f'Missing required field: {key}')

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
