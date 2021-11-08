import { Component, OnInit, Input } from "@angular/core";
import { FormGroup } from "@angular/forms";

@Component({
  selector: "zh-search-sdage",
  templateUrl: "./zh-search-sdage.component.html",
  styleUrls: ["./zh-search-sdage.component.scss"],
})
export class ZhSearchSDAGEComponent implements OnInit {
  @Input() data: any;
  @Input() form: FormGroup;

  public dropdownSettings;

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
}
