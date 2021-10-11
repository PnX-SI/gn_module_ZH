// TODO importer des interfaces déjà faites ailleurs

export interface EvaluationModel {
  fonctions: FonctionsEtValeursMajeures;
  interet: InteretPatrimonialMajeur;
  bilan: BilanMenaces;
  strategie: Strategie;
}

interface FonctionsEtValeursMajeures {
  hydrologique: HydrologiquesBiogeochimiques[];
  biologique: BiologiquesEcologiques[];
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
  interet: InteretsPatrimoniaux;
  faunistique: number;
  floristique: number;
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
