import { NgModule } from "@angular/core";
import { NgbModule } from "@ng-bootstrap/ng-bootstrap";
//import { BrowserModule } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import { HttpClientModule, HttpClient } from '@angular/common/http';
import { Routes, RouterModule } from "@angular/router";
import { GN2CommonModule } from "@geonature_common/GN2Common.module";

import { AppComponent } from './components/app.component';

// my module routing
const routes: Routes = [{ path: "", component: AppComponent }];

@NgModule({
  declarations: [
    AppComponent

  ],
  imports: [
    HttpClientModule,
    CommonModule,
    GN2CommonModule,
    RouterModule.forChild(routes),
    NgbModule.forRoot()
  ],
  providers: [HttpClient],
  bootstrap: [AppComponent]
})
export class GeonatureModule { }
