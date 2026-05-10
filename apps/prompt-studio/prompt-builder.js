function buildPrompt({chap,at,input,mode,registre,niveau,contexte}){
  const materiau=input&&input.trim()?input.trim():'[COLLER ICI LE TEXTE]';

  const header=`NIVEAU IA : ${niveau?niveau.nom:'non défini'}\nOBJECTIF : ${niveau?niveau.objectif:''}`;

  const contextualBlock=`\nCONTEXTE DOCUMENTAIRE INJECTE\n${contexte||'Aucun contexte'}\n`;

  const chapitreBlock=chap?`\nCHAPITRE CIBLE\n${chap.nom}\n`:'\n';
  const atelierBlock=at?`\nATELIER\n${at.nom}\n`:'\n';

  const commonRules=`\nREGLES\n- Ne jamais inventer une citation\n- Signaler les contradictions documentaires\n- Distinguer les faits, hypothèses et interprétations\n- Respecter le style académique narratif défini pour le projet\n- Utiliser les références injectées lorsque pertinentes\n`;

  return `${header}
${chapitreBlock}
${atelierBlock}
MODE REDACTIONNEL
${mode}
${contextualBlock}
${commonRules}
MISSION
Produire une réponse adaptée au mode rédactionnel sélectionné en mobilisant le contexte documentaire injecté.

MATERIAU A TRAITER
${materiau}`;
}
