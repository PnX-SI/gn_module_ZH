import { Component, Input } from "@angular/core";
import { StatutsModel } from "../models/status.model";

@Component({
  selector: "zh-details-statuts",
  templateUrl: "./statuts.component.html",
  styleUrls: ["./statuts.component.scss"],
})
export class StatutsComponent {
  @Input() data: StatutsModel;

  readonly urbanColSize: string = "15%";

  public regimeTableCol = [
    { name: "status", label: "Statut" },
    { name: "remarques", label: "Remarques" },
  ];

  public zonageTableCol = [
    { name: "commune", label: "Commune", size: this.urbanColSize },
    {
      name: "type_doc",
      label: "Type de document communal",
      size: this.urbanColSize,
    },
    {
      name: "type_classement",
      label: "Type de classement",
      size: this.urbanColSize,
    },
    { name: "remarque", label: "Remarques" },
  ];

  public instrumentsTableCol = [
    { name: "instrument", label: "Instruments contractuels et financiers" },
    { name: "date", label: "Date de mise en oeuvre" },
  ];

  public plansTableCol = [
    { name: "plan", label: "Nature du plan" },
    { name: "date", label: "Date de réalisation" },
    { name: "duree", label: "Durée (années)" },
  ];
}
