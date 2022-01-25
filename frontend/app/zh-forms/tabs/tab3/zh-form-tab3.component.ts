import { Component, EventEmitter, OnInit, Input, Output } from "@angular/core";
import { FormGroup, FormBuilder, Validators } from "@angular/forms";
import { ZhDataService } from "../../../services/zh-data.service";
import { NgbModal } from "@ng-bootstrap/ng-bootstrap";
import { Subscription, Observable } from "rxjs";
import { debounceTime, distinctUntilChanged, map } from "rxjs/operators";
import { ToastrService } from "ngx-toastr";
import { TabsService } from "../../../services/tabs.service";
import { ModalService } from "../../../services/modal.service";
import { ErrorTranslatorService } from "../../../services/error-translator.service";

@Component({
  selector: "zh-form-tab3",
  templateUrl: "./zh-form-tab3.component.html",
  styleUrls: ["./zh-form-tab3.component.scss"],
})
export class ZhFormTab3Component implements OnInit {
  @Input() formMetaData;
  @Output() canChangeTab = new EventEmitter<boolean>();
  @Output() nextTab = new EventEmitter<number>();
  form: FormGroup;
  sage: any;
  allSage: any;
  $_currentZhSub: Subscription;
  $_fromChangeSub: Subscription;
  public currentZh: any;
  corinBioMetaData: any;
  corinTableCol = [
    { name: "CB_code", label: "Code Corine biotopes" },
    { name: "CB_label", label: "Libellé Corine biotopes" },
    { name: "CB_humidity", label: "Humidité", size: "5%" },
  ];
  // subcell : if the data contain a list inside the data list
  //   example use : consider this
  // {
  //   "human_activity": {
  //     "id_nomenclature": 604,
  //     "mnemonique": "02 - sylviculture"
  //   },
  //   "impacts": {
  //     "impacts": [
  //       {
  //         "mnemonique": "12.0- 12.0- zone industrielle ou commerciale",
  //       }
  //     ],
  //   }
  // }
  // then use name for human_activity with name="mnemonique"
  // use key and name for impacts with key="impacts"; name="mnemonique"

  readonly activityColSize: string = "20%";

  activityTableCol = [
    {
      name: "human_activity",
      label: "Activités humaines",
      subcell: { name: "mnemonique" },
      size: this.activityColSize,
    },
    {
      name: "localisation",
      label: "Localisation",
      subcell: { name: "mnemonique" },
      size: this.activityColSize,
    },
    {
      name: "impacts",
      label: "Impacts (facteurs influençant l'évolution de la zone)",
      subcell: { key: "impacts", name: "mnemonique" },
      size: this.activityColSize,
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
  formImpactSubmitted: boolean;

  constructor(
    private fb: FormBuilder,
    private _dataService: ZhDataService,
    private _tabService: TabsService,
    public ngbModal: NgbModal,
    private _modalService: ModalService,
    private _error: ErrorTranslatorService,
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
      maxHeight: 300,
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

    this.activityForm = this.fb.group({
      human_activity: [null, Validators.required],
      localisation: [null, Validators.required],
      impacts: [null, Validators.required],
      remark_activity: null,
      frontId: null,
    });

    this.getMetaData();
    this.createForm();
    this.initTab();

    this._tabService.getTabChange().subscribe((tabPosition: number) => {
      this.$_fromChangeSub.unsubscribe();
      this.$_currentZhSub.unsubscribe();
      if (tabPosition == 3) {
        this.initTab();
      }
    });
  }

  initTab() {
    this.listActivity = [];
    this.$_currentZhSub = this._dataService.currentZh.subscribe((zh: any) => {
      if (zh) {
        this.currentZh = zh;
        this.listActivity = [];
        const corineLandcovers = [];
        this.formMetaData.OCCUPATION_SOLS.forEach((critere) => {
          if (
            this.currentZh.properties.id_corine_landcovers.includes(
              critere.id_nomenclature
            )
          ) {
            corineLandcovers.push(critere);
          }
        });
        if (
          this.currentZh.properties.cb_codes_corine_biotope &&
          this.currentZh.properties.cb_codes_corine_biotope.length > 0
        ) {
          this.listCorinBio = this.corinBioMetaData.filter((v) =>
            this.currentZh.properties.cb_codes_corine_biotope.includes(
              v.CB_code
            )
          );
        }
        this.currentZh.properties.activities.forEach((activity) => {
          let impacts = [];
          activity.ids_impact.forEach((impact) => {
            impacts.push(
              this.formMetaData["IMPACTS"].find((item) => {
                return item.id_cor_impact_types == impact;
              })
            );
          });
          let impactNames = impacts.map((item) => {
            return item["mnemonique"];
          });

          this.listActivity.push({
            frontId: activity.id_human_activity,
            human_activity: {
              id_nomenclature: activity.id_human_activity,
              mnemonique: this.formMetaData["ACTIV_HUM"].find((item) => {
                return item.id_nomenclature == activity.id_human_activity;
              }).mnemonique,
            },
            localisation: {
              id_nomenclature: activity.id_localisation,
              mnemonique: this.formMetaData["LOCALISATION"].find((item) => {
                return item.id_nomenclature == activity.id_localisation;
              }).mnemonique,
            },
            remark_activity: activity.remark_activity,
            impacts: {
              impacts: impacts,
              mnemonique: impactNames.join("\r\n"),
            },
          });
          console.log(this.listActivity);
          this.sortHumanActivities();
          this.activitiesInput.map((item) => {
            if (item.id_nomenclature == activity.id_human_activity) {
              item.disabled = true;
            }
          });
        });
        this.form.patchValue({
          id_sdage: this.currentZh.properties.id_sdage,
          id_sage: this.currentZh.properties.id_sage,
          id_corine_landcovers: corineLandcovers,
          remark_pres: this.currentZh.properties.remark_pres,
          id_thread: this.currentZh.properties.id_thread,
          global_remark_activity:
            this.currentZh.properties.global_remark_activity,
        });
      }

      this.$_fromChangeSub = this.form.valueChanges.subscribe(() => {
        this.canChangeTab.emit(false);
      });
    });
  }

  getMetaData() {
    this.allSage = [...this.formMetaData["SDAGE-SAGE"]];
    this.corinBioMetaData = [...this.formMetaData["CORINE_BIO"]];
    this.activitiesInput = [...this.formMetaData["ACTIV_HUM"]];
    this.activitiesInput.map((item) => {
      item.disabled = false;
    });
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
      ),
      // Not to display a Corine that is already in the table
      map((term) =>
        term.filter(
          (t) => !this.listCorinBio.map((c) => c.CB_code).includes(t.CB_code)
        )
      )
    );

  formatter = (result: any) => `${result.CB_code} ${result.CB_label}`;

  onAddCorinBio() {
    if (this.form.value.corinBio) {
      let itemExist = this.listCorinBio.some(
        (item) => item.CB_code == this.form.value.corinBio.CB_code
      );
      if (!itemExist && this.form.value.corinBio.CB_code) {
        this.listCorinBio.push(this.form.value.corinBio);
      }
      this.form.get("corinBio").reset();
      this.canChangeTab.emit(false);
    }
  }

  onDeleteCorin(CB_code: string) {
    this.listCorinBio = this.listCorinBio.filter((item) => {
      return item.CB_code != CB_code;
    });
    this.canChangeTab.emit(false);
  }

  onAddActivity(event, modal) {
    this.resetActivityForm();

    this.patchActivity = false;
    this.modalButtonLabel = "Ajouter";
    this.modalTitle = "Ajout d'une activité humaine";
    event.stopPropagation();
    this._modalService.open(
      modal,
      this.listActivity.map((item) => item.human_activity),
      this.activitiesInput
    );
  }

  onPostActivity() {
    this.formImpactSubmitted = true;
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
        let acrivityToAdd = {
          frontId: activity.human_activity.id_nomenclature,
          human_activity: activity.human_activity,
          localisation: activity.localisation,
          remark_activity: activity.remark_activity,
          impacts: null,
        };
        if (activity.impacts && activity.impacts.length > 0) {
          acrivityToAdd.impacts = {
            impacts: activity.impacts,
            mnemonique: impactNames.join("\r\n"),
          };
        }
        this.listActivity.push(acrivityToAdd);
      }
      this.activitiesInput.map((item) => {
        if (item.id_nomenclature == activity.human_activity.id_nomenclature) {
          item.disabled = true;
        }
      });
      this.ngbModal.dismissAll();
      this.resetActivityForm();
      this.canChangeTab.emit(false);
      this.formImpactSubmitted = false;
      this.sortHumanActivities();
    }
  }

  onEditActivity(modal: any, activity: any) {
    this.patchActivity = true;
    this.modalButtonLabel = "Modifier";
    this.modalTitle = "Modifier l'activié humaine";
    this.selectedItems = activity.impacts.impacts;
    const selectedActivity = this.activitiesInput.find(
      (item) => item.id_nomenclature == activity.human_activity.id_nomenclature
    );
    const selecteLocalisation = this.formMetaData["LOCALISATION"].find(
      (item) => item.id_nomenclature == activity.localisation.id_nomenclature
    );
    this.activityForm.patchValue({
      human_activity: selectedActivity,
      localisation: selecteLocalisation,
      impacts: activity.impacts.impacts,
      remark_activity: activity.remark_activity,
      frontId: activity.frontId,
    });
    this._modalService.open(
      modal,
      this.listActivity.map((item) => item.human_activity),
      this.activitiesInput,
      activity.human_activity
    );
  }

  onPatchActivity() {
    this.patchActivity = false;
    this.formImpactSubmitted = true;
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
      this.activitiesInput.map((item) => {
        if (item.id_nomenclature == activity.human_activity.id_nomenclature) {
          item.disabled = true;
        }
      });
      this.ngbModal.dismissAll();
      this.resetActivityForm();
      this.canChangeTab.emit(false);
      this.formImpactSubmitted = false;
    }
  }

  onDeleteActivity(activity: any) {
    this.listActivity = this.listActivity.filter((item) => {
      return item.frontId != activity.frontId;
    });
    this.activitiesInput.map((item) => {
      if (item.id_nomenclature == activity.human_activity.id_nomenclature) {
        item.disabled = false;
      }
    });
    this.canChangeTab.emit(false);
  }

  onDeSelectAll() {
    this.activityForm.get("impacts").setValue([]);
  }

  onFormSubmit() {
    if (this.form.valid) {
      this.submitted = true;
      this.$_fromChangeSub.unsubscribe();
      let formToPost = {
        id_zh: Number(this.currentZh.properties.id_zh),
        id_sdage: this.form.value.id_sdage,
        id_sage: this.form.value.id_sage,
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
      this.posted = true;

      this._dataService.postDataForm(formToPost, 3).subscribe(
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
              this.nextTab.emit(4);
            });
        },
        (error) => {
          this.posted = false;
          const frontMsg: string = this._error.getFrontError(
            error.error.message
          );
          this._toastr.error(frontMsg, "", {
            positionClass: "toast-top-right",
          });
        }
      );
    }
  }

  resetActivityForm() {
    this.activityForm.reset();
    this.selectedItems = [];
  }

  sortHumanActivities() {
    this.listActivity.sort((a, b) =>
      a.human_activity.mnemonique.slice(0, 2) >
      b.human_activity.mnemonique.slice(0, 2)
        ? 1
        : b.human_activity.mnemonique.slice(0, 2) >
          a.human_activity.mnemonique.slice(0, 2)
        ? -1
        : 0
    );
  }

  ngOnDestroy() {
    this.$_currentZhSub.unsubscribe();
    this.$_fromChangeSub.unsubscribe();
  }
}
