import { 
  Component,
  OnInit,
  ViewChild,
  HostListener
} from '@angular/core';
import { MapListService } from "@geonature_common/map-list/map-list.service";
import { MapService } from "@geonature_common/map/map.service";
import { DatatableComponent } from "@swimlane/ngx-datatable/release";
import { ModuleConfig } from "../module.config";

@Component({
  selector: 'zh-map-list',
  templateUrl: './zh-map-list.component.html',
  styleUrls: ['./zh-map-list.component.scss']
})
export class ZhMapListComponent 
  implements OnInit{
  public zhConfig: any;
  public rowPerPage: number;
  public cardContentHeight: number;

  @ViewChild("table")
  table: DatatableComponent;

  constructor(
    public mapListService: MapListService,
    private _mapService: MapService
  ) { }

  ngOnInit() {
    //config
    this.zhConfig = ModuleConfig;
    // parameters for maplist
    // columns to be default displayed
    this.mapListService.displayColumns = this.zhConfig.default_maplist_columns;
    // columns available for display
    this.mapListService.availableColumns = this.zhConfig.available_maplist_column;
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


  @HostListener("window:resize", ["$event"])
  onResize(event) {
    this.calcCardContentHeight();
  }

  calculateNbRow() {
    let wH = window.innerHeight;
    let listHeight = wH - 64 - 150;
    this.rowPerPage = Math.round(listHeight / 40);
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

}
