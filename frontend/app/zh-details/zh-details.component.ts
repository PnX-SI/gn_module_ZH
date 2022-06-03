import {
  Component,
  HostListener,
  OnInit,
  AfterViewInit,
  ViewChild,
} from "@angular/core";
import { MatAccordion } from "@angular/material/expansion";
import { ActivatedRoute } from "@angular/router";
import { MapService } from "@geonature_common/map/map.service";
import { ZhDataService } from "../services/zh-data.service";
import { ErrorTranslatorService } from "../services/error-translator.service";
import { Rights } from "../models/rights";
import { ToastrService } from "ngx-toastr";
import { GeoJSON } from "leaflet";
import * as L from "leaflet";

import { DetailsModel } from "./models/zh-details.model";



@Component({
  selector: "zh-details",
  templateUrl: "./zh-details.component.html",
  styleUrls: ["./zh-details.component.scss"],
})
export class ZhDetailsComponent implements OnInit, AfterViewInit {
  @ViewChild(MatAccordion) accordion: MatAccordion;
  public cardContentHeight: number;
  public id_zh: number;
  public zhDetails: DetailsModel;
  public rights: Rights;
  public expanded: boolean = false;
  public onError: boolean = false;

  constructor(
    private _mapService: MapService,
    private _zhService: ZhDataService,
    private _route: ActivatedRoute,
    private _toastr: ToastrService,
    private _error: ErrorTranslatorService
  ) {}

  ngOnInit() {
    this.id_zh = this._route.snapshot.params["id"];
    this.getRights(this.id_zh);
    this.getData();
  }

  getRights(idZh: number) {
    this._zhService
      .getRights(idZh)
      .toPromise()
      .then((rights: Rights) => (this.rights = rights));
  }

  // get zone humides details data
  getData() {
    this._zhService.getZhDetails(this.id_zh).subscribe(
      (data: DetailsModel) => {
        this.onError = false;
        this.zhDetails = data;
        let geojson: GeoJSON = {
          geometry: data.geometry,
          properties: { idZh: this.id_zh },
          type: "Feature",
        };
        setTimeout(() => {
          let layer = L.geoJSON(geojson).addTo(this._mapService.map);
          this._mapService.map.fitBounds(layer.getBounds());
        }, 0);
      },
      (error) => {
        this.onError = true;
        const frontMsg: string = this._error.getFrontError(
          error.error.message
        );
        this._toastr.error(frontMsg, "", {
          positionClass: "toast-top-right",
        });
      }
    );
  }

  ngAfterViewInit() {
    setTimeout(() => this.calcCardContentHeight(), 500);
    if (this._mapService.currentExtend) {
      this._mapService.map.setView(
        this._mapService.currentExtend.center,
        this._mapService.currentExtend.zoom
      );
    }
  }

  @HostListener("window:resize", ["$event"])
  onResize(event) {
    this.calcCardContentHeight();
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

  onWrapAll() {
    this.expanded = !this.expanded;
  }
}
