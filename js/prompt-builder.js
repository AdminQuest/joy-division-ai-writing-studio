function listBlock(items){
  if(!items||items.length===0){return '- À renseigner.';}
  return items.map(x=>'- '+x).join('\n');
}

function buildPrompt({chap,at,input,mode,registre}){
  const materiau=input&&input.trim()?input.trim():'[COLLER ICI LE TEXTE]';

  let sourcesDetail='';
  if(chap.sources && registre){
    sourcesDetail = chap.sources.map(id=>{
      const s = registre.find(x=>x.id===id);
      return s ? `- ${id} — ${s.statut} — ${s.usage}` : `- ${id}`;
    }).join("\n");
  } else {
    sourcesDetail = 'À renseigner.';
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
- Style académique
- Sources vérifiées uniquement
- Pas d’invention

MATERIAU
${materiau}`;
}
