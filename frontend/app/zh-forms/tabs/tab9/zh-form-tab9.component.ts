import { Component, EventEmitter, OnInit, Input, Output } from "@angular/core";
import { ToastrService } from "ngx-toastr";
import { Subscription } from "rxjs";

import { ZhDataService } from "../../../services/zh-data.service";
import { TabsService } from "../../../services/tabs.service";
import { HierarchyModel } from "./zh-tab9.model";
import { ItemModel } from "./zh-tab9.model";
import { TableColumn } from "../../../commonComponents/table/table-interface";


@Component({
  selector: "zh-form-tab9",
  templateUrl: "./zh-form-tab9.component.html",
  styleUrls: ["./zh-form-tab9.component.scss"]
})
export class ZhFormTab9Component implements OnInit {
  
  private $_currentZhSub: Subscription;

  public volet1TableCols: TableColumn[] = [
    { name: "name", label: "RUBRIQUES" },
    { name: "qualification", label: "QUALIFICATIONS" },
    { name: "knowledge", label: "CONNAISSANCES" },
    { name: "note", label: "NOTE" },
    { name: "denominator", label: "DENOMINATEUR" },
  ];

  public currentZh: any;
  public hierZh: HierarchyModel;
  public items: ItemModel[];
  //public volet1_table: any = [];
  //public volet2_table: any = [];

  constructor(
    private _dataService: ZhDataService,
    private _toastr: ToastrService,
    private _tabService: TabsService
  ) {}

  ngOnInit() {
    this.getCurrentZh();
  }

  // get current zone humides
  getCurrentZh() {
    this.$_currentZhSub = this._dataService.currentZh.subscribe((zh: any) => {
      if (zh) {
        this.currentZh = zh;
        this._dataService.getHierZh(zh.id).subscribe(
          (data: HierarchyModel) => {
            console.log(data)
            this.hierZh = data;

            this.items = this.setItems()

          },
          (error) => {
            console.log(error.error)
          }
        );
      }
    });
  }

  // set list of hierarchy items
  setItems() {
    this.items = [{"name": "", "active":true, "qualification":"", "knowledge": "", "note": null, "denominator": null}]
    this.items.push({"name": this.hierZh.volet1.cat1_sdage.name.toUpperCase( ), "active":true, "qualification":"", "knowledge": "", "note": this.hierZh.volet1.cat1_sdage.note, "denominator": this.hierZh.volet1.cat1_sdage.denominator})
    this.items.push(this.hierZh.volet1.cat1_sdage.items[0]);
    this.items.push({"name": "", "active":true, "qualification":"", "knowledge": "", "note": null, "denominator": null})
    this.items.push({"name": this.hierZh.volet1.cat2_heritage.name.toUpperCase( ), "active":true, "qualification":"", "knowledge": "", "note": this.hierZh.volet1.cat2_heritage.note, "denominator": this.hierZh.volet1.cat2_heritage.denominator})
    this.items.push(this.hierZh.volet1.cat2_heritage.items[0]);
    this.items.push(this.hierZh.volet1.cat2_heritage.items[1]);
    this.items.push(this.hierZh.volet1.cat2_heritage.items[2]);
    this.items.push(this.hierZh.volet1.cat2_heritage.items[3]);
    this.items.push({"name": "", "active":true, "qualification":"", "knowledge": "", "note": null, "denominator": null})
    this.items.push({"name": this.hierZh.volet1.cat3_eco.name.toUpperCase( ), "active":true, "qualification":"", "knowledge": "", "note": this.hierZh.volet1.cat3_eco.note, "denominator": this.hierZh.volet1.cat3_eco.denominator})
    this.items.push(this.hierZh.volet1.cat3_eco.items[0]);
    this.items.push({"name": "", "active":true, "qualification":"", "knowledge": "", "note": null, "denominator": null})
    this.items.push({"name": this.hierZh.volet1.cat4_hydro.name.toUpperCase( ), "active":true, "qualification":"", "knowledge": "", "note": this.hierZh.volet1.cat4_hydro.note, "denominator": this.hierZh.volet1.cat4_hydro.denominator})
    this.items.push(this.hierZh.volet1.cat4_hydro.items[0]);
    this.items.push(this.hierZh.volet1.cat4_hydro.items[1]);
    this.items.push(this.hierZh.volet1.cat4_hydro.items[2]);
    this.items.push({"name": "", "active":true, "qualification":"", "knowledge": "", "note": null, "denominator": null})
    this.items.push({"name": this.hierZh.volet1.cat5_soc_eco.name.toUpperCase( ), "active":true, "qualification":"", "knowledge": "", "note": this.hierZh.volet1.cat5_soc_eco.note, "denominator": this.hierZh.volet1.cat5_soc_eco.denominator})
    this.items.push(this.hierZh.volet1.cat5_soc_eco.items[0]);
    this.items.push(this.hierZh.volet1.cat5_soc_eco.items[1]);
    this.items.push({"name": "", "active":true, "qualification":"", "knowledge": "", "note": null, "denominator": null})
    this.items.push({"name": "VALEUR GLOBALE", "active":true, "qualification":"", "knowledge": "", "note": this.hierZh.volet1.note, "denominator": this.hierZh.volet1.denominator})

    //console.log(this.hierZh.volet1.cat1_sdage.items)
    return this.items
  }


}
