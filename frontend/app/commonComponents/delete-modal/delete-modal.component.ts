import { Component, Input } from "@angular/core";
import { NgbActiveModal } from "@ng-bootstrap/ng-bootstrap";
@Component({
  selector: "zh-delete-modal",
  templateUrl: "./delete-modal.component.html",
  styleUrls: ["./delete-modal.component.scss"],
})
export class DeleteModalComponent {
  constructor(public activeModal: NgbActiveModal) {}

  @Input() title: string;
  @Input() message: string; // name of the thing to delete
}
