
import { Component, HostListener, OnInit } from "@angular/core";
import { FormGroup, FormBuilder, Validators } from "@angular/forms";
import { Router } from "@angular/router";
import { Subscription } from "rxjs";
import { GeoJSON } from "leaflet";
import { MapService } from '@geonature_common/map/map.service';
import { IDropdownSettings } from 'ng-multiselect-dropdown';
import { ToastrService } from 'ngx-toastr';
import { ZhDataService } from "../services/zh-data.service";

@Component({
  selector: "zh-forms",
  templateUrl: "./zh-forms.component.html",
  styleUrls: ["./zh-forms.component.scss"]
})
export class ZhFormsComponent implements OnInit {

  public form: FormGroup;
  public cardContentHeight: number;
  public critDelim: any;
  public sdage: any;
  public dropdownSettings: IDropdownSettings;
  private $_geojsonSub: Subscription;
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
    this.createForm();
    this.getMetaDataForm(0);

    this.$_geojsonSub = this._mapService.gettingGeojson$.subscribe((geojson: GeoJSON) => {
      this.geometry = geojson;
    })
  }

  ngAfterViewInit() {
    setTimeout(() => this.calcCardContentHeight(), 500);
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
    let height = wH - (tbH + 40);
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

  createForm(patchWithDefaultValues: boolean = false): void {
    this.form = this.fb.group({
      name: [null, Validators.required],
      critere_delim: [null, Validators.required],
      sdage: ["", Validators.required],
    });
  }


  onFormSubmit(formValues: any) {
    this.submitted = true;
    let formToPost = {
      name: formValues.name,
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
        this._dataService.postDataForm(formToPost, 0).subscribe(
          () => {
            this.form.reset();
            this.posted = false;
            this._router.navigate(["zones_humides/tabs"]);
          },
          (error) => {
            console.log('post zh err', error);
          }
        );
      }
    }
    else {
      this._toastr.error('Veuillez tracer ou importer une zone humide sur la carte', '', { positionClass: 'toast-top-right' });
    };

  }

  onCancel() {
    this.form.reset();
    this._router.navigate(["zones_humides"]);
  }

  getMetaDataForm(idForm: number) {
    this._dataService.getMetaDataForm(idForm).subscribe(
      (metaData: any) => {
        this.critDelim = metaData['CRIT_DELIM'];
        this.sdage = metaData['SDAGE'];
      }
    )
  }

  ngOnDestroy() {
    this.$_geojsonSub.unsubscribe();
  }

}
