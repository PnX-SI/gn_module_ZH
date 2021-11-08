import { Component, OnInit, Output, EventEmitter } from "@angular/core";
import { FormGroup, FormBuilder } from "@angular/forms";

@Component({
  selector: "zh-search-departement",
  templateUrl: "./zh-search-departement.component.html",
  styleUrls: ["./zh-search-departement.component.scss"],
})
export class ZhSearchDepartementComponent implements OnInit {
  @Output() onSelected = new EventEmitter<object>();

  public departments: any[];
  public departmentDropdownSettings = {
    enableSearchFilter: true,
    addNewItemOnFilter: true,
    singleSelection: true,
    text: "Sélectionner un département",
    labelKey: "name",
    primaryKey: "code",
    enableFilterSelectAll: false,
  };
  public departmentsForm: FormGroup;

  constructor(private _fb: FormBuilder) {}

  ngOnInit() {
    this.departmentsForm = this._fb.group({
      department: [""],
    });
    this.departmentsForm.get("department").valueChanges.subscribe((x) => {
      this.onSelected.emit(x);
    });
    this.departments = [
      { code: "13", name: "Bouches du Rhône" },
      { code: "83", name: "Var" },
      { code: "06", name: "Alpes Maritimes" },
    ];
  }

  onDeselect() {
    this.departmentsForm.patchValue({ department: undefined });
  }
}
