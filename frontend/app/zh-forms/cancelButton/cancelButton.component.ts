import { Component, Input } from "@angular/core";
import { NgbModal } from "@ng-bootstrap/ng-bootstrap";
import { Router } from "@angular/router";

@Component({
  selector: "zh-cancelButton",
  templateUrl: "./cancelButton.component.html",
  styleUrls: ["./cancelButton.component.scss"],
})
export class CancelButtonComponent {
  @Input() zhId: number;
  constructor(public ngbModal: NgbModal, private router: Router) {}

  onCancel(modal: any) {
    if (!this.zhId) {
      this.router.navigate(["/zones_humides"]);
    } else {
      this.ngbModal.open(modal, {
        centered: true,
        windowClass: "bib-modal",
      });
    }
  }
}
