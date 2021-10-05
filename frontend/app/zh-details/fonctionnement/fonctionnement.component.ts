import { Component, Input } from "@angular/core";

@Component({
  selector: "zh-details-fonctionnement",
  templateUrl: "./fonctionnement.component.html",
  styleUrls: ["./fonctionnement.component.scss"],
})
export class FonctionnementComponent {
  @Input() data;
}
