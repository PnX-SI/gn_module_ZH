import { Component, Input } from "@angular/core";

@Component({
  selector: "zh-details-evaluation",
  templateUrl: "./evaluation.component.html",
  styleUrls: ["./evaluation.component.scss"],
})
export class EvaluationComponent {
  @Input() data;
}
