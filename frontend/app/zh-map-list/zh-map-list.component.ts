import {
  Component,
  HostListener,
  OnInit,
  OnDestroy,
  AfterViewInit,
} from "@angular/core";
import { MapListService } from "@geonature_common/map-list/map-list.service";
import { MapService } from "@geonature_common/map/map.service";
import { ModuleConfig } from "../module.config";
import { NgbModal } from "@ng-bootstrap/ng-bootstrap";
import * as moment from "moment";
import { ZhDataService } from "../services/zh-data.service";
import { CommonService } from "@geonature_common/service/common.service";
import { Subscription } from "rxjs/Subscription";
import { GlobalSubService } from "@geonature/services/global-sub.service";
import { ToastrService } from "ngx-toastr";

@Component({
  selector: "zh-map-list",
  templateUrl: "./zh-map-list.component.html",
  styleUrls: ["./zh-map-list.component.scss"],
})
export class ZhMapListComponent implements OnInit, OnDestroy, AfterViewInit {
  public userCruved: any;
  public displayColumns: Array<any>;
  public availableColumns: Array<any>;
  public idName: string;
  public apiEndPoint: string;
  public zhConfig: any;
  public rowPerPage: number;
  public cardContentHeight: number;
  public moduleSub: Subscription;
  private metaData: any;

  constructor(
    public mapListService: MapListService,
    private _mapService: MapService,
    private _zhService: ZhDataService,
    public ngbModal: NgbModal,
    public globalSub: GlobalSubService,
    private _commonService: CommonService,
    private _toastr: ToastrService
  ) {}

  ngOnInit() {
    this.mapListService.zoomOnLayer = true;
    //config
    this.zhConfig = ModuleConfig;
    this.idName = "id_zh";
    this.apiEndPoint = this.zhConfig.MODULE_URL;
    this._zhService.checkRefGeo().subscribe(
      (status) => {
        if (!status.check_ref_geo) {
          this._toastr.error(
            "Le module est inutilisable : Votre instance GeoNature ne contient aucune référence géographique concernant les communes et/ou les départements - Veuillez remplir la table l_areas du schéma ref_geo dans la base de données",
            "",
            { timeOut: 10000, positionClass: "toast-bottom-right" }
          );
        }
      },
      (err) => {
        this._commonService.translateToaster("error", err.message);
      }
    );
    // get user cruved
    this.moduleSub = this.globalSub.currentModuleSub
      // filter undefined or null
      .filter((mod) => mod)
      .subscribe((mod) => {
        this.userCruved = mod.cruved;
      });

    // parameters for maplist
    // columns to be default displayed
    this.mapListService.displayColumns = this.zhConfig.default_maplist_columns;
    // columns available for display
    this.mapListService.availableColumns =
      this.zhConfig.available_maplist_column;

    this.mapListService.idName = this.idName;
    // FETCH THE DATA
    this.mapListService.refreshUrlQuery();
    this.calculateNbRow();
    this._zhService.getMetaDataForms().subscribe((data: any) => {
      this.metaData = data;
      this.mapListService.getData(
        this.apiEndPoint,
        [{ param: "limit", value: this.rowPerPage }],
        this.zhCustomCallBack.bind(this)
      );
    });

    // end OnInit
  }

  ngAfterViewInit() {
    setTimeout(() => this.calcCardContentHeight(), 500);
    if (this._mapService.currentExtend) {
      this._mapService.map.setView(
        this._mapService.currentExtend.center,
        this._mapService.currentExtend.zoom
      );
    }
    this._mapService.removeLayerFeatureGroups([
      this._mapService.fileLayerFeatureGroup,
    ]);
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

  onChangePage(event) {
    this.mapListService.setTablePage(event, this.apiEndPoint);
  }

  onColumnSort(event) {
    this.mapListService.setHttpParam("orderby", event.column.prop);
    this.mapListService.setHttpParam("order", event.newValue);
    this.mapListService.deleteHttpParam("offset");
    this.mapListService.refreshData(this.apiEndPoint, "set");
  }

  displayAuthorName(element) {
    return element.nom_complet;
  }

  displayDate(element): string {
    return moment(element).format("DD-MM-YYYY");
  }

  displaySdageName(sdageID) {
    const sdage = this.metaData["SDAGE"].find((item: any) => {
      return item.id_nomenclature == sdageID;
    });
    return sdage.mnemonique;
  }

  zhCustomCallBack(feature): any {
    // set Author name
    feature["properties"]["author"] = this.displayAuthorName(
      feature["properties"]["authors"]
    );
    // format Date
    feature["properties"]["create_date"] = this.displayDate(
      feature["properties"]["create_date"]
    );

    feature["properties"]["sdage"] = this.displaySdageName(
      feature["properties"]["id_sdage"]
    );
    console.log("feature", feature);

    return feature;
  }

  deleteOneZh(row) {
    this._zhService.deleteOneZh(row.id_zh).subscribe(
      () => {
        this.mapListService.deleteObsFront(row.id_zh);
        this._commonService.translateToaster(
          "success",
          "la zh a été supprimée avec succès"
        );
      },
      (error) => {
        if (error.status === 403) {
          this._commonService.translateToaster("error", "NotAllowed");
        } else {
          this._commonService.translateToaster("error", "ErrorMessage");
        }
      }
    );
  }

  openDeleteModal(event, modal, iElement, row) {
    this.mapListService.urlQuery;
    this.mapListService.selectedRow = [];
    this.mapListService.selectedRow.push(row);
    event.stopPropagation();
    // prevent erreur link to the component
    iElement &&
      iElement.parentElement &&
      iElement.parentElement.parentElement &&
      iElement.parentElement.parentElement.blur();
    this.ngbModal.open(modal, {
      centered: true,
    });
  }

  ngOnDestroy() {
    this.moduleSub.unsubscribe();
    this.ngbModal.dismissAll();
  }
}
