import { Component, Input, ChangeDetectionStrategy } from "@angular/core";
import { Output, EventEmitter } from "@angular/core";
import { NgbModal } from "@ng-bootstrap/ng-bootstrap";

import { TableColumn } from "./table-interface";

@Component({
  selector: "zh-table",
  templateUrl: "./table.component.html",
  styleUrls: ["./table.component.scss"],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class TableComponent {
  constructor(public deleteModal: NgbModal) {}

  @Input() tableCols: TableColumn[];
  @Input() data: any;
  @Input() deletable: boolean;
  @Input() editable: boolean;
  @Output() onDelete = new EventEmitter<object>();
  @Output() onEdit = new EventEmitter<object>();

  isArray(value) {
    return Array.isArray(value);
  }

  onEditItem(value: object) {
    this.onEdit.emit(value);
  }

  onDeleteItem(modal, value: object) {
    this.deleteModal
      .open(modal, {
        centered: true,
        size: "lg",
        windowClass: "bib-modal",
      })
      .result.then(
        () => {
          //When suppr is clicked
          this.onDelete.emit(value);
        },
        () => {}
      );
  }
}
