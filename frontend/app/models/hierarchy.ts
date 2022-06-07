export type HierarchyFields = {
  categories: HierarchyField[];
  items: Note[];
};

export type HierarchyField = {
  name: string;
  subcategory: HierarchyField[];
};

export type Note = {
  id_rb: number;
  name: string;
  cor_rule_id: number;
  rule_id: number;
  volet: string;
  rubrique: string;
  sousrubrique?: string;
  id_attribut: number;
  attribut: string;
  note: number;
  note_type?: string;
  note_type_id: number;
};

export type RiverBasin = {
  code: number;
  name: string;
};
