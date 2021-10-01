import { Component, HostListener, OnInit, ViewChild } from "@angular/core";
import { ActivatedRoute } from "@angular/router";
import { ZhDataService } from "../../services/zh-data.service";
import { MatTabGroup } from "@angular/material";
import { NgbModalConfig, NgbModal } from "@ng-bootstrap/ng-bootstrap";
import { TabsService } from "../../services/tabs.service";

@Component({
  selector: "zh-tabs",
  templateUrl: "./zh-tabs.component.html",
  styleUrls: ["./zh-tabs.component.scss"],
})
export class ZhTabsComponent implements OnInit {
  public cardContentHeight: number;
  public id_zh: number;
  public disabledTabs = true;
  public selectedIndex = 0;
  public currentTab = 0;
  public clickedTabIndex = 0;
  public formMetaData: any;
  @ViewChild("tabs") tabs: MatTabGroup;
  @ViewChild("tabsChangeModal") tabsChangeModal: any;

  canChangeTab: boolean = false;
  repeatTab: boolean = false;
  nextTabPostion: number = 0;
  modalReference: any;

  constructor(
    private _route: ActivatedRoute,
    public ngbModal: NgbModal,
    private _dataService: ZhDataService,
    private _tabService: TabsService,
    private config: NgbModalConfig
  ) {
    config.backdrop = "static";
  }

  ngOnInit() {
    this.id_zh = this._route.snapshot.params["id"];
    this.getMetaDataForms();
    if (this.id_zh) {
      this.getZhById(this.id_zh);
    }
  }

  ngAfterViewInit() {
    setTimeout(() => this.calcCardContentHeight(), 0);
  }

  selectedIndexChange(nextPosition: number) {
    if (this.canChangeTab) {
      this.currentTab = nextPosition;
      this._tabService.setTabChange(nextPosition);
    } else {
      if (nextPosition != this.currentTab) this.clickedTabIndex = nextPosition;
      this.tabs.selectedIndex = this.currentTab;
      setTimeout(() => {
        this.openTabsModal(this.tabsChangeModal);
      }, 200);
    }
  }

  openTabsModal(modal) {
    this.modalReference = this.ngbModal.open(modal, {
      centered: true,
    });
  }

  onChangeTab(status: boolean) {
    if (status) {
      this.canChangeTab = true;
      this.tabs.selectedIndex = this.clickedTabIndex;
      this._tabService.setTabChange(this.clickedTabIndex);
    }
    this.ngbModal.dismissAll(status);
  }

  calcCardContentHeight() {
    let wH = window.innerHeight;
    let tbH = document.getElementById("app-toolbar")
      ? document.getElementById("app-toolbar").offsetHeight
      : 0;
    let height = wH - (tbH + 80);
    this.cardContentHeight = height >= 350 ? height : 350;
  }

  @HostListener("window:resize", ["$event"])
  onResize(event) {
    this.calcCardContentHeight();
  }

  onNext(step: number) {
    this.selectedIndex = step;
  }

  onActiveTabs(activatedTabs: boolean) {
    this.disabledTabs = !activatedTabs;
  }
  // todo check current tab event ?
  onCanChangeTab(status: boolean) {
    this.canChangeTab = status;
  }

  getMetaDataForms() {
    this._dataService.getMetaDataForms().subscribe((metaData: any) => {
      this.formMetaData = metaData;
    });
  }

  getZhById(id_zh: number) {
    this._dataService.getZhById(id_zh).subscribe((zh: any) => {
      this._dataService.setCurrentZh(zh);
      this.disabledTabs = false;
    });
  }

  ngOnDestroy() {
    this._dataService.setCurrentZh(null);
  }
}
