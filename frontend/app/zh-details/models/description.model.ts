export interface DescriptionModel {
  presentation: Presentation;
  espace: Espace;
  usage: Usage;
}

interface Presentation {
  sdage: string;
  typologie_locale: string;
  corine_biotope: Corine[];
  remarques: null | string;
}

interface Espace {
  ocupation: string[];
}

interface Usage {
  activities: Activities[];
  evaluation_menaces: string;
  Remarques: null | string;
}

interface Corine {
  code: string;
  label: string;
  Humidité: string;
}

interface Activities {
  activite: string;
  impacts: string[];
  localisation: string;
  remarques: string;
}
