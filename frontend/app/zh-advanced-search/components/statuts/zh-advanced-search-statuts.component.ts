import { Component, OnInit, Input } from '@angular/core';
import { FormGroup } from '@angular/forms';

@Component({
  selector: 'zh-advanced-search-statuts',
  templateUrl: './zh-advanced-search-statuts.component.html',
  styleUrls: ['./zh-advanced-search-statuts.component.scss'],
})
export class ZhAdvancedSearchStatutsComponent implements OnInit {
  @Input() statuts: any;
  @Input() plans: [];
  @Input() strategies: [];
  @Input() form: FormGroup;

  constructor() {}
  ngOnInit() {}
}
