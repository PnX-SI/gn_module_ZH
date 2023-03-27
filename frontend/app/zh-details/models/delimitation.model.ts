export interface DelimitationModel {
  delimitation_zone: Criteres;
  delimitation_fonctions: Criteres;
  basin: any;
}

interface Criteres {
  critere: string[];
  remark: null | string;
}
