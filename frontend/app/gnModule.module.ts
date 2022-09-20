import { NgModule } from "@angular/core";
import { NgbModule } from "@ng-bootstrap/ng-bootstrap";
import { CommonModule } from "@angular/common";
import { Routes, RouterModule } from "@angular/router";
import { GN2CommonModule } from "@geonature_common/GN2Common.module";
import { MapListService } from "@geonature_common/map-list/map-list.service";
import { ZhDetailsModule } from "./zh-details/zh-details.module";
import { NgMultiSelectDropDownModule } from "ng-multiselect-dropdown";
//Components
import { ZhMapListComponent } from "./zh-map-list/zh-map-list.component";
import { ZhFormMapComponent } from "./zh-forms/map/map.component";
import { ZhFormTab0Component } from "./zh-forms/tabs/tab0/zh-form-tab0.component";
import { ZhFormTab1Component } from "./zh-forms/tabs/tab1/zh-form-tab1.component";
import { ZhFormTab2Component } from "./zh-forms/tabs/tab2/zh-form-tab2.component";
import { ZhFormTab3Component } from "./zh-forms/tabs/tab3/zh-form-tab3.component";
import { ZhFormTab4Component } from "./zh-forms/tabs/tab4/zh-form-tab4.component";
import { ZhFormTab5Component } from "./zh-forms/tabs/tab5/zh-form-tab5.component";
import { ZhFormTab6Component } from "./zh-forms/tabs/tab6/zh-form-tab6.component";
import { ZhFormTab7Component } from "./zh-forms/tabs/tab7/zh-form-tab7.component";
import { ZhFormTab9Component } from "./zh-forms/tabs/tab9/zh-form-tab9.component";

// Service
import { ZhDataService } from "./services/zh-data.service";
import { ZhTabsComponent } from "./zh-forms/tabs/zh-tabs.component";
import { DatepickerI18n } from "./services/datepicker-i18n.service";
import { CancelButtonComponent } from "./zh-forms/cancelButton/cancelButton.component";
import { ZhFormTab8Component } from "./zh-forms/tabs/tab8/zh-form-tab8.component";
import { ErrorTranslatorService } from "./services/error-translator.service";
import { ZhSearchModule } from "./zh-search/zh-search.module";
import { SearchFormService } from "./services/zh-search.service";

// my module routing
const routes: Routes = [
  { path: "", component: ZhMapListComponent },
  { path: "forms", component: ZhTabsComponent },
  { path: "forms/:id", component: ZhTabsComponent },
];

@NgModule({
  declarations: [
    ZhMapListComponent,
    ZhTabsComponent,
    ZhFormMapComponent,
    ZhFormTab0Component,
    ZhFormTab1Component,
    ZhFormTab2Component,
    ZhFormTab3Component,
    ZhFormTab4Component,
    ZhFormTab5Component,
    ZhFormTab6Component,
    ZhFormTab7Component,
    ZhFormTab8Component,
    ZhFormTab9Component,
    CancelButtonComponent,
  ],
  imports: [
    CommonModule,
    GN2CommonModule,
    RouterModule.forChild(routes),
    NgbModule.forRoot(),
    NgMultiSelectDropDownModule.forRoot(),
    NgbModule,
    ZhDetailsModule,
    ZhSearchModule,
  ],
  providers: [
    ZhDataService,
    MapListService,
    DatepickerI18n,
    ErrorTranslatorService,
    SearchFormService,
  ],
  bootstrap: [ZhMapListComponent],
})
export class GeonatureModule {}
