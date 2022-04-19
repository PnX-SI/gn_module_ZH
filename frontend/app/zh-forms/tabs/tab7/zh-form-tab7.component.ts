import { Component, EventEmitter, OnInit, Input, Output } from "@angular/core";
import { FormGroup, FormBuilder, Validators } from "@angular/forms";
import { NgbModal } from "@ng-bootstrap/ng-bootstrap";
import { ToastrService } from "ngx-toastr";
import { Subscription } from "rxjs";
import { ZhDataService } from "../../../services/zh-data.service";
import { TabsService } from "../../../services/tabs.service";
import { ErrorTranslatorService } from "../../../services/error-translator.service";

@Component({
  selector: "zh-form-tab7",
  templateUrl: "./zh-form-tab7.component.html",
  styleUrls: ["./zh-form-tab7.component.scss"],
})
export class ZhFormTab7Component implements OnInit {
  @Input() public formMetaData: any;
  @Output() public canChangeTab = new EventEmitter<boolean>();
  @Output() nextTab = new EventEmitter<number>();
  public dropdownSettings;
  public formTab7: FormGroup;
  public patchModal: boolean;
  public modalFormSubmitted: boolean;
  public modalTitle: string;
  public addModalBtnLabel: string;
  public actionForm: FormGroup;
  public selectedAction: [any];
  public hydroFctData: any;
  public bioFctData: any;
  public patrimData: any;
  public socEcoData: any;
  public evalZh: any;
  public functionsComment: any;
  public menacesComment: any;
  private $_currentZhSub: Subscription;
  public actionTable: any[] = [];
  public currentZh: any;
  default_prio_level: string = 'Non définie';

  readonly qualifSize: string = "10%";
  readonly knowledgeSize: string = "15%";

  public hydroFctTableCol = [
    {
      name: "function",
      label: "Principales fonctions hydrologiques / biogéochimiques",
      subcell: { name: "mnemonique" },
    },
    {
      name: "qualification",
      label: "Qualifications",
      subcell: { name: "mnemonique" },
      size: this.qualifSize,
    },
    {
      name: "knowledge",
      label: "Connaissance",
      subcell: { name: "mnemonique" },
      size: this.knowledgeSize,
    },
  ];

  public bioFctTableCol = [
    {
      name: "function",
      label: "Principales fonctions biologiques / écologiques",
      subcell: { name: "mnemonique" },
    },
    {
      name: "qualification",
      label: "Qualifications",
      subcell: { name: "mnemonique" },
      size: this.qualifSize,
    },
    {
      name: "knowledge",
      label: "Connaissance",
      subcell: { name: "mnemonique" },
      size: this.knowledgeSize,
    },
  ];

  public patrimTableCol = [
    {
      name: "function",
      label: "Principaux intérêts patrimoniaux",
      subcell: { name: "mnemonique" },
    },
    {
      name: "qualification",
      label: "Qualifications",
      subcell: { name: "mnemonique" },
      size: this.qualifSize,
    },
    {
      name: "knowledge",
      label: "Connaissance",
      subcell: { name: "mnemonique" },
      size: this.knowledgeSize,
    },
  ];

  public actionTableCol = [
    {
      name: "action",
      label: "Propositions d’actions",
      subcell: { name: "name" },
    },
    {
      name: "priority",
      label: "Niveau de priorité",
      subcell: { name: "mnemonique" },
    },
    { name: "remark", label: "Remarques" },
  ];

  public socEcoTableCol = [
    {
      name: "function",
      label: "Principales valeurs socio-economiques",
      subcell: { name: "mnemonique" },
    },
    {
      name: "qualification",
      label: "Qualifications",
      subcell: { name: "mnemonique" },
      size: this.qualifSize,
    },
    {
      name: "knowledge",
      label: "Connaissance",
      subcell: { name: "mnemonique" },
      size: this.knowledgeSize,
    },
  ];

  private tempID: any;
  public actionInput: any;
  public submitted: boolean;
  private $_fromChangeSub: any;
  public posted: boolean;

  constructor(
    private _toastr: ToastrService,
    private fb: FormBuilder,
    public ngbModal: NgbModal,
    private _dataService: ZhDataService,
    private _error: ErrorTranslatorService,
    private _tabService: TabsService
  ) {}

  ngOnInit() {
    this.initForms();
    this.getCurrentZh();
    this._tabService.getTabChange().subscribe((tabPosition: number) => {
      this.$_fromChangeSub.unsubscribe();
      this.$_currentZhSub.unsubscribe();
      if (tabPosition == 7) {
        this.getCurrentZh();
      }
    });
    this.dropdownSettings = {
      enableFilterSelectAll: false,
      enableCheckAll: false,
      text: "Selectionner",
      labelKey: "name",
      primaryKey: "id_action",
      searchPlaceholderText: "Rechercher",
      enableSearchFilter: true,
      singleSelection: true,
      noDataLabel:
        "Toutes les propositions disponibles ont déjà été renseignées dans le tableau",
    };
  }

  initActionInput() {
    this.actionInput = [...this.formMetaData.BIB_ACTIONS];
  }

  // get metaData forms
  getMetaData(action?) {
    this.initActionInput();
    this.actionInput = this.actionInput.filter(
      (item) =>
        !this.actionTable
          .map((m) => m.action.id_action)
          .includes(item.id_action)
    );
    this.selectedAction = null;
    if (action != null) {
      const actionTmp = action.action;
      // push back the action to edit it
      this.actionInput.push(actionTmp);
      this.selectedAction = [actionTmp];
    }
  }

  // initialize forms
  initForms() {
    this.formTab7 = this.fb.group({
      remark_eval_functions: null,
      remark_eval_thread: null,
      remark_eval_actions: null,
    });

    this.actionForm = this.fb.group({
      action: [null, Validators.required],
      priority: [null, Validators.required],
      remark: null,
    });
  }

  // get current zone humides && patch forms values
  getCurrentZh() {
    this.$_currentZhSub = this._dataService.currentZh.subscribe((zh: any) => {
      if (zh) {
        this.currentZh = zh;
        this._dataService.getEvalZh(zh.id).subscribe((evalZh: any) => {
          this.evalZh = evalZh;
          this.hydroFctData = [];
          this.bioFctData = [];
          this.patrimData = [];
          this.socEcoData = [];
          if (evalZh.fonctions_bio && evalZh.fonctions_bio.length > 0) {
            evalZh.fonctions_bio.forEach((fctBio: any) => {
              let namefctBio = this.formMetaData["FONCTIONS_BIO"].find(
                (item: any) => item.id_nomenclature == fctBio.id_function
              );
              let nameQaulif = this.formMetaData["FONCTIONS_QUALIF"].find(
                (item: any) => item.id_nomenclature == fctBio.id_qualification
              );
              let nameKnowledge = this.formMetaData[
                "FONCTIONS_CONNAISSANCE"
              ].find(
                (item: any) => item.id_nomenclature == fctBio.id_knowledge
              );
              this.bioFctData.push({
                function: namefctBio,
                qualification: nameQaulif,
                knowledge: nameKnowledge,
              });
            });
          }
          if (evalZh.fonctions_hydro && evalZh.fonctions_hydro.length > 0) {
            evalZh.fonctions_hydro.forEach((fctBio: any) => {
              let namefctHydro = this.formMetaData["FONCTIONS_HYDRO"].find(
                (item: any) => item.id_nomenclature == fctBio.id_function
              );
              let nameQaulif = this.formMetaData["FONCTIONS_QUALIF"].find(
                (item: any) => item.id_nomenclature == fctBio.id_qualification
              );
              let nameKnowledge = this.formMetaData[
                "FONCTIONS_CONNAISSANCE"
              ].find(
                (item: any) => item.id_nomenclature == fctBio.id_knowledge
              );
              this.hydroFctData.push({
                function: namefctHydro,
                qualification: nameQaulif,
                knowledge: nameKnowledge,
              });
            });
          }
          if (evalZh.interet_patrim && evalZh.interet_patrim.length > 0) {
            evalZh.interet_patrim.forEach((fctBio: any) => {
              let namePatrim = this.formMetaData["INTERET_PATRIM"].find(
                (item: any) => item.id_nomenclature == fctBio.id_function
              );
              let nameQaulif = this.formMetaData["FONCTIONS_QUALIF"].find(
                (item: any) => item.id_nomenclature == fctBio.id_qualification
              );
              let nameKnowledge = this.formMetaData[
                "FONCTIONS_CONNAISSANCE"
              ].find(
                (item: any) => item.id_nomenclature == fctBio.id_knowledge
              );
              this.patrimData.push({
                function: namePatrim,
                qualification: nameQaulif,
                knowledge: nameKnowledge,
              });
            });
          }
          if (evalZh.val_soc_eco && evalZh.val_soc_eco.length > 0) {
            evalZh.val_soc_eco.forEach((socEco: any) => {
              let nameSocEco = this.formMetaData["VAL_SOC_ECO"].find(
                (item: any) => item.id_nomenclature == socEco.id_function
              );
              let nameQaulif = this.formMetaData["FONCTIONS_QUALIF"].find(
                (item: any) => item.id_nomenclature == socEco.id_qualification
              );
              let nameKnowledge = this.formMetaData[
                "FONCTIONS_CONNAISSANCE"
              ].find(
                (item: any) => item.id_nomenclature == socEco.id_knowledge
              );
              this.socEcoData.push({
                function: nameSocEco,
                qualification: nameQaulif,
                knowledge: nameKnowledge,
              });
            });
          }
          if (evalZh.id_thread) {
            this.evalZh.thread = this.formMetaData["EVAL_GLOB_MENACES"].find(
              (item: any) => item.id_nomenclature == evalZh.id_thread
            );
          }
          if (evalZh.id_diag_bio) {
            this.evalZh.diag_bio = this.formMetaData["FONCTIONNALITE_BIO"].find(
              (item: any) => item.id_nomenclature == evalZh.id_diag_bio
            );
          }
          if (evalZh.id_diag_hydro) {
            this.evalZh.diag_hydro = this.formMetaData[
              "FONCTIONNALITE_HYDRO"
            ].find((item: any) => item.id_nomenclature == evalZh.id_diag_hydro);
          }
        });
        // patch forms values
        this.formTab7.patchValue({
          remark_eval_functions:
            this.currentZh.properties.remark_eval_functions,
          remark_eval_thread: this.currentZh.properties.remark_eval_thread,
          remark_eval_actions: this.currentZh.properties.remark_eval_actions,
        });
        if (
          this.currentZh.properties.actions &&
          this.currentZh.properties.actions.length > 0
        ) {
          this.initActionInput();
          const actionTable = [];
          this.currentZh.properties.actions.forEach((action: any) => {
            actionTable.push({
              action: this.actionInput.find(
                (item: any) => item.id_action == action.id_action
              ),
              priority: this.formMetaData["NIVEAU_PRIORITE"].find(
                (item: any) => item.id_nomenclature == action.id_priority_level
              ),
              remark: action.remark,
            });
          });
          this.actionTable = actionTable;
          this.sortAction(this.actionTable);
        }
      }
      this.$_fromChangeSub = this.formTab7.valueChanges.subscribe(() => {
        this.canChangeTab.emit(false);
      });
    });
  }

  // open the add action modal
  onAddAction(event: any, modal: any) {
    this.getMetaData();
    this.actionForm.controls['priority'].setValue(this.formMetaData["NIVEAU_PRIORITE"].find(
      (item) => {
        if (item.mnemonique == this.default_prio_level) {
          return item;
        }
      }
    ), {onlySelf: true});
    this.patchModal = false;
    this.addModalBtnLabel = "Ajouter";
    this.modalTitle = "Ajout d'une proposition d'action";
    event.stopPropagation();
    const modalRef = this.ngbModal.open(modal, {
      centered: true,
      size: "lg",
      windowClass: "bib-modal",
    });
    modalRef.result.then().finally(() => {
      this.actionForm.reset();
    });
  }

  onDeSelectAllActions() {
    this.actionForm.get("action").reset();
  }

  // add a new action to action array
  onPostAction() {
    this.modalFormSubmitted = true;
    if (this.actionForm.valid) {
      let formValues = this.actionForm.value;
      formValues.action = formValues.action[0];
      // check if the action to add is already added
      let itemExist = this.actionTable.some(
        (item: any) => item.action.id_action == formValues.action.id_action
      );
      if (!itemExist) {
        this.actionTable.push(formValues);
      }

      this.ngbModal.dismissAll();
      this.actionForm.reset();
      this.canChangeTab.emit(false);
      this.modalFormSubmitted = false;
      this.sortAction(this.actionTable);
    }
  }

  //delete action from the action array
  onDeleteAction(action: any) {
    this.actionTable = this.actionTable.filter((item: any) => {
      return item.action.id_action != action.action.id_action;
    });
    this.canChangeTab.emit(false);
  }

  // open the edit action modal
  onEditAction(modal: any, action: any) {
    this.getMetaData(action);
    this.patchModal = true;
    this.addModalBtnLabel = "Modifier";
    this.modalTitle = "Modifier la proposition d'action";

    // init inputs object type
    const selectedPriority = this.formMetaData["NIVEAU_PRIORITE"].find(
      (item: any) => item.id_nomenclature == action.priority.id_nomenclature
    );
    // patch form values
    this.actionForm.patchValue({
      action: action.action,
      priority: selectedPriority,
      remark: action.remark,
    });
    this.tempID = action.action.id_action;

    const modalRef = this.ngbModal.open(modal, {
      centered: true,
      size: "lg",
      windowClass: "bib-modal",
    });
    modalRef.result.then().finally(() => {
      this.actionForm.reset();
    });
  }

  // edit action and save into actions array
  onPatchAction() {
    this.patchModal = false;
    this.modalFormSubmitted = true;
    if (this.actionForm.valid) {
      let formValues = this.actionForm.value;
      formValues.action = formValues.action[0];
      this.actionTable = this.actionTable.map((item: any) =>
        item.action.id_action != this.tempID ? item : formValues
      );

      this.tempID = null;
      this.ngbModal.dismissAll();
      this.actionForm.reset();
      this.canChangeTab.emit(false);
      this.modalFormSubmitted = false;
      this.sortAction(this.actionTable);
    }
  }

  onFormSubmit() {
    if (this.formTab7.valid) {
      this.submitted = true;
      this.$_fromChangeSub.unsubscribe();
      let actions = [];

      if (this.actionTable && this.actionTable.length > 0) {
        this.actionTable.forEach((item: any) => {
          actions.push({
            id_action: item.action.id_action,
            id_priority_level: item.priority.id_nomenclature,
            remark: item.remark,
          });
        });
      }

      let formToPost = {
        id_zh: Number(this.currentZh.properties.id_zh),
        remark_eval_functions: this.formTab7.value.remark_eval_functions,
        remark_eval_thread: this.formTab7.value.remark_eval_thread,
        remark_eval_actions: this.formTab7.value.remark_eval_actions,
        actions: actions,
      };

      this.posted = true;
      this._dataService.postDataForm(formToPost, 7).subscribe(
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
              this.nextTab.emit(8);
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

  sortAction(action) {
    const sortingArr = this.formMetaData["NIVEAU_PRIORITE"].map(
      (item) => item.mnemonique
    );
    action.sort(function (a, b) {
      return (
        sortingArr.indexOf(a.priority.mnemonique) -
        sortingArr.indexOf(b.priority.mnemonique)
      );
    });
  }
}
