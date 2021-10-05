import { Component, Input } from "@angular/core";

@Component({
  selector: "zh-details-delimitation",
  templateUrl: "./delimitation.component.html",
  styleUrls: ["./delimitation.component.scss"],
})
export class DelimitationComponent {
  @Input() data;
}
