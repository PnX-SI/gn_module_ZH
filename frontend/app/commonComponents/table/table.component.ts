import { Component, Input } from "@angular/core";
import { Output, EventEmitter } from "@angular/core";
import { NgbModal } from "@ng-bootstrap/ng-bootstrap";

import { TableColumn } from "./table-interface";

@Component({
  selector: "zh-table",
  templateUrl: "./table.component.html",
  styleUrls: ["./table.component.scss"],
})
export class TableComponent {
  constructor(public deleteModal: NgbModal) {}

  @Input() tableCols: TableColumn[];
  @Input() data: any;
  @Input() deletable: boolean;
  @Input() editable: boolean;
  @Input() downloadable: boolean;
  @Output() onDelete = new EventEmitter<object>();
  @Output() onEdit = new EventEmitter<object>();
  @Output() onDownload = new EventEmitter<object>();

  isArray(value) {
    // Since Array cannot be called in the template,
    // do it inside a method
    return Array.isArray(value);
  }

  onEditItem(value: object) {
    // No modal to open, just an event with the object
    // to emit
    this.onEdit.emit(value);
  }

  onDeleteItem(modal, value: object) {
    // Opens the modal to check if the user really wants
    // to delete the object
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

  onDownloadItem(value: object) {
    this.onDownload.emit(value);
  }
}
