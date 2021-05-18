import { Component, OnInit } from "@angular/core";
import { FormGroup, FormBuilder, FormControl } from "@angular/forms";

@Component({
  selector: "zh-form-tab1",
  templateUrl: "./zh-form-tab1.component.html",
  styleUrls: ["./zh-form-tab1.component.scss"]
})
export class ZhFormTab1Component implements OnInit {

  public generalInfoForm: FormGroup;

  constructor(
    private fb: FormBuilder
  ) { }

  ngOnInit() {
    this.createForm()

  }

  createForm(patchWithDefaultValues: boolean = false): void {
    this.generalInfoForm = this.fb.group({
      name: null,
      otherName: null,
      zhCode: null,
      grandEsemble: [{ value: '', disabled: true }, { updateOn: 'blur' }],
      hasGrandEsemble: false,
    });
    this.onFormValueChanges()
  }

  onFormValueChanges(): void {
    this.generalInfoForm.get('hasGrandEsemble').valueChanges.subscribe(val => {
      if (val == true) {
        this.generalInfoForm.get('grandEsemble').enable();
      }
      else {
        this.generalInfoForm.get('grandEsemble').disable();
        this.generalInfoForm.get('grandEsemble').reset();
      }
    });
    this.generalInfoForm.get('grandEsemble').valueChanges.subscribe(val => {
      // todo add new val to list
      console.log(val);
    });

  }

}
