import { Component, OnInit, Input } from "@angular/core";
import { ZhDataService } from "../services/zh-data.service";
import { ToastrService } from "ngx-toastr";
import { ErrorTranslatorService } from "../services/error-translator.service";
import { FormGroup } from "@angular/forms";

@Component({
  selector: "zh-hierarchy-search",
  templateUrl: "./zh-hierarchy-search.component.html",
  styleUrls: ["./zh-hierarchy-search.component.scss"],
})
export class ZhHierarchySearchComponent implements OnInit {
  @Input() riverBasin: FormGroup;
  @Input() zones: FormGroup;
  @Input() form: FormGroup;

  constructor(
    private _zhService: ZhDataService,
    private _toastr: ToastrService,
    private _error: ErrorTranslatorService
  ) {}

  ngOnInit() {}
}
