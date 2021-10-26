import { Component, Input, ChangeDetectionStrategy } from "@angular/core";
import { Output, EventEmitter } from "@angular/core";

import { TableColumn } from "./table-interface";

@Component({
  selector: "zh-table",
  templateUrl: "./table.component.html",
  styleUrls: ["./table.component.scss"],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class TableComponent {
  @Input() tableCols: TableColumn[];
  @Input() data: any;
  @Input() deletable: boolean;
  @Input() editable: boolean;
  @Output() onDelete = new EventEmitter<string>();
  @Output() onEdit = new EventEmitter<string>();

  isArray(value) {
    return Array.isArray(value);
  }

  editItem(value: string) {
    this.onEdit.emit(value);
  }

  deleteItem(value: string) {
    // Show a modal first
    this.onDelete.emit(value);
  }
}
