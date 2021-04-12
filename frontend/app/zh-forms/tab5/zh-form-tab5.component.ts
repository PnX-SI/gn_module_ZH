import { Component, OnInit } from "@angular/core";
import { FormGroup, FormBuilder, FormControl } from "@angular/forms";

@Component({
  selector: "zh-form-tab5",
  templateUrl: "./zh-form-tab5.component.html",
  styleUrls: ["./zh-form-tab5.component.scss"]
})
export class ZhFormTab5Component implements OnInit {

  public formTab5: FormGroup;

  constructor(
    private fb: FormBuilder
  ) { }

  ngOnInit() {
    this.createForm()

  }

  createForm(patchWithDefaultValues: boolean = false): void {
    this.formTab5 = this.fb.group({
    });
  }


}
