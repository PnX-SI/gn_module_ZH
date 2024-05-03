import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Routes, RouterModule } from '@angular/router';
import { GN2CommonModule } from '@geonature_common/GN2Common.module';
import { ZhHierarchySearchComponent } from './zh-hierarchy-search.component';
import { ZhHierarchySearchTableComponent } from './components/zh-hierarchy-search-table.component';
import { ZhDetailsModule } from '../zh-details/zh-details.module';
import { CapitalizePipe } from '../pipes/capitalize.pipe';

const routes: Routes = [{ path: 'hierarchy_search', component: ZhHierarchySearchComponent }];

@NgModule({
  declarations: [ZhHierarchySearchComponent, ZhHierarchySearchTableComponent, CapitalizePipe],
  entryComponents: [],
  imports: [GN2CommonModule, CommonModule, RouterModule.forChild(routes), ZhDetailsModule],
  exports: [ZhHierarchySearchComponent],
})
export class ZhHierarchySearchModule {}
