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

  public readonly imgPath = "external_assets/zones_humides";
  public readonly corConnectionType = {
    "Aucune Connexion": "aucune_connexion.svg",
    "Entrée et sortie": "entree_sortie.svg",
    Entrée: "entree.svg",
    Sortie: "sortie.svg",
    Traversée: "traversee.svg",
    "Passe à coté": "passe_a_cote.svg",
  };
  public connectionImg: string = "";

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
  ngOnInit() {
    if (this.data.connexion in this.corConnectionType) {
      const connectionType = this.corConnectionType[this.data.connexion];
      this.connectionImg = `${this.imgPath}/${connectionType}`;
    }
  }
}
