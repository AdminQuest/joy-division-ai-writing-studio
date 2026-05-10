from typing import Any, Dict, List

SCHEMA_REQUIRED_FIELDS = {
    'atom': ['id','source_id','auteur','titre','type_unite','concepts','chapitres','statut','fiabilite'],
    'quote': ['id','source_id','citation_originale','langue_originale','statut_verification'],
    'chronology': ['id','date','event','type','sources','certainty'],
    'person': ['id','name','role','sources'],
    'song': ['song','themes','sources','chapters']
}

SCHEMA_CONTROLLED_VALUES = {
    'atom': {
        'statut': {'verifie','a_verifier','a_reverifier'},
        'fiabilite': {'forte','moyenne','faible'}
    },
    'quote': {
        'langue_originale': {'en','fr','de','it'}
    },
    'chronology': {
        'certainty': {'strong','medium','weak'}
    }
}

def validate_against_schema(kind: str, data: Dict[str, Any]) -> List[str]:
    diagnostics: List[str] = []

    for key in SCHEMA_REQUIRED_FIELDS.get(kind, []):
        if key not in data:
            diagnostics.append(f'Missing required field: {key}')

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

    return diagnostics
