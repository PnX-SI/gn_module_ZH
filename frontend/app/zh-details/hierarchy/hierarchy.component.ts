import { Component, Input } from '@angular/core';
import { HierarchyTotalModel } from '../models/hierarchy.model';
import { HierarchyService } from '../../services/hierarchy.service';

@Component({
  selector: 'zh-details-hierarchy',
  templateUrl: './hierarchy.component.html',
  styleUrls: ['./hierarchy.component.scss'],
})
export class HierarchyComponent {
  @Input() main_rb_name: string;
  main_river_basin: string;

  constructor(public hierarchy: HierarchyService) {}
  ngOnInit() {
    this.main_river_basin = ''
    if (this.main_rb_name != null) {
      this.main_river_basin = this.main_rb_name;
    } else {
      this.main_river_basin = 'aucun'
    }
  }
}
