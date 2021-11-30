export interface HierarchyModel {
  river_basin_name: string;
  volet1: Volet1;
  volet2: Volet2;
  global_note: number;
  denominator: number;
  final_note: number;
}

export interface ItemModel {
  name: string;
  active: boolean;
  qualification: string;
  knowledge: string;
  note: number;
  denominator: number;
}

interface CatModel {
  name: string;
  items: ItemModel[];
  note: number;
  denominator: number;
}

interface Volet1 {
  cat1_sdage: CatModel;
  cat2_heritage: CatModel;
  cat3_eco: CatModel;
  cat4_hydro: CatModel;
  cat5_soc_eco: CatModel;
  denominator: number;
  note: number;
}

interface Volet2 {
  cat6_status: CatModel;
  cat7_fct_state: CatModel;
  cat8_thread: CatModel;
  denominator: number;
  note: number;
}
