import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { Routes, RouterModule } from "@angular/router";
import { GN2CommonModule } from "@geonature_common/GN2Common.module";
import { ZhHierarchySearchComponent } from "./zh-hierarchy-search.component";
import { AngularMultiSelectModule } from "angular2-multiselect-dropdown";
import { ZhHierarchySearchTableComponent } from "./components/zh-hierarchy-search-table.component";
import { ZhDetailsModule } from "../zh-details/zh-details.module";

const routes: Routes = [{ path: "/hierarchy_search", component: ZhHierarchySearchComponent }];

@NgModule({
  declarations: [ZhHierarchySearchComponent, ZhHierarchySearchTableComponent],
  entryComponents: [],
  imports: [
    GN2CommonModule,
    CommonModule,
    RouterModule.forChild(routes),
    ZhDetailsModule,
    AngularMultiSelectModule,
  ],
  exports: [ZhHierarchySearchComponent, AngularMultiSelectModule],
})
export class ZhHierarchySearchModule {}
