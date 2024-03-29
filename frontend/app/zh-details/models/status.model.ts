export interface StatutsModel {
  regime: Regime[];
  structure: Structure[];
  instruments: Instrument[];
  autre_inventaire: AutreInventaires[]; //boolean
  statuts: string[];
  zonage: Zonage[];
  autre_etude: string;
}

interface AutreInventaires {
  area_name: string;
  area_code: string;
  url: string;
  type_code: string;
  zh_type_name: string;
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
