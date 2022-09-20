import { Component, OnInit, Input, Output, EventEmitter } from "@angular/core";
import { FormBuilder, FormGroup, Validators } from "@angular/forms";
import { NgbModal } from "@ng-bootstrap/ng-bootstrap";
import { ToastrService } from "ngx-toastr";
import { HydrographicZone } from "../models/zones";

import { ErrorTranslatorService } from "../services/error-translator.service";

import { ZhDataService } from "../services/zh-data.service";
import { SearchFormService } from "../services/zh-search.service";

@Component({
  selector: "zh-search",
  templateUrl: "./zh-search.component.html",
  styleUrls: ["./zh-search.component.scss"],
})
export class ZhSearchComponent implements OnInit {
  @Input() data: any;
  @Output() onClose = new EventEmitter<object>();
  @Output() onSearch = new EventEmitter();
  public advancedSearchToggled: boolean = false;
  public hierarchySearchToggled: boolean = false;
  public basins: [];
  public hydrographicZones: HydrographicZone[] | undefined;
  public departements: [] | undefined;
  public communes: [] | undefined;

  constructor(
    private _dataService: ZhDataService,
    private _fb: FormBuilder,
    private _toastr: ToastrService,
    private _error: ErrorTranslatorService,
    public ngbModal: NgbModal,
    private _searchService: SearchFormService
  ) {}

  ngOnInit() {
    this._dataService
      .getDepartments()
      .toPromise()
      .then((resp: any) => {
        this.departements = resp;
      })
      .catch((error) => {
        const frontMsg: string = this._error.getFrontError(error.error.message);
        this.displayError(frontMsg);
      });

    this._dataService
      .getBasins()
      .toPromise()
      .then((resp: any) => {
        this.basins = resp;
      })
      .catch((error) => {
        const frontMsg: string = this._error.getFrontError(error.error.message);
        this.displayError(frontMsg);
      });
  }

  onDepartmentSelected(event) {
    // Reset form
    this._searchService.searchForm.get("communes").reset();
    // reset it for the select to be disabled
    this.communes = undefined;
    if (event && event.length > 0) {
      const department = event[0].code;
      this._dataService
        .getCommuneFromDepartment(department)
        .toPromise()
        .then((resp: any) => (this.communes = resp));
    }
  }

  onBasinSelected(event) {
    // Reset form
    this._searchService.searchForm.get("zones").reset();
    // reset it for the select to be disabled
    this.hydrographicZones = undefined;
    if (event && event.length > 0) {
      const basin = event[0].code;
      this._dataService
        .getHydroZoneFromBasin(basin)
        .toPromise()
        .then((resp: any) => (this.hydrographicZones = resp));
    }
  }

  search() {
    if (!this._searchService.searchForm.invalid) {
      this.onSearch.emit();
    }
  }

  onReset() {
    this._searchService.reset();
    // Emit empty object to search all ZH
    this.onSearch.emit();
  }

  onCloseClicked() {
    this.onClose.emit();
  }

  displayError(error: string) {
    this._toastr.error(error);
  }

  openModalHelp(event, modal) {
    this.ngbModal.open(modal);
  }

  onAdvancedSearchToggled() {
    this.advancedSearchToggled = !this.advancedSearchToggled;
    if (this.hierarchySearchToggled) {
      this.hierarchySearchToggled = false;
      this._searchService.initHierarchyForm();
    }
  }

  onHierarchySearchToggled() {
    this.hierarchySearchToggled = !this.hierarchySearchToggled;
    if (this.advancedSearchToggled) {
      this.advancedSearchToggled = false;
      this._searchService.advancedForm.reset();
    }
  }
}
