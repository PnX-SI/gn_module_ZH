export interface DelimitationModel {
  delitmitation_zone: Criteres;
  delimitation_fonctions: Criteres;
}

interface Criteres {
  critere: string[];
  remarque: null | string;
}
