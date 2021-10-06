import { Component, EventEmitter, Input, OnInit, Output } from "@angular/core";
import { FormGroup, FormBuilder, Validators } from "@angular/forms";
import { ToastrService } from "ngx-toastr";
import { Subscription } from "rxjs";
import { TabsService } from "../../../services/tabs.service";
import { ZhDataService } from "../../../services/zh-data.service";

@Component({
  selector: "zh-form-tab2",
  templateUrl: "./zh-form-tab2.component.html",
  styleUrls: ["./zh-form-tab2.component.scss"],
})
export class ZhFormTab2Component implements OnInit {
  @Input() formMetaData;
  @Output() canChangeTab = new EventEmitter<boolean>();
  private currentZh: any;
  public $_currentZhSub: Subscription;
  public $_fromChangeSub: Subscription;
  public formTab2: FormGroup;
  public critDelim: any;
  public critDelimFct: any;
  public dropdownSettings: any;
  public submitted: boolean;
  public posted: boolean;

  constructor(
    private fb: FormBuilder,
    private _dataService: ZhDataService,
    private _toastr: ToastrService,
    private _tabService: TabsService
  ) {}

  ngOnInit() {
    this.dropdownSettings = {
      singleSelection: false,
      idField: "id_nomenclature",
      textField: "mnemonique",
      searchPlaceholderText: "Rechercher",
      enableCheckAll: false,
      allowSearchFilter: true,
    };

    this.getMetaData();
    this.createForm();
    this.initTab();

    this._tabService.getTabChange().subscribe((tabPosition: number) => {
      if (this.$_fromChangeSub) this.$_fromChangeSub.unsubscribe();
      this.$_currentZhSub.unsubscribe();
      if (tabPosition == 2) {
        this.initTab();
      }
    });
  }

  initTab() {
    this.$_currentZhSub = this._dataService.currentZh.subscribe((zh: any) => {
      if (zh) {
        this.currentZh = zh;
        const selectedCritDelim = [];
        this.critDelim.forEach((critere) => {
          if (
            this.currentZh.properties.id_lims.includes(critere.id_nomenclature)
          ) {
            selectedCritDelim.push(critere);
          }
        });
        const selectedCritDelimFs = [];
        this.critDelimFct.forEach((critere) => {
          if (
            this.currentZh.properties.id_lims_fs.includes(
              critere.id_nomenclature
            )
          ) {
            selectedCritDelimFs.push(critere);
          }
        });
        this.formTab2.patchValue({
          critere_delim: selectedCritDelim,
          id_zh: this.currentZh.properties.id_zh,
          remark_lim: this.currentZh.properties.remark_lim,
          critere_delim_fs: selectedCritDelimFs,
          remark_lim_fs: this.currentZh.properties.remark_lim_fs,
        });
        this.$_fromChangeSub = this.formTab2.valueChanges.subscribe(() => {
          this.canChangeTab.emit(false);
        });
      }
    });
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
      id_zh: Number(this.currentZh.properties.id_zh),
      remark_lim_fs: formValues.remark_lim_fs,
      remark_lim: formValues.remark_lim,
      critere_delim_fs: [],
    };

    if (this.formTab2.valid) {
      this.$_fromChangeSub.unsubscribe();
      formValues.critere_delim.forEach((critere) => {
        formToPost.critere_delim.push(critere.id_nomenclature);
      });
      formValues.critere_delim_fs.forEach((critere) => {
        formToPost.critere_delim_fs.push(critere.id_nomenclature);
      });
      this.posted = true;
      this._dataService.postDataForm(formToPost, 2).subscribe(
        () => {
          this._dataService
            .getZhById(this.currentZh.properties.id_zh)
            .subscribe((zh: any) => {
              this._dataService.setCurrentZh(zh);
              this.posted = false;
              this.canChangeTab.emit(true);
              this._toastr.success("Vos données sont bien enregistrées", "", {
                positionClass: "toast-top-right",
              });
            });
        },
        (error) => {
          this.posted = false;
          this._toastr.error(error.error, "", {
            positionClass: "toast-top-right",
          });
        }
      );
    }
  }

  ngOnDestroy() {
    this.$_currentZhSub.unsubscribe();
    if (this.$_fromChangeSub) this.$_fromChangeSub.unsubscribe();
  }
}
