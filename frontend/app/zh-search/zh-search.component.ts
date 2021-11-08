import { Component, OnInit, Input } from "@angular/core";
import { ZhDataService } from "../services/zh-data.service";

@Component({
  selector: "zh-search",
  templateUrl: "./zh-search.component.html",
  styleUrls: ["./zh-search.component.scss"],
})
export class ZhSearchComponent implements OnInit {
  @Input() forms: any;
  public advancedSearchToggled: boolean = false;
  public bassins: [];
  public hydrographicZones: [];
  public departements: [];
  public communes: [];

  constructor(private _dataService: ZhDataService) {}

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
}
