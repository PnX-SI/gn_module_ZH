import { Component, OnInit, Input } from "@angular/core";
import { FormGroup, FormBuilder, Validators } from "@angular/forms";
import { ZhDataService } from "../../../services/zh-data.service";
import { NgbModal } from "@ng-bootstrap/ng-bootstrap";
import { Subscription, Observable } from "rxjs";
import { debounceTime, distinctUntilChanged, map } from "rxjs/operators";
import { ToastrService } from "ngx-toastr";

@Component({
  selector: "zh-form-tab3",
  templateUrl: "./zh-form-tab3.component.html",
  styleUrls: ["./zh-form-tab3.component.scss"],
})
export class ZhFormTab3Component implements OnInit {
  @Input() formMetaData;
  form: FormGroup;
  sage: any;
  allSage: any;
  $_currentZhSub: Subscription;
  private _currentZh: any;
  corinBioMetaData: any;
  corinTableCol = [
    { name: "CB_code", label: "Code corine Biotope" },
    { name: "CB_label", label: "Libellé corine biotope" },
    { name: "CB_humidity", label: "Humidité" },
  ];
  activityTableCol = [
    { name: "human_activity", label: "Activités humaines" },
    { name: "localisation", label: "Localisation" },
    {
      name: "impacts",
      label: "Impacts (facteurs influençant l'évolution de la zone)",
    },
    { name: "remark_activity", label: "Remarques" },
  ];
  listCorinBio = [];
  posted: boolean = false;
  patchActivity: boolean = false;
  dropdownSettings: any;
  activityForm: FormGroup;
  modalButtonLabel: string;
  modalTitle: string;

  selectedItems = [];
  settings = {};
  listActivity: any = [];
  activitiesInput: any = [];
  submitted: boolean;

  constructor(
    private fb: FormBuilder,
    private _dataService: ZhDataService,
    public ngbModal: NgbModal,
    private _toastr: ToastrService
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

    this.settings = {
      enableCheckAll: false,
      text: "Selectionner",
      labelKey: "mnemonique",
      primaryKey: "id_nomenclature",
      searchPlaceholderText: "Rechercher",
      enableSearchFilter: true,
      groupBy: "category",
    };

    this.getMetaData();
    this.createForm();
    this.$_currentZhSub = this._dataService.currentZh.subscribe((zh: any) => {
      if (zh) {
        this._currentZh = zh;
        this.form.patchValue({
          sdage: this._currentZh.properties.id_sdage,
        });
      }
    });
  }

  getMetaData() {
    this.allSage = [...this.formMetaData["SDAGE-SAGE"]];
    this.corinBioMetaData = [...this.formMetaData["CORINE_BIO"]];
    this.activitiesInput = [...this.formMetaData["ACTIV_HUM"]];
  }

  onFormValueChanges(): void {
    this.form.get("id_sdage").valueChanges.subscribe((val: number) => {
      this.form.get("id_sage").reset();
      this.allSage.forEach((item) => {
        if (val in item) {
          this.sage = Object.values(item)[0];
        }
      });
    });
  }

  createForm(): void {
    this.form = this.fb.group({
      id_sdage: [null, Validators.required],
      id_sage: null,
      corinBio: null,
      id_corine_landcovers: null,
      remark_pres: null,
      id_thread: null,
      global_remark_activity: null,
    });
    this.onFormValueChanges();
  }

  search = (text$: Observable<string>) =>
    text$.pipe(
      debounceTime(200),
      distinctUntilChanged(),
      map((term) =>
        term.length < 1
          ? []
          : this.corinBioMetaData
              .filter(
                (v) =>
                  v.CB_label.toLowerCase().indexOf(term.toLowerCase()) > -1 ||
                  v.CB_code.toLowerCase().indexOf(term.toLowerCase()) > -1
              )
              .slice(0, 10)
      )
    );

  formatter = (result: any) => `${result.CB_code} ${result.CB_label}`;

  onAddCorinBio() {
    //corine_biotopes
    if (this.form.value.corinBio) {
      let itemExist = this.listCorinBio.some(
        (item) => item.CB_code == this.form.value.corinBio.CB_code
      );
      if (!itemExist && this.form.value.corinBio.CB_code) {
        this.listCorinBio.push(this.form.value.corinBio);
      }
      this.form.get("corinBio").reset();
    }
  }

  onDeleteCorin(CB_code: string) {
    this.listCorinBio = this.listCorinBio.filter((item) => {
      return item.CB_code != CB_code;
    });
  }

  onAddActivity(event, modal) {
    this.patchActivity = false;
    this.modalButtonLabel = "Ajouter";
    this.modalTitle = "Ajout d'une activié humaine";
    this.activityForm = this.fb.group({
      human_activity: [null, Validators.required],
      localisation: null,
      impacts: null,
      remark_activity: null,
      frontId: null,
    });
    event.stopPropagation();
    this.ngbModal.open(modal, {
      centered: true,
      size: "lg",
      windowClass: "bib-modal",
    });
  }

  onPostActivity() {
    if (this.activityForm.valid) {
      let activity = this.activityForm.value;
      let itemExist = this.listActivity.some(
        (item) =>
          item.human_activity.id_nomenclature ==
          activity.human_activity.id_nomenclature
      );
      if (!itemExist) {
        let impactNames = activity.impacts.map((item) => {
          return item["mnemonique"];
        });
        this.listActivity.push({
          frontId: Date.now(),
          human_activity: activity.human_activity,
          localisation: activity.localisation,
          impacts: {
            impacts: activity.impacts,
            mnemonique: impactNames.join("\r\n"),
          },
          remark_activity: activity.remark_activity,
        });
      }
      /*       this.activitiesInput = this.activitiesInput.filter((item) => {
        return item.id_nomenclature != activity.human_activity.id_nomenclature;
      }); */
      this.ngbModal.dismissAll();
      this.activityForm.reset();
      this.selectedItems = [];
    }
  }

  onEditActivity(modal: any, activity: any) {
    this.patchActivity = true;
    this.modalButtonLabel = "Modifier";
    this.modalTitle = "Modifier l'activié humaine";
    this.selectedItems = activity.impacts.impacts;
    this.activityForm.patchValue({
      human_activity: activity.human_activity,
      localisation: activity.localisation,
      impacts: activity.impacts.impacts,
      remark_activity: activity.remark_activity,
      frontId: activity.frontId,
    });
    this.ngbModal.open(modal, {
      centered: true,
      size: "lg",
      windowClass: "bib-modal",
    });
  }

  onPatchActivity() {
    this.patchActivity = false;
    if (this.activityForm.valid) {
      let activity = this.activityForm.value;
      let impactNames = activity.impacts.map((item) => {
        return item["mnemonique"];
      });
      activity.impacts = {
        impacts: activity.impacts,
        mnemonique: impactNames.join("\r\n"),
      };
      this.listActivity = this.listActivity.map((item) =>
        item.frontId != activity.frontId ? item : activity
      );

      this.ngbModal.dismissAll();
      this.activityForm.reset();
      this.selectedItems = [];
    }
  }

  onDeleteActivity(activity: any) {
    this.listActivity = this.listActivity.filter((item) => {
      return item.frontId != activity.frontId;
    });
    /*  console.log('del',activity.human_activity); 
    this.activitiesInput.push(activity.human_activity);
    console.log('del push',this.activitiesInput); */
  }

  onFormSubmit() {
    if (this.form.valid) {
      this.submitted = true;

      let formToPost = {
        id_zh: Number(this._currentZh.properties.id_zh),
        id_sdage: this.form.value.id_sdage,
        id_sage: this.form.value.id_sdage,
        id_corine_landcovers: [],
        corine_biotopes: this.listCorinBio,
        remark_pres: this.form.value.remark_pres,
        id_thread: this.form.value.id_thread,
        global_remark_activity: this.form.value.global_remark_activity,
        activities: this.listActivity,
      };
      if (this.form.value.id_corine_landcovers) {
        this.form.value.id_corine_landcovers.forEach((item) => {
          formToPost.id_corine_landcovers.push(item.id_nomenclature);
        });
      }
      console.log("formToPost", formToPost);
      this.posted = true;
      this._dataService.postDataForm(formToPost, 3).subscribe(
        () => {
          this.form.reset();
          this.posted = false;
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
  }
}
