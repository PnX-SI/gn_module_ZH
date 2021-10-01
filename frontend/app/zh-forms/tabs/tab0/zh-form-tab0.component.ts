import {
  Component,
  EventEmitter,
  HostListener,
  Input,
  OnInit,
  Output,
} from "@angular/core";
import { FormGroup, FormBuilder, Validators } from "@angular/forms";
import { Router } from "@angular/router";
import { Subscription } from "rxjs";
import { GeoJSON } from "leaflet";
import * as L from "leaflet";
import { MapService } from "@geonature_common/map/map.service";
import { IDropdownSettings } from "ng-multiselect-dropdown";
import { ToastrService } from "ngx-toastr";
import { ZhDataService } from "../../../services/zh-data.service";
import { TabsService } from "../../../services/tabs.service";

@Component({
  selector: "zh-form-tab0",
  templateUrl: "./zh-form-tab0.component.html",
  styleUrls: ["./zh-form-tab0.component.scss"],
})
export class ZhFormTab0Component implements OnInit {
  @Input() formMetaData;
  @Output() activeTabs = new EventEmitter<boolean>();
  @Output() canChangeTab = new EventEmitter<boolean>();
  private _currentZh: any;
  public form: FormGroup;
  public cardContentHeight: number;
  public critDelim: any;
  public sdage: any;
  public idOrg: any;
  public dropdownSettings: IDropdownSettings;
  public $_geojsonSub: Subscription;
  public $_currentZhSub: Subscription;
  private geometry: GeoJSON;
  private currentLayer: any;
  public submitted = false;
  public posted = false;

  constructor(
    private fb: FormBuilder,
    private _dataService: ZhDataService,
    private _tabService: TabsService,
    private _mapService: MapService,
    private _router: Router,
    private _toastr: ToastrService
  ) {}

  ngOnInit() {
    this.dropdownSettings = {
      singleSelection: false,
      idField: "id_nomenclature",
      textField: "mnemonique",
      searchPlaceholderText: "Rechercher",
      enableCheckAll: false,
      allowSearchFilter: true,
    };

    this.getMetaData();
    this.createForm();

    this.$_geojsonSub = this._mapService.gettingGeojson$.subscribe(
      (geojson: GeoJSON) => {
        if (
          this.geometry &&
          JSON.stringify(this.geometry) != JSON.stringify(geojson)
        ) {
          this.canChangeTab.emit(false);
        }
      }
    );

    this.intiTab();
    this._tabService.getTabChange().subscribe((tabPosition: number) => {
      if (tabPosition == 0) {
        this.intiTab();
      }
    });
  }

  ngAfterViewInit() {
    setTimeout(() => this.calcCardContentHeight(), 0);
  }

  intiTab() {
    setTimeout(() => {
      this._mapService.removeAllLayers(
        this._mapService.map,
        this._mapService.leafletDrawFeatureGroup
      );
    }, 0);

    this._dataService.getAllZhGeom().subscribe((geoms: any) => {
      geoms.forEach((geom) => {
        let geojson = {
          geometry: geom,
          properties: {},
          type: "Feature",
        };
        // L.geoJSON(geojson).addTo(this._mapService.map);
      });
    });
    this.$_currentZhSub = this._dataService.currentZh.subscribe((zh: any) => {
      if (zh) {
        this._currentZh = zh;
        const selectedCritDelim = [];
        this.critDelim.forEach((critere) => {
          if (
            this._currentZh.properties.id_lims.includes(critere.id_nomenclature)
          ) {
            selectedCritDelim.push(critere);
          }
        });
        this.form.patchValue({
          id_org: this._currentZh.properties.id_org,
          main_name: this._currentZh.properties.main_name,
          critere_delim: selectedCritDelim,
          sdage: this._currentZh.properties.id_sdage,
        });
        setTimeout(() => {
          this._mapService.loadGeometryReleve(this._currentZh, false);

          this.currentLayer =
            this._mapService.leafletDrawFeatureGroup.getLayers()[0];

          const coordinates = this._currentZh.geometry.coordinates;
          const myLatLong = coordinates[0].map((point) => {
            return L.latLng(point[1], point[0]);
          });
          const layer = L.polygon(myLatLong);
          this.geometry = layer.toGeoJSON();
          if (this._mapService.map) {
            setTimeout(() => {
              this._mapService.map.fitBounds(layer.getBounds());
            }, 10);
          }
          this._mapService.map.invalidateSize();
        }, 0);
        this.canChangeTab.emit(true);
      }
    });
  }

  calcCardContentHeight() {
    let wH = window.innerHeight;
    let tbH = document.getElementById("app-toolbar")
      ? document.getElementById("app-toolbar").offsetHeight
      : 0;
    let height = wH - (tbH + 81);
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
    this.form.valueChanges.subscribe(() => {
      this.canChangeTab.emit(false);
    });
  }

  onFormSubmit(formValues: any) {
    this.submitted = true;
    let formToPost = {
      id_org: formValues.id_org,
      main_name: formValues.main_name,
      critere_delim: [],
      sdage: formValues.sdage,
      geom: null,
    };

    if (this.geometry) {
      formToPost.geom = this.geometry;
      if (this.form.valid) {
        formValues.critere_delim.forEach((critere) => {
          formToPost.critere_delim.push(critere.id_nomenclature);
        });
        this.posted = true;
        if (this._currentZh) {
          formToPost["id_zh"] = Number(this._currentZh.properties.id_zh);
        }
        this._dataService.postDataForm(formToPost, 0).subscribe(
          (data) => {
            this.posted = false;
            this._dataService.getZhById(data.id_zh).subscribe((zh: any) => {
              this._dataService.setCurrentZh(zh);
            });
            this.activeTabs.emit(true);
            this.canChangeTab.emit(true);
            this._toastr.success("Vos données sont bien enregistrées", "", {
              positionClass: "toast-top-right",
            });
          },
          (error) => {
            this.posted = false;
            this._toastr.error(error.error, "", {
              positionClass: "toast-top-right",
            });
          }
        );
      }
    } else {
      this._toastr.error(
        "Veuillez tracer ou importer une zone humide sur la carte",
        "",
        { positionClass: "toast-top-right" }
      );
    }
  }

  onNewGeom(e) {
    this._mapService.map.eachLayer((l) => {
      if (l._leaflet_id == this.currentLayer._leaflet_id) {
        this._mapService.map.removeLayer(l);
      }
    });
  }

  updateGeom(e) {
    this.geometry = e;
  }

  onCancel() {
    this.form.reset();
    this._router.navigate(["zones_humides"]);
  }

  getMetaData() {
    this.idOrg = this.formMetaData["BIB_ORGANISMES"];
    this.critDelim = this.formMetaData["CRIT_DELIM"];
    this.sdage = this.formMetaData["SDAGE"];
  }

  ngOnDestroy() {
    this.$_geojsonSub.unsubscribe();
    this.$_currentZhSub.unsubscribe();
  }
}
