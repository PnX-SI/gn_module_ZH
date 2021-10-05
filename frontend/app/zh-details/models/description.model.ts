export interface DescriptionModel {
  "3.2- Présentation de la zone humide et de ses milieux": Presentation;
  "3.3- Description de l'espace de fonctionnalité": Espace;
  "3.4- Usage et processus naturels": Usage;
}

interface Presentation {
  "Typologie SDAGE": string;
  "Typologie locale": string;
  "Corine Biotope": string;
  Remarques: null | string;
}

interface Espace {
  "Occupation des sols": string;
}

interface Usage {
  Activités: string;
  "Evaluation globale des menaces potentielles ou avérées": string;
  Remarques: null | string;
}
