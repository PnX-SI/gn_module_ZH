import { Component, OnInit } from "@angular/core";
import { FormGroup, FormBuilder, FormControl } from "@angular/forms";

@Component({
  selector: "zh-form-tab2",
  templateUrl: "./zh-form-tab2.component.html",
  styleUrls: ["./zh-form-tab2.component.scss"]
})
export class ZhFormTab2Component implements OnInit {

  public formTab2: FormGroup;

  constructor(
    private fb: FormBuilder
  ) { }

  ngOnInit() {
    this.createForm()

  }

  createForm(patchWithDefaultValues: boolean = false): void {
    this.formTab2 = this.fb.group({
    });
  }


}
