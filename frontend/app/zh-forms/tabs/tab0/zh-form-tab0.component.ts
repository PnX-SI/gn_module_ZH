import { Component, EventEmitter, HostListener, Input, OnInit, Output } from "@angular/core";
import { FormGroup, FormBuilder, Validators } from "@angular/forms";
import { Router } from "@angular/router";
import { Subscription } from "rxjs";
import { GeoJSON } from "leaflet";
import { MapService } from '@geonature_common/map/map.service';
import { IDropdownSettings } from 'ng-multiselect-dropdown';
import { ToastrService } from 'ngx-toastr';
import { ZhDataService } from "../../../services/zh-data.service";



@Component({
  selector: "zh-form-tab0",
  templateUrl: "./zh-form-tab0.component.html",
  styleUrls: ["./zh-form-tab0.component.scss"]
})
export class ZhFormTab0Component implements OnInit {

  @Input() formMetaData;
  @Output() nextTab = new EventEmitter<number>();
  @Output() activeTabs = new EventEmitter<boolean>();
  private _currentZh: any;
  public form: FormGroup;
  public cardContentHeight: number;
  public critDelim: any;
  public sdage: any;
  public idOrg: any;
  public dropdownSettings: IDropdownSettings;
  private $_geojsonSub: Subscription;
  public $_currentZhSub: Subscription;
  private geometry: GeoJSON;
  public submitted = false;
  public posted = false;

  constructor(
    private fb: FormBuilder,
    private _dataService: ZhDataService,
    private _mapService: MapService,
    private _router: Router,
    private _toastr: ToastrService
  ) { }

  ngOnInit() {
    this.dropdownSettings = {
      singleSelection: false,
      idField: 'id_nomenclature',
      textField: 'mnemonique',
      searchPlaceholderText: 'Rechercher',
      enableCheckAll: false,
      allowSearchFilter: true
    };

    this.getMetaData();
    this.createForm();

    this.$_geojsonSub = this._mapService.gettingGeojson$.subscribe((geojson: GeoJSON) => {
      this.geometry = geojson;
    })

    this.$_currentZhSub = this._dataService.currentZh.subscribe((zh: any) => {
      if (zh) {
        this._currentZh = zh;
        const selectedCritDelim = [];
        this.critDelim.forEach(critere => {
          if (this._currentZh.id_lim_list.includes(critere.id_nomenclature)) {
            selectedCritDelim.push(critere);
          }
        });
        this.form.patchValue({
          id_org: this._currentZh.id_org,
          main_name: this._currentZh.main_name,
          critere_delim: selectedCritDelim,
          sdage: this._currentZh.id_sdage,
        });
      }
    })
  }

  ngAfterViewInit() {
    setTimeout(() => this.calcCardContentHeight(), 0);
    if (this._mapService.currentExtend) {
      this._mapService.map.setView(
        this._mapService.currentExtend.center,
        this._mapService.currentExtend.zoom
      )
    }
    this._mapService.removeLayerFeatureGroups(
      [this._mapService.fileLayerFeatureGroup]
    )
  }

  calcCardContentHeight() {
    let wH = window.innerHeight;
    let tbH = document.getElementById("app-toolbar")
      ? document.getElementById("app-toolbar").offsetHeight
      : 0;
    let height = wH - (tbH + 80);
    this.cardContentHeight = height >= 350 ? height : 350;
    // resize map after resize container
    if (this._mapService.map) {
      setTimeout(() => {
        this._mapService.map.invalidateSize();
      }, 10);
    }
  }

  @HostListener("window:resize", ["$event"])
  onResize(event) {
    this.calcCardContentHeight();
  }

  createForm(): void {
    this.form = this.fb.group({
      id_org: [null, Validators.required],
      main_name: [null, Validators.required],
      critere_delim: [null, Validators.required],
      sdage: ["", Validators.required],
    });
  }

  onFormSubmit(formValues: any) {
    this.submitted = true;
    let formToPost = {
      id_org: formValues.id_org,
      main_name: formValues.main_name,
      critere_delim: [],
      sdage: formValues.sdage,
      geom: null
    };
    if (this.geometry) {
      formToPost.geom = this.geometry;
      if (this.form.valid) {
        formValues.critere_delim.forEach(critere => {
          formToPost.critere_delim.push(critere.id_nomenclature)
        });
        this.posted = true;
        if (this._currentZh) {
          formToPost['id_zh'] = Number(this._currentZh.id_zh);
        }
        this._dataService.postDataForm(formToPost, 0).subscribe(
          (data) => {
            this.form.reset();
            this.posted = false;
            this._dataService.getZhById(data.id_zh).subscribe(
              (zh: any) => {
                this._dataService.setCurrentZh(zh);
              }
            );
            this.nextTab.emit(1);
            this.activeTabs.emit(true);
          },
          (error) => {
            this.posted = false;
            this._toastr.error(error.error, '', { positionClass: 'toast-top-right' });
          }
        )
      };
    }
    else {
      this._toastr.error('Veuillez tracer ou importer une zone humide sur la carte', '', { positionClass: 'toast-top-right' });
    };

  }

  onCancel() {
    this.form.reset();
    this._router.navigate(["zones_humides"]);
  }

  getMetaData() {
    this.idOrg = this.formMetaData['BIB_ORGANISMES'];
    this.critDelim = this.formMetaData['CRIT_DELIM'];
    this.sdage = this.formMetaData['SDAGE'];
  }

  ngOnDestroy() {
    this.$_geojsonSub.unsubscribe();
    this.$_currentZhSub.unsubscribe();
  }

}
