import { Component, Input, OnInit } from '@angular/core';
import { StatutsModel } from '../models/status.model';
import { ConfigService } from '@geonature/services/config.service';
@Component({
  selector: 'zh-details-statuts',
  templateUrl: './statuts.component.html',
  styleUrls: ['./statuts.component.scss'],
})
export class StatutsComponent implements OnInit {
  @Input() data: StatutsModel;
  public table: any;

  readonly urbanColSize: string = '15%';

  public regimeTableCol = [
    { name: 'status', label: 'Statut' },
    { name: 'remarques', label: 'Remarques' },
  ];

  public zonageTableCol = [
    { name: 'commune', label: 'Commune', size: this.urbanColSize },
    {
      name: 'type_doc',
      label: 'Type de document communal',
      size: this.urbanColSize,
    },
    {
      name: 'type_classement',
      label: 'Type de classement',
      size: this.urbanColSize,
    },
    { name: 'remarque', label: 'Remarques' },
  ];

  public instrumentsTableCol = [
    { name: 'instrument', label: 'Instruments contractuels et financiers' },
    { name: 'date', label: 'Date de mise en oeuvre' },
  ];

  public plansTableCol = [
    { name: 'plan', label: 'Nature du plan de gestion' },
    { name: 'date', label: 'Date de réalisation' },
    { name: 'duree', label: 'Durée (années)' },
    { name: 'remark', label: 'Remarques' },
  ];
  constructor(public config: ConfigService) {}

  ngOnInit() {
    var groupBy = function (xs, key) {
      return xs.reduce(function (rv, x) {
        (rv[x[key]] = rv[x[key]] || []).push(x);
        return rv;
      }, {});
    };

    this.table = groupBy(this.data.autre_inventaire, 'type_code');
  }
}
