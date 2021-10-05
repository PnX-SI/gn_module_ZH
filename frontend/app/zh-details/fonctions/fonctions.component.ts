import { Component, Input } from "@angular/core";

@Component({
  selector: "zh-details-fonctions",
  templateUrl: "./fonctions.component.html",
  styleUrls: ["./fonctions.component.scss"],
})
export class FonctionsComponent {
  @Input() data;
}
