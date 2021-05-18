import { Component, OnInit } from "@angular/core";
import { FormGroup, FormBuilder, FormControl } from "@angular/forms";

@Component({
  selector: "zh-form-tab3",
  templateUrl: "./zh-form-tab3.component.html",
  styleUrls: ["./zh-form-tab3.component.scss"]
})
export class ZhFormTab3Component implements OnInit {

  public formTab3: FormGroup;

  constructor(
    private fb: FormBuilder
  ) { }

  ngOnInit() {
    this.createForm()

  }

  createForm(patchWithDefaultValues: boolean = false): void {
    this.formTab3 = this.fb.group({
    });
  }


}
