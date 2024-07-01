import { Component, OnInit, Input } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';

@Component({
  selector: 'zh-advanced-search-evaluations',
  templateUrl: './zh-advanced-search-evaluations.component.html',
  styleUrls: ['./zh-advanced-search-evaluations.component.scss'],
})
export class ZhAdvancedSearchEvaluationsComponent implements OnInit {
  @Input() form: FormGroup;
  @Input() hydros: [];
  @Input() bios: [];
  @Input() menaces: [];

  constructor() {}

  ngOnInit() {}
}
