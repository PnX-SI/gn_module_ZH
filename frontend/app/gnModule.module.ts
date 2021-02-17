import { NgModule } from "@angular/core";
import { NgbModule } from "@ng-bootstrap/ng-bootstrap";
//import { BrowserModule } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import { HttpClientModule, HttpClient } from '@angular/common/http';
import { Routes, RouterModule } from "@angular/router";
import { GN2CommonModule } from "@geonature_common/GN2Common.module";

//Components
import { ZhMapListComponent } from './zh-map-list/zh-map-list.component';

// my module routing
const routes: Routes = [{ path: "", component: ZhMapListComponent }];

@NgModule({
  declarations: [
    ZhMapListComponent

  ],
  imports: [
    HttpClientModule,
    CommonModule,
    GN2CommonModule,
    RouterModule.forChild(routes),
    NgbModule.forRoot()
  ],
  providers: [HttpClient],
  bootstrap: [ZhMapListComponent]
})
export class GeonatureModule { }
