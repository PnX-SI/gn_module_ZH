import { Component, EventEmitter, OnInit, Input, Output } from "@angular/core";
import { Subscription } from "rxjs";

import { ZhDataService } from "../../../services/zh-data.service";
import { HierarchyService } from "../../../services/hierarchy.service";
import { TabsService } from "../../../services/tabs.service";

@Component({
  selector: "zh-form-tab9",
  templateUrl: "./zh-form-tab9.component.html",
  styleUrls: ["./zh-form-tab9.component.scss"],
})
export class ZhFormTab9Component implements OnInit {
  private $_currentZhSub: Subscription;
  public $_fromChangeSub: Subscription;
  public currentZh: any;

  constructor(
    private _dataService: ZhDataService,
    private _tabService: TabsService,
    public hierarchy: HierarchyService
  ) {}

  ngOnInit() {
    this._tabService.getTabChange().subscribe((tabPosition: number) => {
      if (this.$_fromChangeSub) this.$_fromChangeSub.unsubscribe();
      if (this.$_currentZhSub) this.$_currentZhSub.unsubscribe();
      if (tabPosition == 9) {
        this.getCurrentZh();
      }
    });
  }

  // get current zone humides
  getCurrentZh() {
    this.$_currentZhSub = this._dataService.currentZh.subscribe((zh: any) => {
      if (zh) {
        this.currentZh = zh;
        this.hierarchy.getHierarchy(zh.id);
      }
    });
  }
}
