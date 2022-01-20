import { Component, Input, OnInit } from "@angular/core";
import { StatutsModel } from "../models/status.model";
import { ModuleConfig } from "../../module.config";

@Component({
  selector: "zh-details-statuts",
  templateUrl: "./statuts.component.html",
  styleUrls: ["./statuts.component.scss"],
})
export class StatutsComponent implements OnInit {
  @Input() data: StatutsModel;
  public config = ModuleConfig;
  public table: any;

  public regimeTableCol = [
    { name: "status", label: "Statut" },
    { name: "remarques", label: "Remarques" },
  ];

  public zonageTableCol = [
    { name: "commune", label: "Commune" },
    { name: "type_doc", label: "Type de document communal" },
    { name: "type_classement", label: "Type de classement" },
    { name: "remarque", label: "Remarques" },
  ];

  public instrumentsTableCol = [
    { name: "instrument", label: "Instruments contractuels et financiers" },
    { name: "date", label: "Date de mise en oeuvre" },
  ];

  public plansTableCol = [
    { name: "plan", label: "Nature du plan de gestion" },
    { name: "date", label: "Date de réalisation" },
    { name: "duree", label: "Durée (années)" },
  ];

  ngOnInit() {
    var groupBy = function (xs, key) {
      return xs.reduce(function (rv, x) {
        (rv[x[key]] = rv[x[key]] || []).push(x);
        return rv;
      }, {});
    };

    this.table = groupBy(this.data.autre_inventaire, "type_code");
  }
}
