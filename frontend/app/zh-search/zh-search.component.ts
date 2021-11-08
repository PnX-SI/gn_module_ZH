import { Component, OnInit, Input } from "@angular/core";

@Component({
  selector: "zh-search",
  templateUrl: "./zh-search.component.html",
  styleUrls: ["./zh-search.component.scss"],
})
export class ZhSearchComponent implements OnInit {
  @Input() forms: any;

  public selectedDepartment: any;

  constructor() {}

  ngOnInit() {}
}
