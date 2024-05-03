import { Component, OnInit, Input } from '@angular/core';
import { FormGroup } from '@angular/forms';

@Component({
  selector: 'zh-search-sdage',
  templateUrl: './zh-search-sdage.component.html',
  styleUrls: ['./zh-search-sdage.component.scss'],
})
export class ZhSearchSDAGEComponent implements OnInit {
  @Input() data: any;
  @Input() form: FormGroup;

  constructor() {}

  ngOnInit() {}
}
