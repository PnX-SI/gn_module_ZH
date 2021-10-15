export interface StatutsModel {
  regime: Regime[];
  structure: Structure[];
  instruments: Instrument[];
  autre_invetaire: string; //boolean
  statuts: string[];
  zonage: Zonage[];
}

interface Regime {
  status: string;
  remarques: string;
}
interface Structure {
  structure: string;
  plans: Plan[];
}
interface Plan {
  plan: string;
  date: string;
  duree: string;
}
interface Instrument {
  instrument: string;
  date: string;
}
interface Zonage {
  commune: string;
  type_doc: string;
  type_classement: string[];
  remarque: string;
}
