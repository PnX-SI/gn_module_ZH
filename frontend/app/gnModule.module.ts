import { NgModule } from "@angular/core";
import { NgbModule } from "@ng-bootstrap/ng-bootstrap";
//import { BrowserModule } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
//import { HttpClientModule, HttpClient } from '@angular/common/http';
import { Routes, RouterModule } from "@angular/router";
import { GN2CommonModule } from "@geonature_common/GN2Common.module";
import { MapListService } from "@geonature_common/map-list/map-list.service";

//Components
import { ZhMapListComponent } from './zh-map-list/zh-map-list.component';
import { ZhFormsComponent } from "./zh-forms/zh-forms.component";
import { ZhFormMapComponent } from "./zh-forms/map/map.component";
import { GeneralInfoComponent } from "./zh-forms/general-information/general-info.component";
import { ZhFormTab2Component } from "./zh-forms/tab2/zh-form-tab2.component";
import { ZhFormTab3Component } from "./zh-forms/tab3/zh-form-tab3.component";
import { ZhFormTab4Component } from "./zh-forms/tab4/zh-form-tab4.component";
import { ZhFormTab5Component } from "./zh-forms/tab5/zh-form-tab5.component";
import { ZhFormTab6Component } from "./zh-forms/tab6/zh-form-tab6.component";
// Service
import { ZhDataService } from "./services/zh-data.service";
import { ZhFormMapService } from "./zh-forms/map/map.service";


// my module routing
const routes: Routes = [
  { path: "", component: ZhMapListComponent },
  { path: "form", component: ZhFormsComponent },
];

@NgModule({
  declarations: [
    ZhMapListComponent,
    ZhFormsComponent,
    ZhFormMapComponent,
    GeneralInfoComponent,
    ZhFormTab2Component,
    ZhFormTab3Component,
    ZhFormTab4Component,
    ZhFormTab5Component,
    ZhFormTab6Component
  ],
  imports: [
    //HttpClientModule,
    CommonModule,
    GN2CommonModule,
    RouterModule.forChild(routes),
    NgbModule.forRoot(),
    NgbModule
  ],
  providers: [
    //HttpClient,
    ZhDataService,
    MapListService,
    ZhFormMapService
  ],
  bootstrap: [ZhMapListComponent]
})
export class GeonatureModule { }
