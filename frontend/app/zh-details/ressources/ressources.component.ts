import { Component, Input } from '@angular/core';
import { TableColumn } from '../../commonComponents/table/table-interface';
import { FilesExt } from '../../models/files';
import { FilesService } from '../../services/files.service';

@Component({
  selector: 'zh-details-ressources',
  templateUrl: './ressources.component.html',
  styleUrls: ['./ressources.component.scss'],
})
export class RessourcesComponent {
  @Input() zhId: number;

  public fileTableCol: TableColumn[] = [
    {
      name: 'title_fr',
      label: 'Titre du document',
    },
    { name: 'author', label: 'Auteur' },
    { name: 'description_fr', label: 'Résumé' },
  ];

  public corFilesExt: FilesExt[] = [];

  constructor(public _filesService: FilesService) {}

  ngOnInit() {
    this._filesService
      .loadFiles(this.zhId)
      .toPromise()
      .then(() => {
        const allExtensions = [
          ...this._filesService.EXT_PDF,
          ...this._filesService.EXT_CSV,
          ...this._filesService.EXT_IMAGES,
        ];
        this.corFilesExt = [
          {
            name: 'Fichiers PDF',
            files: this._filesService.filterByExtension(this._filesService.EXT_PDF),
          },
          {
            name: 'Fichiers CSV',
            files: this._filesService.filterByExtension(this._filesService.EXT_CSV),
          },
          {
            name: 'Autres fichiers',
            files: this._filesService.unfilterByExtension(allExtensions),
          },
        ];
      });
  }
}
