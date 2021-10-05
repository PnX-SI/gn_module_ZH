export interface FonctionnementModel {
  "4.1- Régime hydrique": Regime;
  "4.2- Connexion de la zone humide dans son environnement": string;
  "4.3- Diagnostic fonctionnel": Diagnostic;
}

interface Regime {
  "Entrée d'eau": string;
  "Sortie d'eau": string;
  "Submersion fréquence": string;
  "Submersion étendue": string;
}

interface Diagnostic {
  "Fonctionnalité hydrologique / biogéochimique": string;
  "Fonctionnalité biologique / écologique": string;
  Commentaires: null | string;
}
