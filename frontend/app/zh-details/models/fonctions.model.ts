export interface FonctionsModel {
  hydrologie: Fonction[];
  biologie: Fonction[];
  interet: Fonction[];
  habitats: Habitats;
  socio: Fonction[];
}

interface Fonction {
  type: string;
  qualification: string;
  connaissance: string;
  justifications: string;
}

interface Habitats {
  cartographie: boolean;
  nombre: string; // number;
  recouvrement: string; // number;
  corine: Corine[];
}

interface Corine {
  biotope: string;
  etat: string;
  cahier: string;
  recouvrement: string; // number;
}

interface FauneFlore {
  nb_flore: string; // number;
  nb_vertebre: string; // number;
  nb_invertebre: string; // number;
}
