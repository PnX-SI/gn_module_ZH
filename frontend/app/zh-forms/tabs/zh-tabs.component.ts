import { Component, HostListener, OnInit } from "@angular/core";
import { ActivatedRoute } from '@angular/router';
import { ZhDataService } from "../../services/zh-data.service";

@Component({
  selector: "zh-tabs",
  templateUrl: "./zh-tabs.component.html",
  styleUrls: ["./zh-tabs.component.scss"]
})
export class ZhTabsComponent implements OnInit {

  public cardContentHeight: number;
  public id_zh: number;
  public disabledTabs = true;
  public selectedIndex = 0;
  public formMetaData: any;

  constructor(
    private _route: ActivatedRoute,
    private _dataService: ZhDataService,
  ) { }

  ngOnInit() {
    this.id_zh = this._route.snapshot.params['id'];
    this.getMetaDataForms();
    if (this.id_zh) {
      this.getZhById(this.id_zh);
    }
  }

  ngAfterViewInit() {
    setTimeout(() => this.calcCardContentHeight(), 0);
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

  getMetaDataForms() {
    this._dataService.getMetaDataForms().subscribe(
      (metaData: any) => {
        this.formMetaData = metaData
      }
    )
  }

  getZhById(id_zh: number) {
    this._dataService.getZhById(id_zh).subscribe(
      (zh: any) => {
        this._dataService.setCurrentZh(zh);
        this.disabledTabs = false;
        console.log(zh);
      }
    )
  }

  ngOnDestroy() {
    this._dataService.setCurrentZh(null);
  }

}
