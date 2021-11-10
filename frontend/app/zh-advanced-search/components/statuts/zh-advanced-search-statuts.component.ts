import { Component, OnInit, Input } from "@angular/core";
import { FormGroup } from "@angular/forms";

@Component({
  selector: "zh-advanced-search-statuts",
  templateUrl: "./zh-advanced-search-statuts.component.html",
  styleUrls: ["./zh-advanced-search-statuts.component.scss"],
})
export class ZhAdvancedSearchStatutsComponent implements OnInit {
  @Input() statuts: any;
  @Input() plans: [];
  @Input() form: FormGroup;
  public dropdownSettings: {};
  constructor() {}

  ngOnInit() {
    this.dropdownSettings = {
      enableCheckAll: false,
      text: "Sélectionner",
      labelKey: "mnemonique",
      primaryKey: "id_nomenclature",
      searchPlaceholderText: "Rechercher",
      enableSearchFilter: true,
      autoPosition: true,
    };
  }

  onDeSelectAllStatuts() {
    this.form.get("statuts").reset();
  }
  onDeSelectAllPlans() {
    this.form.get("plans").reset();
  }
}
