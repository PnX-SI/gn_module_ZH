import { Component, OnInit, Input } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';

@Component({
  selector: 'zh-advanced-search-evaluations',
  templateUrl: './zh-advanced-search-evaluations.component.html',
  styleUrls: ['./zh-advanced-search-evaluations.component.scss'],
})
export class ZhAdvancedSearchEvaluationsComponent implements OnInit {
  @Input() form: FormGroup;
  @Input() hydros: [];
  @Input() bios: [];
  @Input() menaces: [];

  public dropdownSettings: {};
  constructor() {}

  ngOnInit() {
    this.dropdownSettings = {
      enableCheckAll: false,
      text: 'Sélectionner',
      labelKey: 'mnemonique',
      primaryKey: 'id_nomenclature',
      searchPlaceholderText: 'Rechercher',
      enableSearchFilter: true,
      autoPosition: true,
    };
  }

  onDeSelectAllHydro() {
    this.form.get('hydros').reset();
  }
  onDeSelectAllBio() {
    this.form.get('bios').reset();
  }
  onDeSelectAllMenaces() {
    this.form.get('menaces').reset();
  }
}
