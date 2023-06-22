import { Component, Input } from '@angular/core';
import { TableColumn } from '../../commonComponents/table/table-interface';
import { DescriptionModel } from '../models/description.model';

@Component({
  selector: 'zh-details-description',
  templateUrl: './description.component.html',
  styleUrls: ['./description.component.scss'],
})
export class DescriptionComponent {
  @Input() data: DescriptionModel;

  readonly activityColSize: string = '20%';

  public corineTableCols: TableColumn[] = [
    { name: 'code', label: 'Code Corine biotopes' },
    { name: 'label', label: 'Libellé Corine biotopes' },
    { name: 'Humidité', label: 'Humidité', size: '5%' },
  ];
  activitiesTableCols: TableColumn[] = [
    {
      name: 'activite',
      label: 'Activités humaines',
      size: this.activityColSize,
    },
    { name: 'localisation', label: 'Localisation', size: this.activityColSize },
    {
      name: 'impacts',
      label: "	Impacts (facteurs influençant l'évolution de la zone)",
      size: this.activityColSize,
    },
    { name: 'remarques', label: 'Remarques' },
  ];
}
