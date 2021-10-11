export interface FonctionnementModel {
  regime: Regime;
  connexion: string;
  diagnostic: Diagnostic;
}

interface Regime {
  entree: EntreeSortie[];
  sortie: EntreeSortie[];
  frequence: string;
  etendue: string;
  // origine: string;
}

interface EntreeSortie {
  type: string;
  permanence: string;
  toponymie: string;
}

interface Diagnostic {
  hydrologique: string;
  biologique: string;
  commentaires: null | string;
}
