import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule, HttpClient} from '@angular/common/http';

import { ToastrService, ToastrModule } from 'ngx-toastr';

import {PnxMapModule} from 'pnx-map';
import {MapService} from 'pnx-map';

import { AppComponent } from './app.component';

@NgModule({
  declarations: [
    AppComponent,
    
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    CommonModule,
    ToastrModule.forRoot(),
    PnxMapModule
  ],
  providers: [MapService, HttpClient, ToastrService],
  bootstrap: [AppComponent]
})
export class AppModule { }
