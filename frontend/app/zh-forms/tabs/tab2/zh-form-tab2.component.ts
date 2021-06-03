import { Component, EventEmitter, Input, OnInit, Output } from "@angular/core";
import { FormGroup, FormBuilder, Validators } from "@angular/forms";
import { ToastrService } from 'ngx-toastr';
import { Subscription } from "rxjs";
import { ZhDataService } from "../../../services/zh-data.service";

@Component({
  selector: "zh-form-tab2",
  templateUrl: "./zh-form-tab2.component.html",
  styleUrls: ["./zh-form-tab2.component.scss"]
})
export class ZhFormTab2Component implements OnInit {

  @Input() formMetaData;
  @Output() nextTab = new EventEmitter<number>();
  private _currentZh: any;
  public $_currentZhSub: Subscription;
  public formTab2: FormGroup;
  public critDelim: any;
  public critDelimFct: any;
  public dropdownSettings: any;
  public currentZh: any;
  public submitted: boolean;
  public posted: boolean;

  constructor(
    private fb: FormBuilder,
    private _dataService: ZhDataService,
    private _toastr: ToastrService,
  ) { }

  ngOnInit() {
    this.dropdownSettings = {
      singleSelection: false,
      idField: 'id_nomenclature',
      textField: 'mnemonique',
      searchPlaceholderText: 'Rechercher',
      enableCheckAll: false,
      allowSearchFilter: true
    };

    this.getMetaData();
    this.createForm();

    this.$_currentZhSub = this._dataService.currentZh.subscribe((zh: any) => {
      if (zh) {
        this._currentZh = zh;
        const selectedCritDelim = [];
        this.critDelim.forEach(critere => {
          if (this._currentZh.properties.id_lims.includes(critere.id_nomenclature)) {
            selectedCritDelim.push(critere);
          }
        });
        const selectedCritDelimFs = [];
        this.critDelimFct.forEach(critere => {
          if (this._currentZh.properties.id_lims_fs.includes(critere.id_nomenclature)) {
            selectedCritDelimFs.push(critere);
          }
        });
        this.formTab2.patchValue({
          critere_delim: selectedCritDelim,
          id_zh: this._currentZh.properties.id_zh,
          remark_lim: this._currentZh.properties.remark_lim,
          critere_delim_fs: selectedCritDelimFs,
          remark_lim_fs: this._currentZh.properties.remark_lim_fs,
        });
      }
    })
  }

  createForm(): void {
    this.formTab2 = this.fb.group({
      critere_delim: [null, Validators.required],
      id_zh: [{ value: null, disabled: true }, Validators.required],
      remark_lim: null,
      critere_delim_fs: null,
      remark_lim_fs: null,
    });
  }

  getMetaData() {
    this.critDelim = this.formMetaData.CRIT_DELIM;
    this.critDelimFct = this.formMetaData.CRIT_DEF_ESP_FCT;

  }

  onFormSubmit(formValues: any) {
    this.submitted = true;
    let formToPost = {
      critere_delim: [],
      id_zh: Number(this._currentZh.properties.id_zh),
      remark_lim_fs: formValues.remark_lim_fs,
      remark_lim: formValues.remark_lim_fs,
      critere_delim_fs: []
    };

    if (this.formTab2.valid) {
      formValues.critere_delim.forEach(critere => {
        formToPost.critere_delim.push(critere.id_nomenclature)
      });
      formValues.critere_delim_fs.forEach(critere => {
        formToPost.critere_delim_fs.push(critere.id_nomenclature)
      });
      this.posted = true;
      this._dataService.postDataForm(formToPost, 2).subscribe(
        () => {
          this.formTab2.reset();
          this.posted = false;
          this.nextTab.emit(3);
        },
        (error) => {
          this.posted = false;
          this._toastr.error(error.error, '', { positionClass: 'toast-top-right' });
        }
      );
    }
  }


  openDeleteModal(event, modal, iElement, row) {

    event.stopPropagation();

  }

  ngOnDestroy() {
    this.$_currentZhSub.unsubscribe();
  }

}
