import { Component, Input } from '@angular/core';
import { HierarchyModel } from '../models/hierarchy.model';
import { HierarchyService } from '../../services/hierarchy.service';

@Component({
  selector: 'zh-details-hierarchy',
  templateUrl: './hierarchy.component.html',
  styleUrls: ['./hierarchy.component.scss'],
})
export class HierarchyComponent {
  @Input() data: HierarchyModel;

  constructor(public hierarchy: HierarchyService) {}

  ngOnInit() {
    this.hierarchy.setItems(this.data);
  }
}
