import { Component, EventEmitter, OnInit, Input, Output } from "@angular/core";
import { Subscription } from "rxjs";

import { ZhDataService } from "../../../services/zh-data.service";
import { HierarchyService } from "../../../services/hierarchy.service"


@Component({
  selector: "zh-form-tab9",
  templateUrl: "./zh-form-tab9.component.html",
  styleUrls: ["./zh-form-tab9.component.scss"]
})
export class ZhFormTab9Component implements OnInit {
  
  private $_currentZhSub: Subscription;
  public currentZh: any;

  constructor(
    private _dataService: ZhDataService,
    public hierarchy: HierarchyService
  ) {}

  ngOnInit() {
    this.getCurrentZh();
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
