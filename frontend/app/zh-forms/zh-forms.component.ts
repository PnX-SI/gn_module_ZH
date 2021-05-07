import { Component, HostListener, OnInit } from "@angular/core";
import { MapService } from "@geonature_common/map/map.service";

@Component({
  selector: "zh-forms",
  templateUrl: "./zh-forms.component.html",
  styleUrls: ["./zh-forms.component.scss"]
})
export class ZhFormsComponent implements OnInit {

  public cardContentHeight: number;
  public geom: any;

  constructor(
    private _mapService: MapService,

  ) { }

  ngOnInit() {
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

  getGeoInfo(geom) {
    this.geom = geom;
    console.log(this.geom);
  }


}
