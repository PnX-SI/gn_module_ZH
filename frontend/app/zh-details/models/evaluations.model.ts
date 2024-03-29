export interface EvaluationModel {
  fonctions: FonctionsEtValeursMajeures;
  interet: InteretPatrimonialMajeur;
  bilan: BilanMenaces;
  strategie: Strategie;
}

interface FonctionsEtValeursMajeures {
  hydrologique: Fonctions[];
  biologique: Fonctions[];
}

interface Fonctions {
  type: string;
  justification: string;
  qualification: string;
  connaissance: string;
}

interface InteretPatrimonialMajeur {
  interet: Fonctions[];
  faunistique: number;
  floristique: number;
  nb_hab: number;
  total_hab_cover: number;
  Commentaire: null | string;
  valeur: Fonctions[];
}

interface BilanMenaces {
  menaces: string;
  hydrologique: string;
  biologique: string;
  Commentaire: null | string;
}

interface Strategie {
  propositions: Proposition[];
  commentaires: null | string;
  strategie: null | string;
  mgmt_strategy: any;
}

interface Proposition {
  proposition: string;
  niveau: string;
  remarque: string;
}
