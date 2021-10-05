import { Component, Input } from "@angular/core";

@Component({
  selector: "zh-details-statuts",
  templateUrl: "./statuts.component.html",
  styleUrls: ["./statuts.component.scss"],
})
export class StatutsComponent {
  @Input() data;
}
