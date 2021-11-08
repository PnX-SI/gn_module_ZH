import { Component, OnInit, Input, Output, EventEmitter } from "@angular/core";
import { FormGroup, FormBuilder } from "@angular/forms";

@Component({
  selector: "zh-search-commune",
  templateUrl: "./zh-search-commune.component.html",
  styleUrls: ["./zh-search-commune.component.scss"],
})
export class ZhSearchCommuneComponent implements OnInit {
  @Input() set department(value: string) {
    this._department = value;
    this.setCommunes(value);
  }
  @Output() onSelected = new EventEmitter<object>();
  public _department: any = null;
  public communes: any[];
  public communesForm: FormGroup;
  public communesDropdownSettings = {
    enableSearchFilter: true,
    addNewItemOnFilter: true,
    text: "Sélectionner une commune",
    labelKey: "name",
    primaryKey: "code",
    enableFilterSelectAll: false,
    disabled: true,
  };

  constructor(private _fb: FormBuilder) {}

  ngOnInit() {
    this.communesForm = this._fb.group({
      commune: [""],
    });
  }

  setCommunes(value) {
    if (this._department != undefined) {
      this.enable();
      this.communes = [
        { code: "83143", name: "Le Val" },
        { code: "13007", name: "Marseille" },
      ];
    } else {
      this.disable();
    }
  }

  //Awkward but taken from the doc : https://cuppalabs.github.io/angular2-multiselect-dropdown/#/disablemode
  disable() {
    this.communesDropdownSettings = {
      enableSearchFilter: true,
      addNewItemOnFilter: true,
      text: "Sélectionner une commune",
      labelKey: "name",
      primaryKey: "code",
      enableFilterSelectAll: false,
      disabled: true,
    };
  }
  enable() {
    this.communesDropdownSettings = {
      enableSearchFilter: true,
      addNewItemOnFilter: true,
      text: "Sélectionner une commune",
      labelKey: "name",
      primaryKey: "code",
      enableFilterSelectAll: false,
      disabled: false,
    };
  }
}
