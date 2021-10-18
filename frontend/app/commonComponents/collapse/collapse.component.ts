import { Component, Input } from "@angular/core";

@Component({
  selector: "collapse",
  templateUrl: "./collapse.component.html",
  styleUrls: ["./collapse.component.scss"],
})
export class CollapseComponent {
  @Input() title: string;
  @Input() expanded: boolean = true;
}
