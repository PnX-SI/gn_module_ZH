import { Component, Input } from "@angular/core";

@Component({
  selector: "zh-details-header",
  templateUrl: "./header.component.html",
  styleUrls: ["./header.component.scss"],
})
export class HeaderComponent {
  @Input() zhId: number;
}
