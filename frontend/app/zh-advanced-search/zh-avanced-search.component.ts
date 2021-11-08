import { Component, OnInit, Input } from "@angular/core";
import { ZhDataService } from "../services/zh-data.service";

@Component({
  selector: "zh-avanced-search",
  templateUrl: "./zh-avanced-search.component.html",
  styleUrls: ["./zh-avanced-search.component.scss"],
})
export class ZhAdvancedSearchComponent implements OnInit {
  @Input() forms: any;

  constructor(private _dataService: ZhDataService) {}

  ngOnInit() {}

  onDepartmentSelected(event) {}

  onBassinSelected(event) {}
}
