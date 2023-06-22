import { Component } from '@angular/core';
import { Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'zh-delete-modal',
  templateUrl: './delete-modal.component.html',
  styleUrls: ['./delete-modal.component.scss'],
})
export class DeleteModalComponent {
  constructor() {}

  @Output() onDelete = new EventEmitter<string>();
  @Output() onCancel = new EventEmitter<string>();

  onDeleteClicked() {
    this.onDelete.emit();
  }

  onCancelClicked() {
    this.onCancel.emit();
  }
}
