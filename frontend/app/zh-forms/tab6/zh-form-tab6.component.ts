import { Component, OnInit } from "@angular/core";
import { FormGroup, FormBuilder, FormControl } from "@angular/forms";

@Component({
  selector: "zh-form-tab6",
  templateUrl: "./zh-form-tab6.component.html",
  styleUrls: ["./zh-form-tab6.component.scss"]
})
export class ZhFormTab6Component implements OnInit {

  public formTab6: FormGroup;

  constructor(
    private fb: FormBuilder
  ) { }

  ngOnInit() {
    this.createForm()

  }

  createForm(patchWithDefaultValues: boolean = false): void {
    this.formTab6 = this.fb.group({
    });
  }


}
