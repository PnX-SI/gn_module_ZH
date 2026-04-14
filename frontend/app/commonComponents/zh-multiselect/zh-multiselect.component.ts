import {
  Component,
  OnInit,
  Input,
  Output,
  EventEmitter,
  ElementRef,
  ViewChild,
} from '@angular/core';
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
  @Input() hightlightValue: boolean;
  @Input() groupBy: string | null;
  @Input() placeholder: string;
  @Output() onOpen = new EventEmitter<any>();
  @ViewChild('searchInput') private searchInputRef?: ElementRef<HTMLInputElement>;
  constructor() {
    super();
    this.multiple = true;
    this.hightlightValue = true;
    this.groupBy = null;
    this.placeholder = 'Sélectionner';
  }
  ngOnInit() {
    super.ngOnInit();
  }

  // Add dropdown open handler to manage the focus of the component
  public handleOpen(event: any): void {
    this.onOpen.emit(event);
    // Wait for the dropdown to render before moving the focus.
    setTimeout(() => this.searchInputRef?.nativeElement?.focus(), 0);
  }

  public selectAllFiltered(select: any) {
    for (const item of select.itemsList.filteredItems) {
      select.select(item);
    }
    // close popup
    select.close();
  }
}
