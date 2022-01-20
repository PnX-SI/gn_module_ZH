import { Component, Input } from "@angular/core";
import { TableColumn } from "../../commonComponents/table/table-interface";
import { FilesService } from "../../services/files.service";

@Component({
  selector: "zh-details-ressources",
  templateUrl: "./ressources.component.html",
  styleUrls: ["./ressources.component.scss"],
})
export class RessourcesComponent {
  @Input() zhId: number;

  public fileTableCol: TableColumn[] = [
    {
      name: "title_fr",
      label: "Titre du document",
    },
    { name: "author", label: "Auteur" },
    { name: "description_fr", label: "Résumé" },
  ];

  constructor(private _filesService: FilesService) {}

  ngOnInit() {
    this._filesService
      .loadFiles(this.zhId)
      .toPromise()
      .then(() => {});
  }
}
