import { Component, Input } from '@angular/core';
import { HierarchyTotalModel } from '../models/hierarchy.model';
import { HierarchyService } from '../../services/hierarchy.service';

@Component({
  selector: 'zh-details-hierarchy',
  templateUrl: './hierarchy.component.html',
  styleUrls: ['./hierarchy.component.scss'],
})
export class HierarchyComponent {
  @Input() data: HierarchyTotalModel;
  main_river_basin_name: string;

  constructor(public hierarchy: HierarchyService) {}
  ngOnInit() {
    this.main_river_basin_name = ''
    if (this.data.main_basin_name != null) {
      this.main_river_basin_name = this.data.main_basin_name;
      this.hierarchy.setItems(this.data.hierarchy);
    } else {
      this.main_river_basin_name = 'aucun'
    }
  }
}
