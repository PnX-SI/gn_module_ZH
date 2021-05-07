import { Component, OnInit } from "@angular/core";
import { FormGroup, FormBuilder, FormControl } from "@angular/forms";
import { ZhDataService } from "../../services/zh-data.service";
import { MapService } from '@geonature_common/map/map.service';
import { ZhFormsComponent } from "../zh-forms.component";

@Component({
  selector: "zh-form-tab0",
  templateUrl: "./zh-form-tab0.component.html",
  styleUrls: ["./zh-form-tab0.component.scss"]
})
export class ZhFormTab0Component implements OnInit {

  public formTab0: FormGroup;
  public critDelim: any;
  public sdage: any;

  constructor(
    private fb: FormBuilder,
    private _ds: ZhDataService,
    private _mapService: MapService,
    private zhForms: ZhFormsComponent
  ) { }

  ngOnInit() {
    this.createForm();
    this.getForm(0);
  }

  createForm(patchWithDefaultValues: boolean = false): void {
    this.formTab0 = this.fb.group({
      name: null,
      critere_delim: null,
      sdage: null
    });
    this.onFormValueChanges();
  }

  onFormValueChanges(): void {
    this.formTab0.get('critere_delim').valueChanges.subscribe(val => {
      // todo add new val to list
      console.log(val);
    });
    this.formTab0.get('sdage').valueChanges.subscribe(val => {
      // todo add new val to list
      console.log(val);
    });
  }

  onFormTab0(formValues: any) {
    console.log(formValues);
    console.log(this.zhForms.geom);
    this._ds.postUserData(formValues,this.zhForms.geom,0).subscribe(
      data => {
        console.log(data);
      }
    );
    //console.log(this._mapService);
    //console.log(this._mapService.gettingGeojson$);
    //this._ds.postTab0(formValues, this._mapService.gettingGeojson$)
  }

  getForm(idTab) {
    this._ds.getForm(idTab).subscribe(
      data => {
        this.critDelim = data['CRIT_DELIM'];
        this.sdage = data['SDAGE'];
      }
    )
  }

}
