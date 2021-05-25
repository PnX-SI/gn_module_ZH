import { Component, ElementRef, HostListener, OnInit } from "@angular/core";
import { MapService } from "@geonature_common/map/map.service";
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: "zh-tabs",
  templateUrl: "./zh-tabs.component.html",
  styleUrls: ["./zh-tabs.component.scss"]
})
export class ZhTabsComponent implements OnInit {

  public cardContentHeight: number;
  public geom: any;
  public id_zh: number;

  constructor(
    private _mapService: MapService,
    private _route: ActivatedRoute,
    private _elRef: ElementRef
  ) { }

  ngOnInit() {
    this.id_zh = this._route.snapshot.params['id'];
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
    let height = wH - (tbH + 20);
    this.cardContentHeight = height >= 350 ? height : 350;
    console.log(" this.cardContentHeight", this.cardContentHeight);

    // resize map after resize container
    (document.querySelector('mat-tab-group') as HTMLElement).style.height = '800px !important';
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
