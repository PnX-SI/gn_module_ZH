import { Component, EventEmitter, Input, OnInit, Output } from "@angular/core";
import { FormGroup, FormBuilder, Validators } from "@angular/forms";
import { ToastrService } from 'ngx-toastr';
import { ZhDataService } from "../../../services/zh-data.service";

@Component({
  selector: "zh-form-tab2",
  templateUrl: "./zh-form-tab2.component.html",
  styleUrls: ["./zh-form-tab2.component.scss"]
})
export class ZhFormTab2Component implements OnInit {

  @Input() id_zh: number;
  @Output() nextTab = new EventEmitter<number>();
  public formTab2: FormGroup;
  public critDelim: any;
  public SelectedCritDelim: any[] = [];
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
    this.createForm();
    this.getMetaDataForm(2);
    this.getZhById(this.id_zh)

  }

  createForm(): void {
    this.formTab2 = this.fb.group({
      critere_delim: [null, Validators.required],
      id_zh: [{ value: this.id_zh, disabled: true }, Validators.required],
      remark_lim: null,
      critere_delim_fs: null,
      remark_lim_fs: null,
    });
  }

  getMetaDataForm(idForm: number) {
    this._dataService.getMetaDataForm(idForm).subscribe(
      (metaData: any) => {
        this.critDelim = metaData.CRIT_DELIM;
        this.critDelimFct = metaData.CRIT_DEF_ESP_FCT;
      }
    )
  }

  getZhById(id_zh: number) {
    this._dataService.getZhById(id_zh).subscribe(
      (zh: any) => {
        this.currentZh = zh;
        this.critDelim.forEach(critere => {
          if (this.currentZh.id_lim_list.includes(critere.id_nomenclature)) {
            this.SelectedCritDelim.push(critere);
          }
        });
        this.formTab2.patchValue({
          critere_delim: this.SelectedCritDelim
        });
      }
    )
  }

  onFormSubmit(formValues: any) {
    this.submitted = true;
    let formToPost = {
      critere_delim: [],
      id_zh: Number(this.id_zh),
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
        (data) => {
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

}
