import { Component, OnInit, Input } from "@angular/core";
import { FormGroup, FormBuilder, Validators } from "@angular/forms";

type Symbol = {
  value: string;
  text: string;
};

@Component({
  selector: "zh-search-area",
  templateUrl: "./zh-search-area.component.html",
  styleUrls: ["./zh-search-area.component.scss"],
})
export class ZhSearchAreaComponent implements OnInit {
  public areaForm: FormGroup;
  public symbols: Symbol[];

  constructor(private _fb: FormBuilder) {}

  ngOnInit() {
    this.areaForm = this._fb.group({
      ha: [
        "",
        {
          validators: [Validators.min(0)],
          updateOn: "change",
        },
      ],
    });
    this.symbols = [
      {
        value: "≥",
        text: "Supérieur à",
      },
      { value: "=", text: "Égale à" },
      {
        value: "≤",
        text: "Inférieur à",
      },
    ];
  }
}
