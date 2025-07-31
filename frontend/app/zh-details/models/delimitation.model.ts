export interface DelimitationModel {
  delimitation_zone: Criteres;
  delimitation_fonctions: Criteres;
  input_scale: null | string;
  input_ref_geo: null | string;
  basin: any;
}

interface Criteres {
  critere: string[];
  remark: null | string;
}
