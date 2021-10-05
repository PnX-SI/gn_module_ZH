export interface FonctionsModel {
  "5.1- Fonctions hydrologiques / biogéochimiques": string;
  "5.2- Fonctions biologiques / écologiques": string;
  "5.3- Valeurs socio-économiques": "Non renseigné";
  "5.4- Intérêt patrimonial": string;
  "5.4.1- Habitats naturels humides patrimoniaux": Habitats;
  "5.4.2- Faune et flore patrimoniale": FauneFlore;
}

interface Habitats {
  "Cartographie d'habitats": string;
  "Nombre d'habitats": string;
  "Recouvrement total de la ZH (%)": string;
  "Habitats naturels patrimoniaux": string;
}

interface FauneFlore {
  "Flore - nombre d'espèces": string;
  "Faune - nombre d'espèces de vertébrés": string;
  "Faune - nombre d'espèces d'invertébrés": string;
}
