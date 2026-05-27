import { Component, OnInit, Input } from '@angular/core';
import { FormGroup } from '@angular/forms';

@Component({
  selector: 'zh-search-delim',
  templateUrl: './zh-search-delim.component.html',
  styleUrls: ['./zh-search-delim.component.scss'],
})
export class ZhSearchDelimComponent implements OnInit {
  @Input() data: any;
  @Input() form: FormGroup;

  constructor() {}

  ngOnInit() {}
}
