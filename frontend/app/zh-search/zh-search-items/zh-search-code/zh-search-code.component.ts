import { Component, OnInit, Input } from "@angular/core";
import { FormGroup } from "@angular/forms";

@Component({
  selector: "zh-search-code",
  templateUrl: "./zh-search-code.component.html",
  styleUrls: ["./zh-search-code.component.scss"],
})
export class ZhSearchCodeComponent implements OnInit {
  @Input() form: FormGroup;

  constructor() {}

  ngOnInit() {}
}
