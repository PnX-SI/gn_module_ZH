import { Component, Input } from "@angular/core";
import { HierarchyModel } from "../models/hierarchy.model";
import { ItemModel } from "../models/hierarchy.model";
import { TableColumn } from "../../commonComponents/table/table-interface";
import { ZhFormTab9Component } from "../../zh-forms/tabs/tab9/zh-form-tab9.component"

@Component({
  selector: "zh-details-hierarchy",
  templateUrl: "./hierarchy.component.html",
  styleUrls: ["./hierarchy.component.scss"],
})
export class HierarchyComponent {

  @Input() data: HierarchyModel;
  public hierTableCols: TableColumn[] = [
    { name: "name", label: "RUBRIQUES" },
    { name: "qualification", label: "QUALIFICATIONS" },
    { name: "knowledge", label: "CONNAISSANCES" },
    { name: "note", label: "NOTE" }
  ];

  public bold_row_values: any = []
  public italic_row_values: any = ['Total rubrique']
  public currentZh: any;
  public hierZh: HierarchyModel;
  public items: ItemModel[];

  ngOnInit() {
    this.setItems();
  }


  // set list of hierarchy items
  setItems() {

    this.hierZh = this.data;

    this.items = [{"name": "", "active":true, "qualification":"", "knowledge": "", "note": ""}]

    // cat 1
    this.items.push({"name": this.hierZh.volet1.cat1_sdage.name.toUpperCase( ), "active":true, "qualification":"", "knowledge": "", "note": ""})
    this.bold_row_values.push(this.hierZh.volet1.cat1_sdage.name.toUpperCase( ))
    this.items.push(this.hierZh.volet1.cat1_sdage.items[0]);
    this.items.push({"name": "Total rubrique", "active":true, "qualification":"", "knowledge": "", "note": this.hierZh.volet1.cat1_sdage.note})

    this.items.push({"name": "", "active":true, "qualification":"", "knowledge": "", "note": ""})

    // cat 2
    this.items.push({"name": this.hierZh.volet1.cat2_heritage.name.toUpperCase( ), "active":true, "qualification":"", "knowledge": "", "note": ""})
    this.bold_row_values.push(this.hierZh.volet1.cat2_heritage.name.toUpperCase( ))
    this.items.push(this.hierZh.volet1.cat2_heritage.items[0]);
    this.items.push(this.hierZh.volet1.cat2_heritage.items[1]);
    this.items.push(this.hierZh.volet1.cat2_heritage.items[2]);
    this.items.push(this.hierZh.volet1.cat2_heritage.items[3]);
    this.items.push({"name": "Total rubrique", "active":true, "qualification":"", "knowledge": "", "note": this.hierZh.volet1.cat2_heritage.note})

    this.items.push({"name": "", "active":true, "qualification":"", "knowledge": "", "note": ""})

    // cat 3
    this.items.push({"name": this.hierZh.volet1.cat3_eco.name.toUpperCase( ), "active":true, "qualification":"", "knowledge": "", "note": ""})
    this.bold_row_values.push(this.hierZh.volet1.cat3_eco.name.toUpperCase( ))
    this.items.push(this.hierZh.volet1.cat3_eco.items[0]);
    this.items.push({"name": "Total rubrique", "active":true, "qualification":"", "knowledge": "", "note": this.hierZh.volet1.cat3_eco.note})

    this.items.push({"name": "", "active":true, "qualification":"", "knowledge": "", "note": ""})

    // cat 4
    this.items.push({"name": this.hierZh.volet1.cat4_hydro.name.toUpperCase( ), "active":true, "qualification":"", "knowledge": "", "note": ""})
    this.bold_row_values.push(this.hierZh.volet1.cat4_hydro.name.toUpperCase( ))
    this.items.push(this.hierZh.volet1.cat4_hydro.items[0]);
    this.items.push(this.hierZh.volet1.cat4_hydro.items[1]);
    this.items.push(this.hierZh.volet1.cat4_hydro.items[2]);
    this.items.push({"name": "Total rubrique", "active":true, "qualification":"", "knowledge": "", "note": this.hierZh.volet1.cat4_hydro.note})

    this.items.push({"name": "", "active":true, "qualification":"", "knowledge": "", "note": ""})

    // cat 5
    this.items.push({"name": this.hierZh.volet1.cat5_soc_eco.name.toUpperCase( ), "active":true, "qualification":"", "knowledge": "", "note": ""})
    this.bold_row_values.push(this.hierZh.volet1.cat5_soc_eco.name.toUpperCase( ))
    this.items.push(this.hierZh.volet1.cat5_soc_eco.items[0]);
    this.items.push(this.hierZh.volet1.cat5_soc_eco.items[1]);
    this.items.push({"name": "Total rubrique", "active":true, "qualification":"", "knowledge": "", "note": this.hierZh.volet1.cat5_soc_eco.note})

    this.items.push({"name": "", "active":true, "qualification":"", "knowledge": "", "note": ""})

    // note volet 1
    this.items.push({"name": "NOTE VOLET 1 - VALEUR GLOBALE", "active":true, "qualification":"", "knowledge": "", "note": this.hierZh.volet1.note})
    this.bold_row_values.push("NOTE VOLET 1 - VALEUR GLOBALE")
    this.items.push({"name": "", "active":true, "qualification":"", "knowledge": "", "note": ""})

    // cat 6
    this.items.push({"name": this.hierZh.volet2.cat6_status.name.toUpperCase( ), "active":true, "qualification":"", "knowledge": "", "note": ""})
    this.bold_row_values.push(this.hierZh.volet2.cat6_status.name.toUpperCase( ))
    this.items.push(this.hierZh.volet2.cat6_status.items[0]);
    this.items.push(this.hierZh.volet2.cat6_status.items[1]);
    this.items.push({"name": "Total rubrique", "active":true, "qualification":"", "knowledge": "", "note": this.hierZh.volet2.cat6_status.note})

    this.items.push({"name": "", "active":true, "qualification":"", "knowledge": "", "note": ""})

    // cat 7
    this.items.push({"name": this.hierZh.volet2.cat7_fct_state.name.toUpperCase( ), "active":true, "qualification":"", "knowledge": "", "note": ""})
    this.bold_row_values.push(this.hierZh.volet2.cat7_fct_state.name.toUpperCase( ))
    this.items.push(this.hierZh.volet2.cat7_fct_state.items[0]);
    this.items.push(this.hierZh.volet2.cat7_fct_state.items[1]);
    this.items.push({"name": "Total rubrique", "active":true, "qualification":"", "knowledge": "", "note": this.hierZh.volet2.cat7_fct_state.note})

    this.items.push({"name": "", "active":true, "qualification":"", "knowledge": "", "note": ""})

    // cat 8
    this.items.push({"name": this.hierZh.volet2.cat8_thread.name.toUpperCase( ), "active":true, "qualification":"", "knowledge": "", "note": ""})
    this.bold_row_values.push(this.hierZh.volet2.cat8_thread.name.toUpperCase( ))
    this.items.push(this.hierZh.volet2.cat8_thread.items[0]);
    this.items.push({"name": "Total rubrique", "active":true, "qualification":"", "knowledge": "", "note": this.hierZh.volet2.cat8_thread.note})

    this.items.push({"name": "", "active":true, "qualification":"", "knowledge": "", "note": ""})

    // note volet 2 - priorite d'intervention
    this.items.push({"name": "NOTE VOLET 2 - PRIORITE D'INTERVENTION", "active":true, "qualification":"", "knowledge": "", "note": this.hierZh.volet2.note})
    this.bold_row_values.push("NOTE VOLET 2 - PRIORITE D'INTERVENTION")

    this.items.push({"name": "", "active":true, "qualification":"", "knowledge": "", "note": ""})

    // note globale
    this.items.push({"name": "TOTAL", "active":true, "qualification":"", "knowledge": "", "note": this.hierZh.global_note})
    this.bold_row_values.push("TOTAL")

    // note globale
    this.items.push({"name": "NOTE FINALE", "active":true, "qualification":"", "knowledge": "", "note": this.hierZh.final_note})
    this.bold_row_values.push("NOTE FINALE")

    return this.items
  }

}
