import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Routes, RouterModule } from '@angular/router';
import { GN2CommonModule } from '@geonature_common/GN2Common.module';
import { ZhAdvancedSearchComponent } from './zh-advanced-search.component';
import { ZhAdvancedSearchFonctionsComponent } from './components/fonctions/zh-advanced-search-fonctions.component';
import { ZhDetailsModule } from '../zh-details/zh-details.module';
import { ZhAdvancedSearchStatutsComponent } from './components/statuts/zh-advanced-search-statuts.component';
import { ZhAdvancedSearchEvaluationsComponent } from './components/evaluations/zh-advanced-search-evaluations.component';

const routes: Routes = [{ path: 'advanced_search', component: ZhAdvancedSearchComponent }];

@NgModule({
  declarations: [
    ZhAdvancedSearchComponent,
    ZhAdvancedSearchFonctionsComponent,
    ZhAdvancedSearchStatutsComponent,
    ZhAdvancedSearchEvaluationsComponent,
  ],
  entryComponents: [],
  imports: [GN2CommonModule, CommonModule, RouterModule.forChild(routes), ZhDetailsModule],
  exports: [ZhAdvancedSearchComponent],
})
export class ZhAdvancedSearchModule {}
