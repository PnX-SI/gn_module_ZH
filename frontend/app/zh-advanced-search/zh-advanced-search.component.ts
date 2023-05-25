import { Component, OnInit, Input } from '@angular/core';
import { FormGroup } from '@angular/forms';

@Component({
  selector: 'zh-advanced-search',
  templateUrl: './zh-advanced-search.component.html',
  styleUrls: ['./zh-advanced-search.component.scss'],
})
export class ZhAdvancedSearchComponent implements OnInit {
  @Input() data: any;
  @Input() form: FormGroup;

  constructor() {}

  ngOnInit() {}
}
