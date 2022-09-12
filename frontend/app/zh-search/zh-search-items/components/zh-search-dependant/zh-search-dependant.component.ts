import { Component, OnInit, Input, Output, EventEmitter } from "@angular/core";
import { FormGroup } from "@angular/forms";

type inputDataType = {
  name: string;
  code: string;
};

@Component({
  selector: "zh-search-dependant",
  templateUrl: "./zh-search-dependant.component.html",
  styleUrls: ["./zh-search-dependant.component.scss"],
})
export class ZhSearchDependantComponent implements OnInit {
  @Input() label: string = "";
  @Input() form: FormGroup;
  @Input() set inputData(value: inputDataType[]) {
    this._inputData = value;
    this.setData(value);
  }
  @Output() onSelected = new EventEmitter<object>();
  public _inputData: inputDataType[] = null;
  public dataForm: FormGroup;
  public dropdownSettings = {
    enableSearchFilter: true,
    text: "",
    labelKey: "name",
    primaryKey: "code",
    enableFilterSelectAll: false,
    selectAllText: "Tout sélectionner",
    unSelectAllText: "Tout désélectionner",
    searchPlaceholderText: "Rechercher",
    disabled: true,
  };

  constructor() {}

  ngOnInit() {}

  setData(value) {
    if (this._inputData != undefined) {
      this.enable();
      this._inputData = value;
    } else {
      this.form.reset();
      this.disable();
    }
  }

  onDeselectAll() {
    this.form.reset();
  }

  //Awkward but taken from the doc : https://cuppalabs.github.io/angular2-multiselect-dropdown/#/disablemode
  disable() {
    this.dropdownSettings = { ...this.dropdownSettings, disabled: true };
  }
  enable() {
    this.dropdownSettings = { ...this.dropdownSettings, disabled: false };
  }
}
