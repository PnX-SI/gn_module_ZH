import { Component, Input } from "@angular/core";
import { DelimitationModel } from "../models/delimitation.model";

@Component({
  selector: "zh-details-delimitation",
  templateUrl: "./delimitation.component.html",
  styleUrls: ["./delimitation.component.scss"],
})
export class DelimitationComponent {
  @Input() data: DelimitationModel;
}
