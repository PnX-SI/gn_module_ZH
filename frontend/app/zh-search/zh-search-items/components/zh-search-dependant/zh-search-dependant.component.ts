import { Component, OnInit, Input, Output, EventEmitter } from "@angular/core";
import { FormGroup, FormBuilder } from "@angular/forms";

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
    addNewItemOnFilter: true,
    text: "",
    labelKey: "name",
    primaryKey: "code",
    enableFilterSelectAll: false,
    disabled: true,
  };

  constructor() {}

  ngOnInit() {}

  setData(value) {
    if (this._inputData != undefined) {
      this.enable();
      this._inputData = value;
    } else {
      this.disable();
    }
  }

  //Awkward but taken from the doc : https://cuppalabs.github.io/angular2-multiselect-dropdown/#/disablemode
  disable() {
    this.dropdownSettings = {
      enableSearchFilter: true,
      addNewItemOnFilter: true,
      text: "",
      labelKey: "name",
      primaryKey: "code",
      enableFilterSelectAll: false,
      disabled: true,
    };
  }
  enable() {
    this.dropdownSettings = {
      enableSearchFilter: true,
      addNewItemOnFilter: true,
      text: "",
      labelKey: "name",
      primaryKey: "code",
      enableFilterSelectAll: false,
      disabled: false,
    };
  }
}
