import { Component, OnInit, Input } from "@angular/core";
import { FormGroup } from "@angular/forms";

@Component({
  selector: "zh-advanced-search-fonctions",
  templateUrl: "./zh-advanced-search-fonctions.component.html",
  styleUrls: ["./zh-advanced-search-fonctions.component.scss"],
})
export class ZhAdvancedSearchFonctionsComponent implements OnInit {
  @Input() data: any;
  @Input() qualifications: [];
  @Input() connaissances: [];
  @Input() title: string = "";
  @Input() fonctionLabel: string = "Fonction";
  @Input() form: FormGroup;
  public dropdownSettings: {};
  public dropdownSettingsNoCategory: {};
  constructor() {}

  ngOnInit() {
    let settings = {
      enableCheckAll: false,
      text: "Sélectionner",
      labelKey: "mnemonique",
      primaryKey: "id_nomenclature",
      searchPlaceholderText: "Rechercher",
      enableSearchFilter: true,
      autoPosition: false,
      groupBy: null,
    };
    if (this.data.every((obj) => "category" in obj)) {
      settings.groupBy = "category";
    }
    this.dropdownSettings = settings;
    this.dropdownSettingsNoCategory = {
      enableCheckAll: false,
      text: "Sélectionner",
      labelKey: "mnemonique",
      primaryKey: "id_nomenclature",
      autoPosition: false,
    };
  }
}
