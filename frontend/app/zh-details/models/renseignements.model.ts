export interface RenseignementsGenerauxModel {
  "1.1- Identification de la zone humide": IdentificationZH;
  "1.2- Auteur": Auteur;
  "1.4- Principales références bibliographiques": string;
}

interface IdentificationZH {
  Identification: Identification;
  "Localisation de la zone humide": Localisation;
}

interface Identification {
  "Nom usuel de la zone humide": string;
  "Autre nom": null | string;
  "Partie d'un ensemble": string;
  "Code de la zone humide": "30-GE3-2";
}

interface Localisation {
  Region: string[];
  Département: Object;
  Commune: Commune;
}

interface Commune {
  Commune: string;
  "Code INSEE": string;
  "Couverture ZH par rapport à la surface de la commune": string;
}

interface Auteur {
  "Auteur de la fiche": string;
  "Auteur des dernières modifications": string;
  "Date d'établissement": string;
  "Date des dernières modifications": string;
}
