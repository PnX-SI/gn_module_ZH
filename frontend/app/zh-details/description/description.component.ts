import { Component, Input } from "@angular/core";

@Component({
  selector: "zh-details-description",
  templateUrl: "./description.component.html",
  styleUrls: ["./description.component.scss"],
})
export class DescriptionComponent {
  @Input() data;
}
