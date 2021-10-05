export interface DelimitationModel {
  "2.1- Critères de délimitation de la zone humide": Criteres;
  "2.2- Critère de délimitation de l'espace de fonctionnalité": Criteres;
}

interface Criteres {
  "Critères utilisés": string[];
  Remarque: null | string;
}
