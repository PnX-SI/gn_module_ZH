import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { Routes, RouterModule } from "@angular/router";
import { GN2CommonModule } from "@geonature_common/GN2Common.module";
import { ZhSearchSDAGEComponent } from "./zh-search-items/zh-search-sdage/zh-search-sdage.component";
import { ZhSearchComponent } from "./zh-search.component";
import { ZhDetailsModule } from "../zh-details/zh-details.module";
import { TableComponent } from "../commonComponents/table/table.component";
import { LabelComponent } from "../commonComponents/label/label.component";
import { ZhSearchCodeComponent } from "./zh-search-items/zh-search-code/zh-search-code.component";
import { ZhSearchEnsembleComponent } from "./zh-search-items/zh-search-ensemble/zh-search-ensemble.component";
import { ZhSearchAreaComponent } from "./zh-search-items/zh-search-superficie/zh-search-area.component";

const routes: Routes = [{ path: "/search", component: ZhSearchComponent }];

@NgModule({
  declarations: [
    ZhSearchSDAGEComponent,
    ZhSearchComponent,
    ZhSearchCodeComponent,
    ZhSearchEnsembleComponent,
    ZhSearchAreaComponent,
  ],
  entryComponents: [],
  imports: [
    GN2CommonModule,
    CommonModule,
    RouterModule.forChild(routes),
    ZhDetailsModule,
  ],
  exports: [TableComponent, LabelComponent, ZhSearchComponent],
})
export class ZhSearchModule {}
