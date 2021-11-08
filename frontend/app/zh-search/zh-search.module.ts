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
import { ZhSearchDepartementComponent } from "./zh-search-items/zh-search-departement/zh-search-departement.component";
import { ZhSearchCommuneComponent } from "./zh-search-items/zh-search-commune/zh-search-commune.component";

const routes: Routes = [{ path: "/search", component: ZhSearchComponent }];

@NgModule({
  declarations: [
    ZhSearchSDAGEComponent,
    ZhSearchComponent,
    ZhSearchCodeComponent,
    ZhSearchEnsembleComponent,
    ZhSearchAreaComponent,
    ZhSearchDepartementComponent,
    ZhSearchCommuneComponent,
  ],
  entryComponents: [],
  imports: [
    GN2CommonModule,
    CommonModule,
    RouterModule.forChild(routes),
    ZhDetailsModule,
    AngularMultiSelectModule,
  ],
  exports: [
    TableComponent,
    LabelComponent,
    ZhSearchComponent,
    AngularMultiSelectModule,
  ],
})
export class ZhSearchModule {}
