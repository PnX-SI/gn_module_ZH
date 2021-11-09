import { Component, OnInit, Input, Output, EventEmitter } from "@angular/core";
import { FormBuilder, FormGroup } from "@angular/forms";

@Component({
  selector: "zh-advanced-search",
  templateUrl: "./zh-advanced-search.component.html",
  styleUrls: ["./zh-advanced-search.component.scss"],
})
export class ZhAdvancedSearchComponent implements OnInit {
  @Input() data: any;
  @Output() changed = new EventEmitter<FormGroup>();

  public advancedForm: FormGroup;

  constructor(private _fb: FormBuilder) {}

  ngOnInit() {
    this.advancedForm = this._fb.group({
      hydro: this._fb.group({
        functions: [""],
        qualifications: [""],
        connaissances: [""],
      }),
      bio: this._fb.group({
        functions: [""],
        qualifications: [""],
        connaissances: [""],
      }),
      socio: this._fb.group({
        functions: [""],
        qualifications: [""],
        connaissances: [""],
      }),
      interet: this._fb.group({
        functions: [""],
        qualifications: [""],
        connaissances: [""],
      }),
      statuts: this._fb.group({
        statuts: [""],
        plans: [""],
      }),
    });

    this.advancedForm.valueChanges.subscribe((res) => {
      this.changed.emit(res);
    });
  }
}
