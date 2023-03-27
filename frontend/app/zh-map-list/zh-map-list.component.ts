import { Component, HostListener, OnInit, OnDestroy, AfterViewInit } from "@angular/core";

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
import { ErrorTranslatorService } from "../services/error-translator.service";
import "leaflet.vectorgrid";
import { PbfService } from "../services/pbf.service";
import { SearchFormService } from "../services/zh-search.service";
import { filter } from "rxjs/operators";

const DEFAULT_ORDER: string = "desc";
const DEFAULT_ORDER_BY: string = "update_date";

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
  public sorts: any = [];
  public metaData: any = [];
  private order: string = DEFAULT_ORDER;
  private orderby: string = DEFAULT_ORDER_BY;

  constructor(
    public mapListService: MapListService,
    private _mapService: MapService,
    private _pbfService: PbfService,
    private _zhService: ZhDataService,
    public ngbModal: NgbModal,
    public globalSub: GlobalSubService,
    private _commonService: CommonService,
    private _toastr: ToastrService,
    private _error: ErrorTranslatorService,
    public _searchService: SearchFormService
  ) {}

  ngOnInit() {
    this._searchService.initForm();
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
      .pipe(filter((mod) => mod))
      // filter undefined or null
      .subscribe((mod: any) => {
        this.userCruved = mod.cruved;
      });

    // parameters for maplist
    // columns to be default displayed
    this.mapListService.displayColumns = this.zhConfig.default_maplist_columns;
    // columns available for display
    this.mapListService.availableColumns = this.zhConfig.available_maplist_column;

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
      // Filter without data = get all ZH
      //this.filterZh({});
    });
  }

  ngAfterViewInit() {
    setTimeout(() => this.calcCardContentHeight(), 500);
    if (this._mapService.currentExtend) {
      this._mapService.map.setView(
        this._mapService.currentExtend.center,
        this._mapService.currentExtend.zoom
      );
    }
    // Load all geoms
    this._pbfService
      .getPbf(this._mapService.map)
      .toPromise()
      .then((data) =>
        data
          .on(
            "click",
            function (e) {
              const properties = e.layer.properties;
              this.filterZh({ id_zh: properties.id_zh });
            }.bind(this)
          )
          .addTo(this._mapService.map)
      );
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
    this.filterZh(this._searchService.getJson(), { offset: event.offset });
  }

  onColumnSort(event) {
    this.order = event.newValue;
    this.orderby = event.column.prop;
    this.sorts = event.sorts;
    this.filterZh(this._searchService.getJson());
  }

  displayAuthorName(element) {
    return element.prenom_role == "" ? element.nom_role : element.nom_complet;
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

  displayOrganism(authors): string {
    return authors.organisme.nom_organisme;
  }

  zhCustomCallBack(feature): any {
    // set Author name
    feature["properties"]["author"] = this.displayAuthorName(feature["properties"]["authors"]);
    // set Change Author name
    feature["properties"]["update_author"] = this.displayAuthorName(
      feature["properties"]["coauthors"]
    );
    // format Date
    feature["properties"]["create_date"] = this.displayDate(feature["properties"]["create_date"]);
    feature["properties"]["update_date"] = this.displayDate(feature["properties"]["update_date"]);

    feature["properties"]["sdage"] = this.displaySdageName(feature["properties"]["id_sdage"]);

    feature["properties"]["organism"] = this.displayOrganism(feature["properties"]["authors"]);

    feature["properties"]["update_organism"] = this.displayOrganism(
      feature["properties"]["coauthors"]
    );

    return feature;
  }

  deleteOneZh(row) {
    this._zhService.deleteOneZh(row.id_zh).subscribe(
      () => {
        this.mapListService.deleteObsFront(row.id_zh);
        this._commonService.translateToaster("success", "la zh a été supprimée avec succès");
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

  openModalCol(event, modal) {
    this.ngbModal.open(modal);
  }

  isChecked(col) {
    let i = 0;
    while (
      i < this.mapListService.displayColumns.length &&
      this.mapListService.displayColumns[i].prop !== col.prop
    ) {
      i = i + 1;
    }
    return i === this.mapListService.displayColumns.length ? false : true;
  }

  toggle(col) {
    const isChecked = this.isChecked(col);
    if (isChecked) {
      this.mapListService.displayColumns = this.mapListService.displayColumns.filter((c) => {
        return c.prop !== col.prop;
      });
    } else {
      this.mapListService.displayColumns = [...this.mapListService.displayColumns, col];
    }
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

  filterZh(filtered, params = {}) {
    const ms = this.mapListService;
    ms.isLoading = true;
    this._zhService
      .search(filtered, {
        limit: this.rowPerPage,
        order: this.order,
        orderby: this.orderby,
        ...params,
      })
      .toPromise()
      .then((res: any) => {
        ms.page.totalElements = res.total;
        ms.page.itemPerPage = this.rowPerPage;
        ms.page.pageNumber = res.page;
        ms.geojsonData = res.items;
        ms.loadTableData(res.items, this.zhCustomCallBack.bind(this));
      })
      .catch((error) => {
        const frontMsg: string = this._error.getFrontError(error.error.message);
        this._toastr.error(frontMsg);
      })
      .finally(() => (ms.isLoading = false));
  }

  resetMap() {
    this.mapListService.selectedRow = [];
    const selectedLayer = this.mapListService.selectedLayer;
    if (selectedLayer !== undefined) {
      selectedLayer.setStyle(this.mapListService.originStyle);
    }
    const layers = Object.keys(this.mapListService.layerDict);
    this.mapListService.zoomOnSeveralSelectedLayers(this._mapService.getMap(), layers);
  }

  displayAllZh() {
    this._searchService.reset();
    this.order = DEFAULT_ORDER;
    this.orderby = DEFAULT_ORDER_BY;
    this.sorts = [];
    this.filterZh({});
  }

  ngOnDestroy() {
    this.moduleSub.unsubscribe();
    this.ngbModal.dismissAll();
  }
}
