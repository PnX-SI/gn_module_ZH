import { Component, EventEmitter, Input, OnInit, Output } from "@angular/core";
import { FormGroup, FormBuilder, Validators } from "@angular/forms";
import { Subscription } from "rxjs";
import { ToastrService } from 'ngx-toastr';
import { ZhDataService } from "../../../services/zh-data.service";
import { AppConfig } from "@geonature_config/app.config";

@Component({
  selector: "zh-form-tab1",
  templateUrl: "./zh-form-tab1.component.html",
  styleUrls: ["./zh-form-tab1.component.scss"]
})
export class ZhFormTab1Component implements OnInit {

  @Input() formMetaData;
  @Output() nextTab = new EventEmitter<number>();
  public generalInfoForm: FormGroup;
  public siteSpaceList: any[];
  public hasSiteSpace = false;
  public appConfig = AppConfig;
  public cols = ['title', 'authors', 'pub_year'];
  private _currentZh: any;
  public $_currentZhSub: Subscription;
  listBib: any[] = [];
  submitted: boolean;
  posted: boolean;
  selectedLib: any;

  constructor(
    private fb: FormBuilder,
    private _dataService: ZhDataService,
    private _toastr: ToastrService,
  ) { }

  ngOnInit() {
    this.getMetaData();
    this.createForm();

    this.$_currentZhSub = this._dataService.currentZh.subscribe((zh: any) => {
      if (zh) {
        this._currentZh = zh;
        this.generalInfoForm.patchValue({
          main_name: this._currentZh.main_name,
          id_zh: this._currentZh.id_zh,
        });
      }
    })
  }


  createForm(): void {
    this.generalInfoForm = this.fb.group({
      main_name: [null, Validators.required],
      secondary_name: null,
      id_zh: [{ value: null, disabled: true }, Validators.required],
      id_site_space: null,
      is_id_site_space: false,
      bibRef: []
    });
    this.onFormValueChanges();
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

  getMetaData() {
    this.siteSpaceList = this.formMetaData.BIB_SITE_SPACE;
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
      id_zh: Number(this._currentZh.id_zh),
      id_site_space: formValues.id_site_space,
      is_id_site_space: formValues.is_id_site_space,
      id_references: []
    };

    if (this.generalInfoForm.valid) {
      if (formValues.main_name != this._currentZh.main_name) {
        formValues.main_name = formValues.main_name;
      }
      this.listBib.forEach(bib => {
        formToPost.id_references.push(bib.id_reference)
      });
      this.posted = true;
      this._dataService.postDataForm(formToPost, 1).subscribe(
        () => {
          this.generalInfoForm.reset();
          this.posted = false;
          this.nextTab.emit(2);
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
    this.nextTab.emit(0);
  }

  ngOnDestroy() {
    this.$_currentZhSub.unsubscribe();
  }

}
