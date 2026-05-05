function buildPrompt({chap,at,input,mode,registre,niveau}){
  const materiau=input&&input.trim()?input.trim():'[COLLER ICI LE TEXTE]';

  const header=`NIVEAU IA : ${niveau?niveau.nom:'non défini'}\nOBJECTIF : ${niveau?niveau.objectif:''}`;

  if(niveau && niveau.id==='sources'){
    return `${header}\n\nEXTRACTION DOCUMENTAIRE\n\nExtraire fidèlement les informations suivantes :\n- faits\n- citations exactes\n- références\n\nINTERDICTIONS\n- aucune reformulation libre\n- aucune interprétation\n\nMATERIAU\n${materiau}`;
  }

  if(niveau && niveau.id==='recherche'){
    return `${header}\n\nRECHERCHE DOCUMENTAIRE\n\nCompléter et vérifier :\n- sources\n- citations\n- références\n\nSIGNALER\n- sources fragiles\n- incohérences\n\nMATERIAU\n${materiau}`;
  }

  if(niveau && niveau.id==='production'){
    return `${header}\n\nREDACTION LONGUE\n\nProduire un texte structuré, fluide, sans inventer.\n\nCONTRAINTES\n- style académique\n- respect du chapitre\n\nMATERIAU\n${materiau}`;
  }

  if(niveau && niveau.id==='controle'){
    return `${header}\n\nCONTROLE GLOBAL\n\nVérifier :\n- cohérence\n- doublons\n- sources\n- structure\n\nMATERIAU\n${materiau}`;
  }

  return `MODE STANDARD\n\n${materiau}`;
}
