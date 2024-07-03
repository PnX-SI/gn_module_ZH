import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { FormGroup } from '@angular/forms';

type inputDataType = {
  name: string;
  code: string;
};

@Component({
  selector: 'zh-search-dependant',
  templateUrl: './zh-search-dependant.component.html',
  styleUrls: ['./zh-search-dependant.component.scss'],
})
export class ZhSearchDependantComponent implements OnInit {
  @Input() label: string = '';
  @Input() form: FormGroup;
  @Input() set inputData(value: inputDataType[]) {
    this._inputData = value;
    this.setData(value);
  }
  @Output() onSelected = new EventEmitter<object>();
  public _inputData: inputDataType[] = null;

  constructor() {}

  ngOnInit() {
    if (!this._inputData || this._inputData.length < 1) {
      this.disable();
    }
  }

  setData(value) {
    if (this._inputData != undefined) {
      this.enable();
      this._inputData = value;
    } else {
      this.form?.reset();
      this.disable();
    }
  }
  disable() {
    this.form?.disable();
  }
  enable() {
    this.form?.enable();
  }
}
