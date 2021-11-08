import { Component, OnInit, Input } from "@angular/core";
import { FormBuilder, FormGroup } from "@angular/forms";

@Component({
  selector: "zh-advanced-search-evaluations",
  templateUrl: "./zh-advanced-search-evaluations.component.html",
  styleUrls: ["./zh-advanced-search-evaluations.component.scss"],
})
export class ZhAdvancedSearchEvaluationsComponent implements OnInit {
  @Input() hydros: [];
  @Input() bio: [];
  @Input() menaces: [];

  public form: FormGroup;
  public dropdownSettings: {};
  constructor(private _fb: FormBuilder) {}

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
    this.form = this._fb.group({
      hydros: [""],
      bios: [""],
      menaces: [""],
    });
  }
}
