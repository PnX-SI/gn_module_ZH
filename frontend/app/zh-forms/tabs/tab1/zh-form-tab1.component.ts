import { Component, Input, OnInit } from "@angular/core";
import { FormGroup, FormBuilder, Validators } from "@angular/forms";
import { Router } from "@angular/router";
import { ToastrService } from 'ngx-toastr';
import { ZhDataService } from "../../../services/zh-data.service";
import { AppConfig } from "@geonature_config/app.config";

@Component({
  selector: "zh-form-tab1",
  templateUrl: "./zh-form-tab1.component.html",
  styleUrls: ["./zh-form-tab1.component.scss"]
})
export class ZhFormTab1Component implements OnInit {

  @Input() id_zh: number;
  public generalInfoForm: FormGroup;
  public siteSpaceList: any[];
  public hasSiteSpace = false;
  public currentZh: any;
  public appConfig = AppConfig;
  public cols = ['title', 'authors', 'pub_year'];
  listBib: any[] = [];
  submitted: boolean;
  posted: boolean;
  selectedLib: any;

  constructor(
    private fb: FormBuilder,
    private _dataService: ZhDataService,
    private _toastr: ToastrService,
    private _router: Router
  ) { }

  ngOnInit() {
    this.createForm();
    this.getMetaDataForm(1);
    this.getZhById(this.id_zh);
  }



  createForm(): void {
    this.generalInfoForm = this.fb.group({
      main_name: [null, Validators.required],
      secondary_name: null,
      id_zh: [{ value: this.id_zh, disabled: true }, Validators.required],
      id_site_space: null,
      is_id_site_space: false,
      bibRef: []
    });
    this.onFormValueChanges()
  }

  onFormValueChanges(): void {
    this.generalInfoForm.get('is_id_site_space').valueChanges.subscribe(
      (val: Boolean) => {
        if (val == true) {
          this.generalInfoForm.get('id_site_space').enable();
          this.hasSiteSpace = true;
        }
        else {
          this.hasSiteSpace = false;
          this.generalInfoForm.get('id_site_space').reset();
        }
      });
  }

  getMetaDataForm(idForm: number) {
    this._dataService.getMetaDataForm(idForm).subscribe(
      (metaData: any) => {
        this.siteSpaceList = metaData.BIB_SITE_SPACE;
      }
    )
  }

  getZhById(id_zh: number) {
    this._dataService.getZhById(id_zh).subscribe(
      (zh: any) => {
        this.currentZh = zh;
        
        this.generalInfoForm.patchValue({
          main_name: this.currentZh.main_name
        });
        
      }
    )
  }

  formatter(item) {
    return item.title;
  }

  onSelectLib(bib) {
    this.selectedLib = bib.item;
  }

  onAddBib() {
    if (this.selectedLib) {
      let itemExist = this.listBib.some(item => item.id_reference == this.selectedLib.id_reference);
      if (!itemExist) {
        this.listBib.push(this.selectedLib);
        this.generalInfoForm.get('bibRef').reset();
      }
    }
  }

  onDeleteBib(id_reference: number) {
    this.listBib = this.listBib.filter(item => { return item.id_reference != id_reference });
  }

  onFormSubmit(formValues: any) {
    this.submitted = true;
    let formToPost = {
      main_name: formValues.main_name,
      secondary_name: formValues.secondary_name,
      id_zh: Number(this.id_zh),
      id_site_space: formValues.id_site_space,
      is_id_site_space: formValues.is_id_site_space,
      id_references: []
    };

    if (this.generalInfoForm.valid) {
      
      if (formValues.main_name != this.currentZh.main_name) {
        formValues.main_name = formValues.main_name;
      }
      
      //formToPost.bibRef.push(formValues.bibRef.id_reference)
      this.listBib.forEach(bib => {
        formToPost.id_references.push(bib.id_reference)
      });
      this.posted = true;
      console.log('formToPost', formToPost);
      this._dataService.postDataForm(formToPost, 1).subscribe(
        (data) => {
          //this.generalInfoForm.reset();
          this.posted = false;
          //this._router.navigate(["zones_humides/tabs", this.id_zh]);
        },
        (error) => {
          this.posted = false;
          this._toastr.error(error.error, '', { positionClass: 'toast-top-right' });
        }
      );
    }
  }

  onPrevious() {
    this.generalInfoForm.reset();
    this._router.navigate(["zones_humides/form", this.id_zh]);
  }


}
