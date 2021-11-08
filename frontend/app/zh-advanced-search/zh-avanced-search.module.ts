import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { Routes, RouterModule } from "@angular/router";
import { GN2CommonModule } from "@geonature_common/GN2Common.module";
import { ZhAdvancedSearchComponent } from "./zh-avanced-search.component";

const routes: Routes = [
  { path: "/advanced_search", component: ZhAdvancedSearchComponent },
];

@NgModule({
  declarations: [ZhAdvancedSearchComponent],
  entryComponents: [],
  imports: [GN2CommonModule, CommonModule, RouterModule.forChild(routes)],
  exports: [ZhAdvancedSearchComponent],
})
export class ZhAdvancedSearchModule {}
