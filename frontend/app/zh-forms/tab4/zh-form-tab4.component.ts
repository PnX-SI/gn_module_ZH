import { Component, OnInit } from "@angular/core";
import { FormGroup, FormBuilder, FormControl } from "@angular/forms";

@Component({
  selector: "zh-form-tab4",
  templateUrl: "./zh-form-tab4.component.html",
  styleUrls: ["./zh-form-tab4.component.scss"]
})
export class ZhFormTab4Component implements OnInit {

  public formTab4: FormGroup;

  constructor(
    private fb: FormBuilder
  ) { }

  ngOnInit() {
    this.createForm()

  }

  createForm(patchWithDefaultValues: boolean = false): void {
    this.formTab4 = this.fb.group({
    });
  }


}
