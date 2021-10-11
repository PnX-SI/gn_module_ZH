import { Component, Input } from "@angular/core";
import { TableColumn } from "../../commonComponents/table/table-interface";
import { FonctionnementModel } from "../models/fonctionnement.model";

@Component({
  selector: "zh-details-fonctionnement",
  templateUrl: "./fonctionnement.component.html",
  styleUrls: ["./fonctionnement.component.scss"],
})
export class FonctionnementComponent {
  @Input() data: FonctionnementModel;
  public entryTableCols: TableColumn[] = [
    { name: "type", label: "Entrée d'eau" },
    { name: "permanence", label: "Permanence" },
    { name: "toponymie", label: "Toponymie et compléments d'information" },
  ];
  public exitTableCols: TableColumn[] = [
    { name: "type", label: "Sortie d'eau" },
    { name: "permanence", label: "Permanence" },
    { name: "toponymie", label: "Toponymie et compléments d'information" },
  ];
}
