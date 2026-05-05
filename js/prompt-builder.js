function listBlock(items){
  if(!items||items.length===0){return '- À renseigner.';}
  return items.map(x=>'- '+x).join('\n');
}

function buildSourcesBlock(chap,registre){
  if(!chap.sources || chap.sources.length===0){
    return '- Aucune source renseignée pour ce chapitre dans chapitres.json.';
  }
  if(!registre || registre.length===0){
    return chap.sources.map(id=>'- '+id+' — statut non disponible').join('\n');
  }
  return chap.sources.map(id=>{
    const s=registre.find(x=>x.id===id);
    if(!s){return '- '+id+' — absent du registre';}
    const statut=s.statut||'statut non renseigné';
    const usage=s.usage||'usage non renseigné';
    const auteur=s.auteur?(' — '+s.auteur):'';
    return '- '+id+auteur+' — '+statut+' — '+usage;
  }).join('\n');
}

function buildPrompt({chap,at,input,mode,registre}){
  const materiau=input&&input.trim()?input.trim():'[COLLER ICI LE TEXTE]';
  const sourcesDetail=buildSourcesBlock(chap,registre);

  if(mode === 'Audit automatique'){
    return `Audit complet du chapitre.

CHAPITRE
${chap.nom}

FONCTION
${chap.fonction}

HORS CHAMP
${listBlock(chap.hors_champ)}

RISQUES
${listBlock(chap.risques)}

CONTROLE ATTENDU
1. Cohérence globale.
2. Respect du périmètre.
3. Détection des doublons.
4. Analyse des sources utilisées.
5. Identification des zones non sourcées.
6. Identification des sources fragiles.
7. Recommandations structurées.

SOURCES
${sourcesDetail}

MATERIAU
${materiau}`;
  }

  return `Tu interviens sur le projet de livre « Joy Division, le son de l’éternel ».

CHAPITRE CIBLE
${chap.nom}

FONCTION DU CHAPITRE
${chap.fonction}

HORS CHAMP EXPLICITE
${listBlock(chap.hors_champ)}

RISQUES DE GLISSEMENT
${listBlock(chap.risques)}

SOURCES A MOBILISER
${sourcesDetail}

ATELIER
${at.nom}

OBJECTIF
${at.objectif}

CONTROLES
${listBlock(at.controles)}

MODE
${mode}

CONVENTIONS
- Style académique.
- Sources vérifiées uniquement.
- Pas d’invention.
- Guillemets français.
- Albums en italique.
- Titres de chansons entre guillemets.

MATERIAU
${materiau}`;
}
