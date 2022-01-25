import { Component, Input, ChangeDetectionStrategy } from "@angular/core";
import { Output, EventEmitter } from "@angular/core";
import { NgbModal } from "@ng-bootstrap/ng-bootstrap";

import { TableColumn } from "../table/table-interface";

@Component({
  selector: "zh-image-table",
  templateUrl: "./image-table.component.html",
  styleUrls: ["./image-table.component.scss"],
})
export class ImageTableComponent {
  public mainPhoto: any;

  constructor(public deleteModal: NgbModal) {}

  @Input() tableCols: TableColumn[];
  @Input() data: any;
  @Input() deletable: boolean;
  @Input() editable: boolean;
  @Input() downloadable: boolean;
  @Output() onDelete = new EventEmitter<object>();
  @Output() onEdit = new EventEmitter<object>();
  @Output() onDownload = new EventEmitter<object>();
  @Output() onRadioChanged = new EventEmitter<object>();

  onEditItem(value: object) {
    // No modal to open, just an event with the object
    // to emit
    console.log(value);
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

  onRadioChangedItem(event) {
    this.onRadioChanged.emit(event);
  }
}
