export interface EvaluationModel {
  "7.1- Fonctions et valeurs majeures": FonctionsEtValeursMajeures;
  "7.2- Intérêt patrimonial majeur": InteretPatrimonialMajeur;

  "7.3- Bilan des menaces et des facteurs infuançant la zone humide": BilanMenaces;
  "7.4- Stratégie de gestion et orientations d'actions": Strategie;
}

interface FonctionsEtValeursMajeures {
  "Principales fonctions hydrologiques / biogéochimiques": [
    HydrologiquesBiogeochimiques
  ];
  "Principales fonctions biologiques / écologiques": [BiologiquesEcologiques];
}

interface HydrologiquesBiogeochimiques {
  fonctions_hydro: string;
  Justification: string;
  Qualification: string;
  Connaissance: string;
}

interface BiologiquesEcologiques {
  fonctions_bio: string;
  Justification: string;
  Qualification: string;
  Connaissance: string;
}

interface InteretPatrimonialMajeur {
  "Intérêts patrimoniaux": InteretsPatrimoniaux;
  "Nombre d'espèces faunistiques": number;
  "Nombre d'espèces floristiques": number;
  "Nombre d'habitats humides patrimoniaux": number;
  "Recouvrement total de la ZH (%)": number;
  Commentaire: null | string;
}

interface InteretsPatrimoniaux {
  interet_patrim: string;
  Justification: string;
  Qualification: string;
  Connaissance: string;
}

interface BilanMenaces {
  "Evaluation globale des menaces potentielles ou avérées": string;
  "Fonctionnalité hydrologique / biogéochimique": string;
  "Fonctionnalité biologique / écologique (habitats / faune / flore)": string;
  Commentaire: null | string;
}

interface Strategie {
  "Propositions d'actions": string;
  Commentaires: null | string;
}
