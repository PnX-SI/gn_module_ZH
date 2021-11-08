import { Component, OnInit, Input } from "@angular/core";

@Component({
  selector: "zh-search-ensemble",
  templateUrl: "./zh-search-ensemble.component.html",
  styleUrls: ["./zh-search-ensemble.component.scss"],
})
export class ZhSearchEnsembleComponent implements OnInit {
  @Input() data: any;

  constructor() {}

  ngOnInit() {}
}
