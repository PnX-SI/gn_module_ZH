import { Component, Input } from "@angular/core";
import { TableColumn } from "../../commonComponents/table/table-interface";

@Component({
  selector: "zh-details-renseignements",
  templateUrl: "./renseignements.component.html",
  styleUrls: ["./renseignements.component.scss"],
})
export class RenseignementsComponent {
  @Input() data;

  biblioTableCols: TableColumn[] = [
    { name: "docTitle", label: "Titre du document" },
    { name: "authors", label: "Auteurs" },
    { name: "anneeParution", label: "Année de parution" },
    { name: "bassinsVersants", label: "Bassins versants" },
    { name: "editeur", label: "Editeur" },
    { name: "lieu", label: "Lieu" },
  ];
}
