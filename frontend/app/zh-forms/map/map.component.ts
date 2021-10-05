import {
  Component,
  OnInit,
  AfterViewInit,
  OnDestroy,
  Output,
  EventEmitter,
} from "@angular/core";
import { Subscription } from "rxjs";
import { leafletDrawOption } from "@geonature_common/map/leaflet-draw.options";
import { ModuleConfig } from "../../module.config";
import { MapService } from "@geonature_common/map/map.service";

import * as L from "leaflet";

@Component({
  selector: "zh-form-map",
  templateUrl: "map.component.html",
})
export class ZhFormMapComponent implements OnInit, AfterViewInit, OnDestroy {
  public leafletDrawOptions: any;
  public zhConfig = ModuleConfig;
  private $_geojsonSub: Subscription;
  public geometry: any = null;
  public editedGeometry: any = null;
  @Output() draw = new EventEmitter<any>();
  @Output() edit = new EventEmitter<any>();
  @Output() endDraw = new EventEmitter<any>();

  constructor(private _mapService: MapService) {}

  ngOnInit() {
    // overight the leaflet draw object to set options
    // examples: enable circle =>  leafletDrawOption.draw.circle = true;
    leafletDrawOption.draw.marker = false;
    leafletDrawOption.draw.polyline = false;
    this.leafletDrawOptions = leafletDrawOption;
    // set the input for the marker component
    // set the coord only when load data and when its edition mode (id_releve)
    // after the marker component does it by itself whith the ouput
    // when modifie the coordinates innput, it create twice the marker

    // to get geometry from filelayer
    this.$_geojsonSub = this._mapService.gettingGeojson$.subscribe(
      (geojson) => {
        this.geometry = geojson;
      }
    );
  }

  ngAfterViewInit() {
    if (this._mapService.currentExtend) {
      this._mapService.map.setView(
        this._mapService.currentExtend.center,
        this._mapService.currentExtend.zoom
      );
    }
    this._mapService.map.off(L.Draw.Event.DRAWSTART);
    this._mapService.map.on(L.Draw.Event.CREATED, (e) => {
      this.onDrawStop(e);
    });
    this._mapService.map.off(L.Draw.Event.EDITED);
    this._mapService.map.on(L.Draw.Event.EDITSTART, (e) => {
      this.onBeginEdit(e);
    });
    this._mapService.map.on(L.Draw.Event.EDITED, (e) => {
      this.onEdit(e);
    });
    let filelayerFeatures = this._mapService.fileLayerFeatureGroup.getLayers();
    // si il y a encore des filelayer -> on désactive le marker par defaut
    if (filelayerFeatures.length > 0) {
      this._mapService.setEditingMarker(false);
      this._mapService.fileLayerEditionMode = true;
    }

    filelayerFeatures.forEach((el) => {
      if ((el as any).getLayers()[0].options.color == "red") {
        (el as any).setStyle({ color: "green", opacity: 0.2 });
      }
    });
  }

  infoMessageFileLayer(geojson) {
    this._mapService.firstLayerFromMap = false;
    this._mapService.setGeojsonCoord(geojson);
    this.onDrawn(geojson[0]);
  }

  onDrawn(e) {
    this.draw.emit(e);
  }

  onBeginEdit(e) {
    this.editedGeometry = e;
  }

  onEdit(e) {
    e.layers.eachLayer((e) => this.edit.emit(e.toGeoJSON()));
  }

  onDrawStop(e) {
    this.endDraw.emit(e);
  }

  ngOnDestroy() {
    this.$_geojsonSub.unsubscribe();
  }
}
