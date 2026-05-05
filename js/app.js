let chapData=[];
let atelierData=[];
let registreData=[];

const FALLBACK_CHAPITRES=[
{id:'ch1',nom:'Chapitre 1 — Manchester année zéro : le terreau de la colère',fonction:'Établir Manchester comme environnement matériel, social et affectif conditionnant l’émergence de Joy Division.',hors_champ:['Biographie détaillée des membres','Analyse musicale détaillée','Esthétique visuelle','Héritage urbain et patrimonial'],risques:['Glissement vers le chapitre 3 pour l’analyse sonore','Glissement vers le chapitre 4 pour Ian Curtis','Glissement vers le chapitre 5 pour Peter Saville','Glissement vers les chapitres 12 ou 14 pour la patrimonialisation'],sources:['S01','S02','S03','S04','S05','S06','S07','S08','S09','S10','S11','S12','S14','S15','S16','S17','S18','S19','S20','S21','S22','S23','S24','S25','S26','S27','S28','S29','S30','S31','S32','S33','S34','S35','S36','S37','S38','S39','S40','S41']},
{id:'ch2',nom:'Chapitre 2 — Les années d’apprentissage : quand quatre furieux décident de faire de la musique',fonction:'Décrire la métamorphose de Warsaw en Joy Division entre 1976 et 1978.',hors_champ:['Forme achevée du son Joy Division','Production Hannett pleinement constituée','Unknown Pleasures','Canonisation critique'],risques:['Récit téléologique','Mythification rétrospective','Glissement vers le chapitre 3'],sources:[]},
{id:'ch3',nom:'Chapitre 3 — La première racine du son de l’éternel : les innovations sonores',fonction:'Analyser le système sonore comme langage formel.',hors_champ:['Biographie','Lecture pathologique','Réception et héritage','Peter Saville comme acteur central'],risques:['Redite du contexte urbain','Explication biographique','Glissement vers le chapitre 5'],sources:[]},
{id:'ch4',nom:'Chapitre 4 — La deuxième racine : la poésie de l’aliénation de Ian Curtis',fonction:'Analyser la voix écrite, les motifs, les images et les structures textuelles.',hors_champ:['Diagnostic médical','Analyse musicologique','Sociologie générale','Biographie clinique'],risques:['Psychologisation','Philosophie abstraite','Glissement vers le chapitre 10'],sources:[]},
{id:'ch5',nom:'Chapitre 5 — La troisième racine : Peter Saville et l’esthétique du vide',fonction:'Étudier l’identité visuelle et l’esthétique graphique sans commémoration.',hors_champ:['Analyse sonore','Patrimonialisation contemporaine','Récit biographique de Saville'],risques:['Dérive commémorative','Glissement vers les chapitres 12 ou 14'],sources:[]},
{id:'ch6',nom:'Chapitre 6 — L’arbre se dresse : quand l’architecture sonore devient cathédrale',fonction:'Analyser la cristallisation esthétique de Joy Division en 1979-1980.',hors_champ:['Apprentissage 1976-1978','Patrimonialisation','Inventaire discographique brut'],risques:['Redite du chapitre 3','Surdramatisation tragique','Confusion entre forme et réception'],sources:[]},
{id:'ch7',nom:'Chapitre 7 — L’héritage musical à travers les décennies',fonction:'Étudier l’influence musicale de Joy Division dans les scènes postérieures.',hors_champ:['Patrimonialisation urbaine','Culture bootleg','Réception numérique'],risques:['Catalogue de groupes','Influence affirmée sans preuve','Confusion entre héritage musical et héritage culturel'],sources:[]},
{id:'ch8',nom:'Chapitre 8 — Joy Division underground : la culture bootleg comme mémoire alternative',fonction:'Analyser les bootlegs comme mémoire alternative, circulation souterraine et archive parallèle.',hors_champ:['Discographie officielle exhaustive','Collectionnite non problématisée','Mythologie fan non contrôlée'],risques:['Inventaire sec','Fétichisation de l’objet','Absence de problématisation'],sources:[]},
{id:'ch9',nom:'Chapitre 9 — Résonances globales : l’influence internationale de Joy Division',fonction:'Étudier la circulation internationale de l’influence de Joy Division.',hors_champ:['Analyse sonore détaillée','Patrimoine mancunien','Culture numérique'],risques:['Généralisation non sourcée','Liste de pays ou de groupes','Confusion avec réception contemporaine'],sources:[]},
{id:'ch10',nom:'Chapitre 10 — Joy Division à l’ère numérique : perpétuation et réinvention du mythe',fonction:'Analyser la perpétuation du mythe Joy Division dans les environnements numériques.',hors_champ:['Analyse musicale formelle','Biographie clinique détaillée','Culture bootleg comme objet principal'],risques:['Sociologie vague des fans','Présentisme','Confusion avec patrimonialisation institutionnelle'],sources:[]},
{id:'ch11',nom:'Chapitre 11 — Joy Division et la condition humaine moderne',fonction:'Interpréter ce que Joy Division dit de l’expérience humaine moderne à partir des textes et motifs récurrents.',hors_champ:['Biographie clinique','Analyse musicologique','Sociologie des fans','Philosophie abstraite non adossée aux textes'],risques:['Abstraction excessive','Surinterprétation philosophique','Confusion avec le chapitre 4'],sources:[]},
{id:'ch12',nom:'Chapitre 12 — L’éternel retour : Joy Division dans la culture contemporaine',fonction:'Analyser la patrimonialisation, les réappropriations culturelles et la mémoire contemporaine.',hors_champ:['Contexte originel de Manchester','Analyse musicale formelle','Biographie du groupe'],risques:['Récit promotionnel','Confusion patrimoine et marketing','Doublon avec le chapitre 14'],sources:[]},
{id:'ch13',nom:'Chapitre 13 — Les territoires de la mélancolie : Joy Division et la géographie émotionnelle',fonction:'Lire Joy Division à travers les relations entre espace, affect et mémoire.',hors_champ:['Contexte socio-économique brut','Analyse musicale détaillée','Patrimonialisation contemporaine'],risques:['Redite du chapitre 1','Métaphore spatiale excessive','Confusion avec le chapitre 11'],sources:[]},
{id:'ch14',nom:'Chapitre 14 — L’éternel retour : Joy Division dans la culture contemporaine',fonction:'Conclure sur la survivance culturelle de Joy Division et ses réapparitions contemporaines.',hors_champ:['Analyse détaillée du Manchester originel','Inventaire exhaustif des références','Répétition des chapitres précédents'],risques:['Doublon avec le chapitre 12','Conclusion trop commémorative','Catalogue d’occurrences contemporaines'],sources:[]}
];

const FALLBACK_ATELIERS=[
{id:'coherence',nom:'Relecture de cohérence',objectif:'Vérifier la solidité du raisonnement, le respect du périmètre et la progression démonstrative.',controles:['Respect du périmètre du chapitre','Progression logique','Cohérence argumentative','Absence de digression','Corrections ciblées']},
{id:'sources',nom:'Vérification des sources',objectif:'Sécuriser citations, références, statuts de sources et usages probatoires.',controles:['Exactitude des citations','Correspondance auteur / ouvrage','Statut de la source','Solidité scientifique','Points à consolider']},
{id:'style',nom:'Réécriture style livre',objectif:'Mettre le texte au niveau stylistique du livre sans modifier les faits.',controles:['Style académique narratif','Densité sans surcharge','Alternance des phrases courtes et longues','Absence de banalité','Respect des conventions typographiques']},
{id:'doublons',nom:'Anti-doublons',objectif:'Éliminer les redites internes et les chevauchements entre chapitres.',controles:['Répétitions internes','Chevauchements inter-chapitres','Passages à supprimer','Passages à déplacer','Version condensée éventuelle']},
{id:'notes_vers_texte',nom:'Transformation notes → texte',objectif:'Transformer des notes brutes en passage rédigé, hiérarchisé et publiable.',controles:['Hiérarchisation des idées','Absence d’effet catalogue','Lien logique entre les arguments','Style du livre','Aucune source inventée']},
{id:'document_maitre',nom:'Construction document maître',objectif:'Construire ou mettre à jour l’architecture préparatoire d’un chapitre.',controles:['Fonction du chapitre','Hors champ explicite','Axes directeurs','Corpus primaire et secondaire','Hypothèses interprétatives','Risques et points de vigilance']},
{id:'registre',nom:'Mise à jour du registre',objectif:'Actualiser la traçabilité documentaire et le statut des sources.',controles:['ID source','Référence complète','Nature de la source','Usage précis','Passages concernés','Statut opérationnel']},
{id:'notes_bas_page',nom:'Notes de bas de page',objectif:'Produire des notes exactes, sobres, contextualisées et vérifiables.',controles:['Exactitude bibliographique','Brièveté','Contextualisation','Aucune citation longue inutile','Respect des guillemets français']}
];

const FALLBACK_REGISTRE=[
{id:'S01',auteur:'Manchester City Council',statut:'sécurisée',usage:'contexte économique'},
{id:'S02',auteur:'Sénat',statut:'sécurisée',usage:'données démographiques'},
{id:'S03',auteur:'ONS',statut:'sécurisée',usage:'emploi'},
{id:'S04',auteur:'Alan Kidd',statut:'à consolider',usage:'industrialisation'},
{id:'S05',auteur:'Jeffery',statut:'sécurisée',usage:'émeutes'},
{id:'S06',auteur:'Carter',statut:'sécurisée',usage:'Hulme'}
];

async function loadJson(path,fallback){
  try{
    const response=await fetch(path,{cache:'no-store'});
    if(!response.ok){throw new Error(path+' non chargé');}
    return await response.json();
  }catch(error){
    console.warn('Chargement local JSON impossible, utilisation du secours intégré :',path,error);
    return fallback;
  }
}

async function load(){
  chapData=await loadJson('data/chapitres.json',FALLBACK_CHAPITRES);
  atelierData=await loadJson('data/ateliers.json',FALLBACK_ATELIERS);
  registreData=await loadJson('data/registre.json',FALLBACK_REGISTRE);
  populateSelect('chapitre',chapData);
  populateSelect('atelier',atelierData);
}

function populateSelect(id,data){
  const select=document.getElementById(id);
  select.innerHTML='';
  data.forEach(item=>select.add(new Option(item.nom,item.id)));
}

function generate(){
  const chap=chapData.find(c=>c.id===document.getElementById('chapitre').value);
  const at=atelierData.find(a=>a.id===document.getElementById('atelier').value);
  if(!chap||!at){
    document.getElementById('output').value='Erreur : les chapitres ou ateliers ne sont pas chargés.';
    return;
  }
  const input=document.getElementById('input').value;
  const mode=document.getElementById('mode').value;
  document.getElementById('output').value=buildPrompt({chap,at,input,mode,registre:registreData});
}

document.getElementById('generateBtn').onclick=generate;
document.getElementById('copyBtn').onclick=function(){navigator.clipboard.writeText(document.getElementById('output').value)};
load();
