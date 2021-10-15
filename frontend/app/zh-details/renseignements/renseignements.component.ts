import { Component, Input } from "@angular/core";
import { TableColumn } from "../../commonComponents/table/table-interface";
import { RenseignementsGenerauxModel } from "../models/renseignements.model";

@Component({
  selector: "zh-details-renseignements",
  templateUrl: "./renseignements.component.html",
  styleUrls: ["./renseignements.component.scss"],
})
export class RenseignementsComponent {
  @Input() data: RenseignementsGenerauxModel;

  biblioTableCols: TableColumn[] = [
    { name: "titre", label: "Titre du document" },
    { name: "auteurs", label: "Auteurs" },
    { name: "annee", label: "Année de parution" },
  ];
}
