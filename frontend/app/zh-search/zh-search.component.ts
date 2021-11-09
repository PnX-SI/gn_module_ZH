import { Component, OnInit, Input } from "@angular/core";
import { FormBuilder, FormGroup, Validators } from "@angular/forms";

import { ZhDataService } from "../services/zh-data.service";

@Component({
  selector: "zh-search",
  templateUrl: "./zh-search.component.html",
  styleUrls: ["./zh-search.component.scss"],
})
export class ZhSearchComponent implements OnInit {
  @Input() data: any;
  public advancedSearchToggled: boolean = false;
  public bassins: [];
  public hydrographicZones: [];
  public departements: [];
  public communes: [];
  public advancedForm: FormGroup;
  public searchForm: FormGroup;

  constructor(private _dataService: ZhDataService, private _fb: FormBuilder) {}

  ngOnInit() {
    this._dataService
      .getDepartments()
      .toPromise()
      .then((resp: any) => {
        this.departements = resp;
      })
      .catch((error) => console.log(error));

    this._dataService
      .getBassins()
      .toPromise()
      .then((resp: any) => {
        this.bassins = resp;
      })
      .catch((error) => console.log(error));

    this.initForm();
  }

  onDepartmentSelected(event) {
    if (event) {
      const department = event[0].code;
      this._dataService
        .getCommuneFromDepartment(department)
        .toPromise()
        .then((resp: any) => (this.communes = resp));
    } else {
      // reset it for the select to be disabled
      this.communes = undefined;
    }
  }

  onBassinSelected(event) {
    if (event) {
      this.hydrographicZones = [];
    } else {
      this.hydrographicZones = undefined;
    }
  }

  onSearch() {
    if (!this.searchForm.invalid) {
      const searchObj = Object.assign(
        {},
        this.searchForm.value,
        this.advancedForm.value
      );
      const filtered = this.filterFormGroup(searchObj);
      console.log(filtered);

      this._dataService
        .search(filtered)
        .toPromise()
        .then((res) => {
          console.log(res);
        })
        .catch((error) => console.log(error));
    }
  }

  onAdvancedFormChanged(event) {
    this.advancedForm = event;
  }

  initForm() {
    this.searchForm = this._fb.group({
      bassin: [null],
      departement: [null],
      communes: [null],
      sdage: [null],
      code: [
        null,
        {
          validators: [Validators.pattern("^[0-9]{2}[A-Z]{2}[0-9]{5}")],
          updateOn: "change",
        },
      ],
      zones: [null],
      ensemble: [null],
      area: [
        null,
        {
          validators: [Validators.min(0)],
          updateOn: "change",
        },
      ],
    });
    this.advancedForm = this._fb.group({
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
          value = value.filter((item) => item != null);
        } else if (value instanceof Object) {
          value = this.filterFormGroup(value);
        }
        if (Object.keys(value).length !== 0) {
          filtered[key] = value;
        }
      }
    });

    return filtered;
  }
}
