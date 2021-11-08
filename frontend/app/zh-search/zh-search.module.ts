import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { Routes, RouterModule } from "@angular/router";
import { AngularMultiSelectModule } from "angular2-multiselect-dropdown";
import { GN2CommonModule } from "@geonature_common/GN2Common.module";
import { ZhSearchSDAGEComponent } from "./zh-search-items/zh-search-sdage/zh-search-sdage.component";
import { ZhSearchComponent } from "./zh-search.component";
import { ZhDetailsModule } from "../zh-details/zh-details.module";
import { TableComponent } from "../commonComponents/table/table.component";
import { LabelComponent } from "../commonComponents/label/label.component";
import { ZhSearchCodeComponent } from "./zh-search-items/zh-search-code/zh-search-code.component";
import { ZhSearchEnsembleComponent } from "./zh-search-items/zh-search-ensemble/zh-search-ensemble.component";
import { ZhSearchAreaComponent } from "./zh-search-items/zh-search-superficie/zh-search-area.component";
import { ZhSearchDependantComponent } from "./zh-search-items/components/zh-search-dependant/zh-search-dependant.component";
import { ZhSearchInputComponent } from "./zh-search-items/components/zh-search-input/zh-search-input.component";
import { ZhAdvancedSearchModule } from "../zh-advanced-search/zh-avanced-search.module";

const routes: Routes = [{ path: "/search", component: ZhSearchComponent }];

@NgModule({
  declarations: [
    ZhSearchSDAGEComponent,
    ZhSearchComponent,
    ZhSearchCodeComponent,
    ZhSearchEnsembleComponent,
    ZhSearchAreaComponent,
    ZhSearchDependantComponent,
    ZhSearchInputComponent,
  ],
  entryComponents: [],
  imports: [
    GN2CommonModule,
    CommonModule,
    RouterModule.forChild(routes),
    ZhDetailsModule,
    AngularMultiSelectModule,
    ZhAdvancedSearchModule,
  ],
  exports: [
    TableComponent,
    LabelComponent,
    ZhSearchComponent,
    AngularMultiSelectModule,
  ],
})
export class ZhSearchModule {}
