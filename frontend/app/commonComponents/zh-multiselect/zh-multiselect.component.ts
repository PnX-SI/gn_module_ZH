import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { MultiSelectComponent } from '@geonature_common/form/multiselect/multiselect.component';

@Component({
  selector: 'zh-multiselect',
  templateUrl: './zh-multiselect.component.html',
  styleUrls: ['./zh-multiselect.component.scss'],
})
export class ZHMultiSelectComponent extends MultiSelectComponent implements OnInit {
  /** 
  */
  @Input() multiple: boolean;
  @Input() groupBy: string | null;
  @Input() placeholder: string;
  @Output() onOpen = new EventEmitter<any>();
  constructor() {
    super()
    this.multiple = true;
    this.groupBy = null;
    this.placeholder = "Sélectionner";
  }
  ngOnInit() {
    super.ngOnInit()
  }

  public selectAllFiltered(select: any) {
    for (const item of select.itemsList.filteredItems) {
      select.select(item)
    }
    // close popup
    select.close();
  }
}
