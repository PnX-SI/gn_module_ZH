import { Component, OnInit, Input } from "@angular/core";
import { FormGroup, FormBuilder, Validators } from "@angular/forms";

@Component({
  selector: "zh-search-code",
  templateUrl: "./zh-search-code.component.html",
  styleUrls: ["./zh-search-code.component.scss"],
})
export class ZhSearchCodeComponent implements OnInit {
  public codeForm: FormGroup;

  constructor(private _fb: FormBuilder) {}

  ngOnInit() {
    this.codeForm = this._fb.group({
      code: [
        "",
        {
          validators: [Validators.pattern("^[0-9]{2}[A-Z]{2}[0-9]{5}")],
          updateOn: "change",
        },
      ],
    });
  }
}
