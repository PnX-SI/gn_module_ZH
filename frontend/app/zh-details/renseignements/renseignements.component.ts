import { Component, Input } from "@angular/core";

@Component({
  selector: "zh-details-renseignements",
  templateUrl: "./renseignements.component.html",
  styleUrls: ["./renseignements.component.scss"],
})
export class RenseignementsComponent {
  @Input() data;
}
