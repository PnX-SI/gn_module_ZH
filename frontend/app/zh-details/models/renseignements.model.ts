export interface RenseignementsGenerauxModel {
  identification: Identification;
  localisation: Localisation;
  auteur: Auteur;
  references: Reference[];
}

interface Localisation {
  region: string[];
  departement: string[];
  commune: Commune[];
}

interface Commune {
  nom: string;
  insee: string;
  couverture: string;
}

interface Identification {
  nom: string;
  autre: null | string;
  inclus: string; //partie d'un ensemble String or Boolean ??
  ensemble: string;
  code: string;
}

interface Auteur {
  auteur: string;
  auteur_modif: string;
  date: string;
  date_modif: string;
}

interface Reference {
  reference: string;
  titre: string;
  auteurs: string;
  annee: string;
  bassins: string;
  editeur: string;
  lieu: string;
}
