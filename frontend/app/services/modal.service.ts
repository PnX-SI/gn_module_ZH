import { Injectable } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';

/*

*/

@Injectable({
  providedIn: 'root',
})
export class ModalService {
  constructor(public ngbModal: NgbModal) {}

  // Specific open for all modal that edits tables
  open(modal, presentItems, allItems, currentItem?) {
    this._disableItems(presentItems, allItems);
    if (currentItem != null) {
      this._enableOneItem(currentItem, allItems);
    }
    this.ngbModal.open(modal, {
      centered: true,
      size: 'lg',
      windowClass: 'bib-modal',
    });
  }

  _enableOneItem(currentItem, allItems) {
    allItems.forEach((item) => {
      if (currentItem.id_nomenclature == item.id_nomenclature) {
        item.disabled = false;
      }
    });
  }

  _disableItems(presentItems, allItems) {
    const ids = presentItems.map((item) => item.id_nomenclature);
    allItems.forEach((item) => {
      if (ids.includes(item.id_nomenclature)) {
        item.disabled = true;
      } else {
        item.disabled = false;
      }
    });
  }
}
