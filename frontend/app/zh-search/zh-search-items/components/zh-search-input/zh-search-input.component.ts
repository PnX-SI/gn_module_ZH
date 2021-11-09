import { Component, OnInit, Input, Output, EventEmitter } from "@angular/core";
import { FormGroup, FormBuilder } from "@angular/forms";

@Component({
  selector: "zh-search-input",
  templateUrl: "./zh-search-input.component.html",
  styleUrls: ["./zh-search-input.component.scss"],
})
export class ZhSearchInputComponent implements OnInit {
  @Input() data: any[];
  @Input() label: string = "";
  @Input() displayCode: boolean = false;
  @Input() form: FormGroup;
  @Output() onSelected = new EventEmitter<object>();

  public dropdownSettings = {
    enableSearchFilter: true,
    addNewItemOnFilter: true,
    singleSelection: true,
    text: "",
    labelKey: "name",
    primaryKey: "code",
    enableFilterSelectAll: false,
  };

  constructor() {}

  ngOnInit() {
    this.form.valueChanges.subscribe((x) => {
      this.onSelected.emit(x);
    });
  }

  onDeselect() {
    this.form.patchValue({ data: undefined });
  }
}
