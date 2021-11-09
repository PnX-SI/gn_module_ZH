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

  onSearch() {}

  onAdvancedFormChanged(event) {
    this.advancedForm = event;
  }

  initForm() {
    this.searchForm = this._fb.group({
      bassin: [null],
      departement: [null],
      commune: [null],
      sdage: this._fb.group({ sdage: [null] }),
      code: this._fb.group({
        code: [
          null,
          {
            validators: [Validators.pattern("^[0-9]{2}[A-Z]{2}[0-9]{5}")],
            updateOn: "change",
          },
        ],
      }),
      hydro: [null],
      ensemble: this._fb.group({ ensemble: [null] }),
      area: this._fb.group({
        ha: [
          "",
          {
            validators: [Validators.min(0)],
            updateOn: "change",
          },
        ],
      }),
    });
  }
}
