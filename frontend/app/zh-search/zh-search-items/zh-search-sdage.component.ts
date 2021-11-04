import { Component, OnInit, Input } from "@angular/core";

@Component({
  selector: "zh-search-sdage",
  templateUrl: "./zh-search-sdage.component.html",
  styleUrls: ["./zh-search-sdage.component.scss"],
})
export class ZhSearchSDAGEComponent implements OnInit {
  @Input() sdage: any;
  @Input() values: any;

  constructor() {}

  ngOnInit() {}
}
