import { Injectable } from "@angular/core";
import { FormBuilder, FormGroup, Validators } from "@angular/forms";

@Injectable({
  providedIn: "root",
})
export class SearchFormService {
  private _advancedForm: FormGroup;
  private _searchForm: FormGroup;
  private _hierarchyForm: FormGroup;
  constructor(private _fb: FormBuilder) {}

  get searchForm() {
    return this._searchForm;
  }

  get advancedForm() {
    return this._advancedForm;
  }

  get hierarchyForm() {
    return this._hierarchyForm;
  }

  initForm() {
    this._searchForm = this._fb.group({
      basin: [null],
      departement: [null],
      communes: [null],
      sdage: [null],
      nameorcode: [null],
      zones: [null],
      ensemble: [null],
      ha_area: this._fb.group({
        ha: [
          null,
          {
            validators: [Validators.min(0)],
          },
        ],
        symbol: [null],
      }),
    });
    this._advancedForm = this._fb.group({
      hydro: this._fb.group({
        functions: [null],
        qualifications: [null],
        connaissances: [null],
      }),
      bio: this._fb.group({
        functions: [null],
        qualifications: [null],
        connaissances: [null],
      }),
      socio: this._fb.group({
        functions: [null],
        qualifications: [null],
        connaissances: [null],
      }),
      interet: this._fb.group({
        functions: [null],
        qualifications: [null],
        connaissances: [null],
      }),
      statuts: this._fb.group({
        statuts: [null],
        plans: [null],
        strategies: [null],
      }),
      evaluations: this._fb.group({
        hydros: [null],
        bios: [null],
        menaces: [null],
      }),
    });
    this.initHierarchyForm();
  }

  initHierarchyForm() {
    this._hierarchyForm = this._fb.group({
      hierarchy: this._fb.group({
        hierarchy: this._fb.array([]),
        and: [false], // if !"and" => OR
      }),
    });
  }

  filterFormGroup(values) {
    const filtered = {};
    // Since everything is a form group:
    Object.keys(values).forEach((key) => {
      let value = values[key];
      if (value) {
        if (value instanceof Array) {
          if (value.length !== 0) {
            value = value.filter((item) => item !== null);
            filtered[key] = value;
          }
        } else if (value instanceof Object) {
          value = this.filterFormGroup(value);
          if (Object.keys(value).length !== 0) {
            filtered[key] = value;
          }
        } else {
          filtered[key] = value;
        }
      }
    });

    return filtered;
  }

  getJson() {
    if (!this.searchForm.invalid) {
      const searchObj = Object.assign(
        {},
        this.searchForm.value,
        this.advancedForm.value,
        this.hierarchyForm.value
      );
      return this.filterFormGroup(searchObj);
    }
  }

  reset() {
    this.searchForm.reset();
    this.advancedForm.reset();
    // reset does not work with FormArray...
    this.initHierarchyForm();
  }
}
