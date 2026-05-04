function listBlock(items){
  if(!items||items.length===0){return '- À renseigner.';}
  return items.map(x=>'- '+x).join('\n');
}

function buildPrompt({chap,at,input,mode}){
  const materiau=input&&input.trim()?input.trim():'[COLLER ICI LE TEXTE, LES NOTES OU LES REFERENCES A TRAITER]';
  const sources=chap.sources&&chap.sources.length?chap.sources.join(', '):'À renseigner depuis le registre des références.';
  return `Tu interviens sur le projet de livre « Joy Division, le son de l’éternel ».

CHAPITRE CIBLE
${chap.nom}

FONCTION DU CHAPITRE
${chap.fonction}

HORS CHAMP EXPLICITE
${listBlock(chap.hors_champ)}

RISQUES DE GLISSEMENT OU DE DOUBLON
${listBlock(chap.risques)}

SOURCES A MOBILISER EN PRIORITE
${sources}

ATELIER DE PILOTAGE REDACTIONNEL
${at.nom}

OBJECTIF DE L’ATELIER
${at.objectif}

CONTROLES A EFFECTUER
${listBlock(at.controles)}

MODE DE SORTIE ATTENDU
${mode}

CONVENTIONS REDACTIONNELLES
- Répondre en français.
- Employer un style académique, direct et contrôlé.
- Utiliser les guillemets français.
- Écrire les albums en italique.
- Écrire les titres de chansons entre guillemets.
- Rédiger au présent lorsque tu proposes du texte destiné au livre.
- Ne pas inventer de source, de citation, de page ou de référence.
- Signaler explicitement les éléments à vérifier.
- Ne pas pathologiser Ian Curtis hors des chapitres prévus.
- Ne pas transformer Joy Division en simple symptôme de Manchester.
- Ne pas conclure par une question ouverte.

FORME DE LA REPONSE
1. Diagnostic bref.
2. Corrections ou arbitrages proposés.
3. Texte révisé si nécessaire.
4. Points restant à vérifier.

MATERIAU A TRAITER
${materiau}`;
}
