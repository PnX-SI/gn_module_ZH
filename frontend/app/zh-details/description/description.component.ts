import { Component, Input } from "@angular/core";
import { TableColumn } from "../../commonComponents/table/table-interface";
import { DescriptionModel } from "../models/description.model";

@Component({
  selector: "zh-details-description",
  templateUrl: "./description.component.html",
  styleUrls: ["./description.component.scss"],
})
export class DescriptionComponent {
  @Input() data: DescriptionModel;
  public corineTableCols: TableColumn[] = [
    { name: "code", label: "Code corine Biotope" },
    { name: "label", label: "Libellé corine biotope" },
    { name: "Humidité", label: "Humidité" },
  ];
  activitiesTableCols: TableColumn[] = [
    { name: "activite", label: "Activités humaines" },
    { name: "localisation", label: "Localisation" },
    {
      name: "impacts",
      label: "	Impacts (facteurs influençant l'évolution de la zone)",
    },
    { name: "remarques", label: "Remarques" },
  ];
}
