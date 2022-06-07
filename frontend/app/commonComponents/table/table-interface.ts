export interface TableColumn {
  name: string;
  label: string;
  // size (Width) of the column
  size?: string;
  subcell?: SubCell;
  subarr?: SubCell;
}

export interface SubCell {
  name: string;
}
