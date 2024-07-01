import { Component, OnInit, Input } from '@angular/core';
import { FormGroup } from '@angular/forms';

@Component({
  selector: 'zh-advanced-search-fonctions',
  templateUrl: './zh-advanced-search-fonctions.component.html',
  styleUrls: ['./zh-advanced-search-fonctions.component.scss'],
})
export class ZhAdvancedSearchFonctionsComponent implements OnInit {
  @Input() data: any;
  @Input() qualifications: [];
  @Input() connaissances: [];
  @Input() title: string = '';
  @Input() fonctionLabel: string = 'Fonction';
  @Input() form: FormGroup;
  // public dropdownSettings: {};
  // public dropdownSettingsNoCategory: {};
  constructor() {}

  ngOnInit() {}
}
