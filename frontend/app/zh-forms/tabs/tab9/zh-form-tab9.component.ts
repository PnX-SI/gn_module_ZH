import { Component, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';

import { ZhDataService } from '../../../services/zh-data.service';
import { HierarchyService } from '../../../services/hierarchy.service';
import { TabsService } from '../../../services/tabs.service';

@Component({
  selector: 'zh-form-tab9',
  templateUrl: './zh-form-tab9.component.html',
  styleUrls: ['./zh-form-tab9.component.scss'],
})
export class ZhFormTab9Component implements OnInit {
  private $_currentZhSub: Subscription;
  public $_fromChangeSub: Subscription;
  public $_getTabChangeSub: Subscription;
  public currentZh: any;
  public main_rb_name: string;

  constructor(
    private _dataService: ZhDataService,
    private _tabService: TabsService,
    public hierarchy: HierarchyService
  ) {}

  ngOnInit() {
    this.$_getTabChangeSub = this._tabService.getTabChange().subscribe((tabPosition: number) => {
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
        if (zh.properties.main_rb_name != null) {
          this.main_rb_name = zh.properties.main_rb_name;
          this.hierarchy.getHierarchy(zh.id);
        } else {
          this.main_rb_name = 'aucun';
        }
      }
    });
  }

  //keep this code and propagate it to other tabs
  ngOnDestroy() {
    if (this.$_getTabChangeSub) this.$_getTabChangeSub.unsubscribe();
    if (this.$_currentZhSub) this.$_currentZhSub.unsubscribe();
  }
}
