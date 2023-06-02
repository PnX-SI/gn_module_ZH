import { Component, OnInit, Input } from '@angular/core';
import { FormGroup } from '@angular/forms';

type Symbol = {
  value: string;
  text: string;
};

@Component({
  selector: 'zh-search-area',
  templateUrl: './zh-search-area.component.html',
  styleUrls: ['./zh-search-area.component.scss'],
})
export class ZhSearchAreaComponent implements OnInit {
  @Input() form: FormGroup;
  public symbols: Symbol[];

  constructor() {}

  ngOnInit() {
    this.symbols = [
      {
        value: '',
        text: 'Aucun filtre',
      },
      {
        value: '≥',
        text: 'Supérieur à',
      },
      { value: '=', text: 'Égale à' },
      {
        value: '≤',
        text: 'Inférieur à',
      },
    ];
  }
}
