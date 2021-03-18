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
// Service
import { ZhDataService } from "./services/zh-data.service";
import { ZhFormMapService } from "./zh-forms/map/map.service";
import { ZhFormMapComponent } from "./zh-forms/map/map.component";

// my module routing
const routes: Routes = [
  { path: "", component: ZhMapListComponent },
  { path: "form", component: ZhFormsComponent },
];

@NgModule({
  declarations: [
    ZhMapListComponent,
    ZhFormsComponent,
    ZhFormMapComponent
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
