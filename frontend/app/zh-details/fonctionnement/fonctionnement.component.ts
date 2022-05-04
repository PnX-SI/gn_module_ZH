import { Component, Input } from "@angular/core";
import { TableColumn } from "../../commonComponents/table/table-interface";
import { FonctionnementModel } from "../models/fonctionnement.model";
import { ZhDataService } from "../../services/zh-data.service";

@Component({
  selector: "zh-details-fonctionnement",
  templateUrl: "./fonctionnement.component.html",
  styleUrls: ["./fonctionnement.component.scss"],
})
export class FonctionnementComponent {
  @Input() data: FonctionnementModel;

  readonly flowSize: string = "15%";
  readonly permaSize: string = "15%";

  public readonly corConnectionType = {
    "Aucune connexion": "aucune_connexion.svg",
    "Entrée et sortie": "entree_sortie.svg",
    Entrée: "entree.svg",
    Sortie: "sortie.svg",
    Traversée: "traversee.svg",
    "Passe à coté": "passe_a_cote.svg",
  };
  public connectionImg: string = "";

  public entryTableCols: TableColumn[] = [
    { name: "type", label: "Entrée d'eau", size: this.flowSize },
    { name: "permanence", label: "Permanence", size: this.permaSize },
    { name: "toponymie", label: "Toponymie et compléments d'information" },
  ];

  public exitTableCols: TableColumn[] = [
    { name: "type", label: "Sortie d'eau", size: this.flowSize },
    { name: "permanence", label: "Permanence", size: this.permaSize },
    { name: "toponymie", label: "Toponymie et compléments d'information" },
  ];

  constructor(private _dataService: ZhDataService) {}

  ngOnInit() {
    if (this.data.connexion in this.corConnectionType) {
      const connectionType = this.corConnectionType[this.data.connexion];
      this.connectionImg = this._dataService.getStatic(connectionType);
    }
  }
}
