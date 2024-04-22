import { Component, EventEmitter, OnInit, Input, Output } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { NgbDateParserFormatter, NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { NgbDatepickerI18n } from '@ng-bootstrap/ng-bootstrap';

import { NgbDateFRParserFormatter } from '../../../services/dateFrFormatter';
import { TabsService } from '../../../services/tabs.service';
import { ModalService } from '../../../services/modal.service';
import { ConfigService } from '@geonature/services/config.service';

import { ToastrService } from 'ngx-toastr';
import { Subscription } from 'rxjs';
import { DatepickerI18n, I18n } from '../../../services/datepicker-i18n.service';

import { ZhDataService } from '../../../services/zh-data.service';
import { ErrorTranslatorService } from '../../../services/error-translator.service';

@Component({
  selector: 'zh-form-tab6',
  templateUrl: './zh-form-tab6.component.html',
  styleUrls: ['./zh-form-tab6.component.scss'],
  providers: [
    I18n,
    { provide: NgbDatepickerI18n, useClass: DatepickerI18n },
    { provide: NgbDateParserFormatter, useClass: NgbDateFRParserFormatter },
  ],
})
export class ZhFormTab6Component implements OnInit {
  @Input() public formMetaData: any;
  @Output() public canChangeTab = new EventEmitter<boolean>();
  @Output() nextTab = new EventEmitter<number>();
  // FIXME: only used for URL path... Must be a better way to do this..
  public formTab6: FormGroup;
  public statusForm: FormGroup;
  public instrumentForm: FormGroup;
  public urbanDocForm: FormGroup;
  public planForm: FormGroup;
  public statusInput: any;
  public instrumentInput: any;
  public planInput: any;
  public municipalities: any;
  public typeClassementInput: any;
  public patchModal: boolean;
  public addModalBtnLabel: string;
  public modalTitle: string;
  public modalFormSubmitted: boolean;
  public statusTable: any[] = [];
  public instrumentTable: any[] = [];
  public urbanDocTable: any[] = [];
  public structures: {
    id_org: number;
    name: string;
    abbreviation: string;
    is_op_org: boolean;
    plans: [];
  }[] = [];
  public managements: any[] = [];
  public plans: any[] = [];
  private tempID: any;
  private $_currentZhSub: Subscription;
  private $_fromChangeSub: Subscription;
  private $_getTabChangeSub: Subscription;
  public selectedItems = [];
  default_status: string = 'Indéterminé';

  readonly urbanColSize: string = '15%';

  public statusTableCol = [
    {
      name: 'status',
      label: 'Statut',
      subcell: { name: 'mnemonique' },
      size: '45%',
    },
    { name: 'remark', label: 'Remarques' },
  ];

  public instrumentTableCol = [
    {
      name: 'instrument',
      label: 'Instruments contractuels et financiers',
      subcell: { name: 'mnemonique' },
    },
    { name: 'instrument_date', label: 'Date de mise en oeuvre' },
  ];

  public urbanDocTableCol = [
    {
      name: 'area',
      label: 'Commune',
      subcell: { name: 'municipality_name' },
      size: this.urbanColSize,
    },
    {
      name: 'urbanType',
      label: 'Type de document communal',
      subcell: { name: 'mnemonique' },
      size: this.urbanColSize,
    },
    {
      name: 'typeClassement',
      label: 'Type de classement',
      subcell: { name: 'mnemonique' },
      size: this.urbanColSize,
    },
    { name: 'remark', label: 'Remarques' },
  ];
  public planTableCol = [
    { name: 'plan', label: 'Nature du plan de gestion' },
    { name: 'plan_date', label: 'Date de réalisation' },
    { name: 'duration', label: 'Durée (années)' },
    { name: 'remark', label: 'Remarques' },
  ];

  public dropdownSettings: any;
  public multiselectTypeClassement: any;
  public organismDropdownSettings: {
    enableSearchFilter: boolean;
    singleSelection: boolean;
    text: string;
    labelKey: string;
    primaryKey: string;
    enableFilterSelectAll: boolean;
    noDataLabel: string;
  };
  public currentZh: any;
  selectedManagement: any;
  posted: boolean;
  submitted: boolean;

  constructor(
    private fb: FormBuilder,
    private dateParser: NgbDateParserFormatter,
    public ngbModal: NgbModal,
    private _dataService: ZhDataService,
    private _toastr: ToastrService,
    private _modalService: ModalService,
    private _error: ErrorTranslatorService,
    private _tabService: TabsService,
    public config: ConfigService
  ) {}

  ngOnInit() {
    this.multiselectTypeClassement = {
      singleSelection: false,
      idField: 'id_cor',
      textField: 'mnemonique',
      searchPlaceholderText: 'Rechercher',
      enableCheckAll: false,
      allowSearchFilter: true,
    };
    this.organismDropdownSettings = {
      enableSearchFilter: true,
      singleSelection: true,
      text: 'Sélectionner un organisme',
      labelKey: 'name',
      primaryKey: 'id_org',
      enableFilterSelectAll: false,
      noDataLabel: 'Aucun organisme disponible',
    };
    this.dropdownSettings = {
      enableCheckAll: false,
      text: 'Selectionner',
      labelKey: 'mnemonique_status',
      primaryKey: 'id_protection_status',
      searchPlaceholderText: 'Rechercher',
      enableSearchFilter: true,
      groupBy: 'category',
      autoposition: false,
      position: 'top',
      maxHeight: 190,
    };

    this.getMetaData();
    this.initForms();

    this.$_getTabChangeSub = this._tabService.getTabChange().subscribe((tabPosition: number) => {
      if (tabPosition == 6) {
        this.getCurrentZh();
        if (this.$_fromChangeSub != undefined) this.$_fromChangeSub.unsubscribe();
        if (this.$_currentZhSub != undefined) this.$_currentZhSub.unsubscribe();
      }
    });
  }

  // initialize forms
  initForms(): void {
    this.formTab6 = this.fb.group({
      protections: null,
      structure: null,
      is_other_inventory: false,
      remark_is_other_inventory: null,
    });

    this.statusForm = this.fb.group({
      status: [null, Validators.required],
      remark: null,
    });

    this.instrumentForm = this.fb.group({
      instrument: [null, Validators.required],
      instrument_date: [null],
    });

    this.urbanDocForm = this.fb.group({
      area: [null, Validators.required],
      urbanType: [null, Validators.required],
      typeClassement: [null, Validators.required],
      remark: null,
    });

    this.planForm = this.fb.group({
      plan: [null, Validators.required],
      plan_date: [null, Validators.required],
      duration: [null, Validators.compose([Validators.required, Validators.min(0)])],
      remark: null,
    });
  }

  // get metaData forms
  getMetaData() {
    this.statusInput = this.formMetaData['STATUT_PROPRIETE'];
    // add disabled property to statusInput options list
    this.statusInput.map((item: any) => {
      item.disabled = false;
    });
    this.instrumentInput = this.formMetaData['INSTRU_CONTRAC_FINANC'];
    this.instrumentInput.map((item: any) => {
      item.disabled = false;
    });
  }

  // get current zone humides && patch forms values
  getCurrentZh() {
    this.$_currentZhSub = this._dataService.currentZh.subscribe((zh: any) => {
      if (zh) {
        this.currentZh = zh;
        this._dataService.getMunicipalitiesByZh(zh.id).subscribe((municipalities: any) => {
          this.statusTable = [];
          this.urbanDocTable = [];
          this.managements = [];
          this.instrumentTable = [];
          this.municipalities = municipalities;
          //patch forms values
          let protections = [];
          if (
            this.currentZh.properties.protections &&
            this.currentZh.properties.protections.length > 0
          ) {
            this.currentZh.properties.protections.forEach((element) => {
              let protection = this.formMetaData['PROTECTIONS'].find(
                (item: any) => item.id_protection_status == element
              );

              protections.push(protection);
            });
          }
          this.formTab6.patchValue({
            protections: protections,
            is_other_inventory: this.currentZh.properties.is_other_inventory,
            remark_is_other_inventory: this.currentZh.properties.remark_is_other_inventory,
          });
          if (
            this.currentZh.properties.ownerships &&
            this.currentZh.properties.ownerships.length > 0
          ) {
            this.currentZh.properties.ownerships.forEach((owner: any) => {
              this.statusTable.push({
                status: this.formMetaData['STATUT_PROPRIETE'].find(
                  (item: any) => item.id_nomenclature == owner.id_status
                ),
                remark: owner.remark,
              });
              this.statusInput.map((item: any) => {
                if (item.id_nomenclature == owner.id_status) {
                  item.disabled = true;
                }
              });
            });
          }
          if (
            this.currentZh.properties.instruments &&
            this.currentZh.properties.instruments.length > 0
          ) {
            this.currentZh.properties.instruments.forEach((instrument: any) => {
              this.instrumentTable.push({
                instrument: this.formMetaData['INSTRU_CONTRAC_FINANC'].find(
                  (item: any) => item.id_nomenclature == instrument.id_instrument
                ),
                instrument_date: instrument.instrument_date,
              });
              this.instrumentInput.map((item: any) => {
                if (item.id_nomenclature == instrument.id_instrument) {
                  item.disabled = true;
                }
              });
            });
          }
          if (
            this.currentZh.properties.managements &&
            this.currentZh.properties.managements.length > 0
          ) {
            this.currentZh.properties.managements.forEach((management: any) => {
              let structure = this.formMetaData['BIB_MANAGEMENT_STRUCTURES'].find(
                (item: any) => item.id_org == management.structure
              );
              let plans = [];
              if (management.plans && management.plans.length > 0) {
                management.plans.forEach((plan) => {
                  plans.push({
                    plan: this.formMetaData['PLAN_GESTION'].find(
                      (item: any) => item.id_nomenclature == plan.id_nature
                    ),
                    plan_date: plan.plan_date,
                    duration: plan.duration,
                    remark: plan.remark,
                  });
                });
              }
              structure.plans = plans;

              // moreDetails enable to expand the table to show the plans
              // set it to true by default
              structure.moreDetails = true;

              this.managements.push(structure);
            });
          }
          if (
            this.currentZh.properties.urban_docs &&
            this.currentZh.properties.urban_docs.length > 0
          ) {
            this.currentZh.properties.urban_docs.forEach((doc: any) => {
              let docType = this.formMetaData['TYP_DOC_COMM'].find(
                (item: any) => item.id_nomenclature == doc.id_doc_type
              );
              let typeClassement = [];
              if (docType.type_classement) {
                doc.id_cors.forEach((idCor) => {
                  let temp = docType.type_classement.find((item: any) => item.id_cor == idCor);
                  typeClassement.push(temp);
                });
              }
              let classementNames = typeClassement.map((item) => {
                return item['mnemonique'];
              });
              this.urbanDocTable.push({
                area: this.municipalities.find((item: any) => item.id_area == doc.id_area),
                urbanType: docType,
                typeClassement: {
                  typeClassement: typeClassement,
                  mnemonique: classementNames.join('\r\n'),
                },
                remark: doc.remark,
              });
              this.municipalities.map((item: any) => {
                if (item.id_area == doc.id_area) {
                  item.disabled = true;
                }
              });
            });
            this.sortUrbanDocs();
          }
        });
        this.$_fromChangeSub = this.formTab6.valueChanges.subscribe(() => {
          this.canChangeTab.emit(false);
        });
      }
    });
  }

  // open the add status modal
  onAddStatus(event: any, modal: any) {
    this.statusForm.reset();
    this.statusForm.controls['status'].setValue(
      this.formMetaData['STATUT_PROPRIETE'].find((item) => {
        if (item.mnemonique == this.default_status) {
          return item;
        }
      })
    );
    this.patchModal = false;
    this.addModalBtnLabel = 'Ajouter';
    this.modalTitle = "Ajout d'un statut de propriété";
    event.stopPropagation();
    this._modalService.open(
      modal,
      this.statusTable.map((item) => item.status),
      this.statusInput
    );
  }

  // add a new status to status array
  onPostStatus() {
    this.modalFormSubmitted = true;
    if (this.statusForm.valid) {
      let formValues = this.statusForm.value;
      // check if the status to add is already added
      let itemExist = this.statusTable.some(
        (item: any) => item.status.id_nomenclature == formValues.status.id_nomenclature
      );
      if (!itemExist) {
        this.statusTable.push(formValues);
      }
      // disable the added status on the select input list
      this.statusInput.map((item: any) => {
        if (item.id_nomenclature == formValues.status.id_nomenclature) {
          item.disabled = true;
        }
      });

      this.ngbModal.dismissAll();
      this.statusForm.reset();
      this.canChangeTab.emit(false);
      this.modalFormSubmitted = false;
    }
  }

  //delete status from the status array
  onDeleteStatus(status: any) {
    this.statusTable = this.statusTable.filter((item: any) => {
      return item.status.id_nomenclature != status.status.id_nomenclature;
    });
    this.statusInput.map((item: any) => {
      if (item.id_nomenclature == status.status.id_nomenclature) {
        item.disabled = false;
      }
    });
    this.canChangeTab.emit(false);
  }

  // open the edit status modal
  onEditStatus(modal: any, status: any) {
    this.patchModal = true;
    this.addModalBtnLabel = 'Modifier';
    this.modalTitle = 'Modifier le statut de propriété';
    // init inputs object type
    const selectedStatus = this.statusInput.find(
      (item: any) => item.id_nomenclature == status.status.id_nomenclature
    );
    // patch form values
    this.statusForm.patchValue({
      status: selectedStatus,
      remark: status.remark,
    });
    this.tempID = status.status.id_nomenclature;

    this._modalService.open(
      modal,
      this.statusTable.map((item) => item.status),
      this.statusInput,
      status.status
    );
  }

  // edit status and save into status array
  onPatchStatus() {
    this.patchModal = false;
    this.modalFormSubmitted = true;
    if (this.statusForm.valid) {
      let formValues = this.statusForm.value;
      this.statusTable = this.statusTable.map((item: any) =>
        item.status.id_nomenclature != this.tempID ? item : formValues
      );
      this.tempID = null;
      this.statusInput.map((item: any) => {
        if (item.id_nomenclature == formValues.status.id_nomenclature) {
          item.disabled = true;
        }
      });
      this.ngbModal.dismissAll();
      this.statusForm.reset();
      this.canChangeTab.emit(false);
      this.modalFormSubmitted = false;
    }
  }

  // open the add instrument modal
  onAddInstrument(event: any, modal: any) {
    this.instrumentForm.reset();
    this.patchModal = false;
    this.addModalBtnLabel = 'Ajouter';
    this.modalTitle = "Ajout d'un instrument contractuel et financier";
    event.stopPropagation();
    this._modalService.open(
      modal,
      this.instrumentTable.map((item) => item.instrument),
      this.instrumentInput
    );
  }

  // add a new Instrument to Instrument array
  onPostInstrument() {
    this.modalFormSubmitted = true;
    if (this.instrumentForm.valid) {
      let formValues = this.instrumentForm.value;
      // check if the instrument to add is already added
      let itemExist = this.instrumentTable.some(
        (item: any) => item.instrument.id_nomenclature == formValues.instrument.id_nomenclature
      );
      formValues.instrument_date = this.dateParser.format(formValues.instrument_date) || null;

      if (!itemExist) {
        this.instrumentTable.push(formValues);
      }

      this.ngbModal.dismissAll();
      this.instrumentForm.reset();
      this.canChangeTab.emit(false);
      this.modalFormSubmitted = false;
    }
  }

  //delete instrument from the instrument array
  onDeleteInstrument(instrument: any) {
    this.instrumentTable = this.instrumentTable.filter((item: any) => {
      return item.instrument.id_nomenclature != instrument.instrument.id_nomenclature;
    });
    this.canChangeTab.emit(false);
  }

  // open the edit instrument modal
  onEditInstrument(modal: any, instrument: any) {
    this.patchModal = true;
    this.addModalBtnLabel = 'Modifier';
    this.modalTitle = "Modifier l'instrument contractuel et financier";
    // init inputs object type
    const selectedinstrument = this.instrumentInput.find(
      (item: any) => item.id_nomenclature == instrument.instrument.id_nomenclature
    );
    // patch form values
    this.instrumentForm.patchValue({
      instrument: selectedinstrument,
      instrument_date: this.dateParser.parse(instrument.instrument_date),
    });
    this.tempID = instrument.instrument.id_nomenclature;
    this._modalService.open(
      modal,
      this.instrumentTable.map((item) => item.instrument),
      this.instrumentInput,
      instrument.instrument
    );
  }

  // edit instrument and save into instruments array
  onPatchInstrument() {
    this.patchModal = false;
    this.modalFormSubmitted = true;
    if (this.instrumentForm.valid) {
      let formValues = this.instrumentForm.value;
      formValues.instrument_date = this.dateParser.format(formValues.instrument_date);
      this.instrumentTable = this.instrumentTable.map((item: any) =>
        item.instrument.id_nomenclature != this.tempID ? item : formValues
      );
      this.tempID = null;
      this.instrumentInput.map((item: any) => {
        if (item.id_nomenclature == formValues.instrument.id_nomenclature) {
          item.disabled = true;
        }
      });
      this.ngbModal.dismissAll();
      this.instrumentForm.reset();
      this.canChangeTab.emit(false);
      this.modalFormSubmitted = false;
    }
  }

  // open the add urbanDoc modal
  onAddUrbanDoc(event: any, modal: any) {
    this.patchModal = false;
    this.addModalBtnLabel = 'Ajouter';
    this.modalTitle = "Ajout d'un zonage d'urbanisme";
    event.stopPropagation();
    const modalRef = this.ngbModal.open(modal, {
      centered: true,
      size: 'lg',
      windowClass: 'bib-modal',
    });
    let $_urbanTypeInputSub = this.urbanDocForm.get('urbanType').valueChanges.subscribe((val) => {
      this.urbanDocForm.get('typeClassement').reset();
      if (val) this.typeClassementInput = val.type_classement;
    });

    modalRef.result.then().finally(() => {
      $_urbanTypeInputSub.unsubscribe();
      this.urbanDocForm.reset();
      this.typeClassementInput = null;
    });
  }

  // add a new urbanDoc to urbanDoc array
  onPostUrbanDoc() {
    this.modalFormSubmitted = true;
    if (this.urbanDocForm.valid) {
      let formValues = this.urbanDocForm.value;
      // check if the urbanDoc to add is already added
      let itemExist = this.urbanDocTable.some(
        (item: any) => item.area.id_area == formValues.area.id_area
      );
      if (!itemExist) {
        if (formValues.typeClassement && formValues.typeClassement.length > 0) {
          let classementNames = formValues.typeClassement.map((item) => {
            return item['mnemonique'];
          });
          formValues.typeClassement = {
            typeClassement: formValues.typeClassement,
            mnemonique: classementNames.join('\r\n'),
          };
        }
        this.urbanDocTable.push(formValues);
        this.sortUrbanDocs();
      }
      // disable the added urbanDoc on the municipalities list
      this.municipalities.map((item: any) => {
        if (item.id_area == formValues.area.id_area) {
          item.disabled = true;
        }
      });

      this.ngbModal.dismissAll();
      this.urbanDocForm.reset();
      this.canChangeTab.emit(false);
      this.modalFormSubmitted = false;
    }
  }

  //delete urbanDoc from the urbanDoc array
  onDeleteUrbanDoc(urbanDoc: any) {
    this.urbanDocTable = this.urbanDocTable.filter((item: any) => {
      return item.area.id_area != urbanDoc.area.id_area;
    });
    this.municipalities.map((item: any) => {
      if (item.id_area == urbanDoc.area.id_area) {
        item.disabled = false;
      }
    });
    this.canChangeTab.emit(false);
  }

  // open the edit urbanDoc modal
  onEditUrbanDoc(modal: any, urbanDoc: any) {
    this.patchModal = true;
    this.addModalBtnLabel = 'Modifier';
    this.modalTitle = "Modifier le zonage d'urbanisme";
    // init inputs object type
    const selectedArea = this.municipalities.find(
      (item: any) => item.id_area == urbanDoc.area.id_area
    );
    const selecteurbanType = this.formMetaData.TYP_DOC_COMM.find(
      (item: any) => item.id_nomenclature == urbanDoc.urbanType.id_nomenclature
    );
    this.typeClassementInput = selecteurbanType.type_classement;
    // patch form values
    this.urbanDocForm.patchValue({
      area: selectedArea,
      urbanType: selecteurbanType,
      typeClassement: urbanDoc.typeClassement.typeClassement,
      remark: urbanDoc.remark,
    });
    let $_urbanTypeInputSub = this.urbanDocForm.get('urbanType').valueChanges.subscribe((val) => {
      this.urbanDocForm.get('typeClassement').reset();
      if (val) this.typeClassementInput = val.type_classement;
    });

    this.tempID = urbanDoc.area.id_area;
    // manger disabled urbanDoc input items
    let $_areaInputSub = this.urbanDocForm.get('area').valueChanges.subscribe(() => {
      this.municipalities.map((item: any) => {
        if (item.id_area == urbanDoc.area.id_area) {
          item.disabled = false;
        }
      });
    });
    const modalRef = this.ngbModal.open(modal, {
      centered: true,
      size: 'lg',
      windowClass: 'bib-modal',
    });
    modalRef.result.then().finally(() => {
      $_areaInputSub.unsubscribe();
      $_urbanTypeInputSub.unsubscribe();
      this.urbanDocForm.reset();
    });
  }

  // edit urbanDoc and save into urbanDocs array
  onPatchUrbanDoc() {
    this.patchModal = false;
    this.modalFormSubmitted = true;
    if (this.urbanDocForm.valid) {
      let formValues = this.urbanDocForm.value;
      if (formValues.typeClassement && formValues.typeClassement.length > 0) {
        let classementNames = formValues.typeClassement.map((item) => {
          return item['mnemonique'];
        });
        formValues.typeClassement = {
          typeClassement: formValues.typeClassement,
          mnemonique: classementNames.join('\r\n'),
        };
      }
      this.urbanDocTable = this.urbanDocTable.map((item: any) =>
        item.area.id_area != this.tempID ? item : formValues
      );
      this.sortUrbanDocs();
      this.tempID = null;
      this.municipalities.map((item: any) => {
        if (item.id_area == formValues.area.id_area) {
          item.disabled = true;
        }
      });
      this.ngbModal.dismissAll();
      this.urbanDocForm.reset();
      this.canChangeTab.emit(false);
      this.modalFormSubmitted = false;
    }
  }

  onStructureOpened() {
    // When the multiselect is opened
    // Filter the structure with the ones present in the table
    this.structures = this.formMetaData.BIB_MANAGEMENT_STRUCTURES.filter(
      (item) => !this.managements.map((m) => m.id_org).includes(item.id_org)
    );
  }

  onAddStructure() {
    // multi select : returns an Array...
    const structure = this.formTab6.value.structure;
    if (structure) {
      const itemExist = this.managements.some((item) => item.id_org == structure.id_org);
      if (!itemExist && structure.id_org) {
        this.managements.push(structure);
      }
      this.formTab6.get('structure').reset();
      this.canChangeTab.emit(false);
    }
  }

  onAllStructuresDeselected() {
    this.formTab6.get('structure').reset();
  }

  onDeleteStrutureModal(modal, structure) {
    this.ngbModal
      .open(modal, {
        centered: true,
        size: 'lg',
        windowClass: 'bib-modal',
      })
      .result.then(
        () => {
          //When suppr is clicked
          this.onDeleteStructure(structure);
        },
        () => {}
      );
  }

  //delete Structure from the StructureS array
  onDeleteStructure(structure: any) {
    structure.plans = [];
    this.managements = this.managements.filter((item: any) => {
      return item.id_org != structure.id_org;
    });
    this.canChangeTab.emit(false);
  }

  // open the add plan modal
  onAddPlan(event: any, management: any, modal: any) {
    this.patchModal = false;
    this.addModalBtnLabel = 'Ajouter';
    this.modalTitle = "Ajout d'un plan de gestion";
    event.stopPropagation();
    this.selectedManagement = management;
    this.planInput = [...this.formMetaData['PLAN_GESTION']];
    this.planInput.map((item: any) => {
      item.disabled = false;
      if (this.selectedManagement.plans && this.selectedManagement.plans.length > 0) {
        this.selectedManagement.plans.forEach((plan) => {
          if (plan.plan.id_nomenclature == item.id_nomenclature) item.disabled = true;
        });
      }
    });
    const modalRef = this.ngbModal.open(modal, {
      centered: true,
      size: 'lg',
      windowClass: 'bib-modal',
    });
    modalRef.result.then().finally(() => {
      this.planForm.reset();
      this.selectedManagement = null;
    });
  }

  // add a new plan to plan array
  onPostPlan() {
    this.modalFormSubmitted = true;
    if (this.planForm.valid) {
      let formValues = this.planForm.value;
      this.managements.map((item: any) => {
        if (item.id_org == this.selectedManagement.id_org) {
          if (!item.plans || item.plans.length == 0) {
            formValues.plan_date = this.dateParser.format(formValues.plan_date);
            item.plans = [formValues];
          } else if (item.plans && item.plans.length > 0) {
            let palnExist = item.plans.some(
              (item: any) => item.plan.id_nomenclature == formValues.plan.id_nomenclature
            );
            if (!palnExist) {
              formValues.plan_date = this.dateParser.format(formValues.plan_date);
              // moreDetails enable to expand the table to show the plans
              // set it to true here enable to expand when plan is added
              item.moreDetails = true;
              item.plans.push(formValues);
            }
          }
        }
      });
      this.selectedManagement = null;
      this.ngbModal.dismissAll();
      this.planForm.reset();
      this.canChangeTab.emit(false);
      this.modalFormSubmitted = false;
    }
  }

  onDeletePlanModal(modal, plan, structure) {
    this.ngbModal
      .open(modal, {
        centered: true,
        size: 'lg',
        windowClass: 'bib-modal',
      })
      .result.then(
        () => {
          //When suppr is clicked
          this.onDeletePlan(plan, structure);
        },
        () => {}
      );
  }

  //delete plan from the plan array
  onDeletePlan(plan: any, structure: any) {
    this.managements.map((item: any) => {
      if (item.id_org == structure.id_org) {
        if (item.plans && item.plans.length > 0) {
          item.plans = item.plans.filter((item: any) => {
            return item.plan.id_nomenclature != plan.plan.id_nomenclature;
          });
        }
      }
    });
    this.canChangeTab.emit(false);
  }

  // open the edit plan modal
  onEditPlan(modal: any, plan: any, management: any) {
    this.patchModal = true;
    this.addModalBtnLabel = 'Modifier';
    this.modalTitle = 'Modifier un plan de gestion';
    this.selectedManagement = management;
    this.planInput = [...this.formMetaData['PLAN_GESTION']];
    this.planInput.map((item: any) => {
      item.disabled = false;
      if (this.selectedManagement.plans && this.selectedManagement.plans.length > 0) {
        this.selectedManagement.plans.forEach((plan) => {
          if (plan.plan.id_nomenclature == item.id_nomenclature) item.disabled = true;
        });
      }
    });

    // init inputs object type
    const selectedPlan = this.planInput.find(
      (item: any) => item.id_nomenclature == plan.plan.id_nomenclature
    );

    // patch form values
    this.planForm.patchValue({
      plan: selectedPlan,
      plan_date: this.dateParser.parse(plan.plan_date),
      duration: plan.duration,
      remark: plan.remark,
    });

    let $_planInputSub = this.planForm.get('plan').valueChanges.subscribe(() => {
      this.planInput.map((item: any) => {
        if (item.id_nomenclature == plan.plan.id_nomenclature) {
          item.disabled = false;
        }
      });
    });

    this.tempID = plan.plan.id_nomenclature;

    const modalRef = this.ngbModal.open(modal, {
      centered: true,
      size: 'lg',
      windowClass: 'bib-modal',
    });
    modalRef.result.then().finally(() => {
      $_planInputSub.unsubscribe();
      this.planForm.reset();
    });
  }

  // edit plan and save into plans array
  onPatchPlan() {
    this.patchModal = false;
    this.modalFormSubmitted = true;
    if (this.planForm.valid) {
      let formValues = this.planForm.value;
      formValues.plan_date = this.dateParser.format(formValues.plan_date);
      this.managements.map((item: any) => {
        if (item.id_org == this.selectedManagement.id_org) {
          if (item.plans && item.plans.length > 0) {
            item.plans = item.plans.map((item: any) =>
              item.plan.id_nomenclature != this.tempID ? item : formValues
            );
          }
        }
      });
      this.tempID = null;
      this.ngbModal.dismissAll();
      this.planForm.reset();
      this.canChangeTab.emit(false);
      this.modalFormSubmitted = false;
    }
  }

  onMoreDetails(item) {
    item.moreDetails = !item.moreDetails;
  }

  onDeSelectAll() {
    this.formTab6.get('protections').reset();
  }

  handleEnterKeyPress() {
    return false;
  }

  onFormSubmit() {
    if (this.formTab6.valid) {
      this.submitted = true;
      //this.$_fromChangeSub.unsubscribe();
      let managements = [];
      let urban_docs = [];
      let instruments = [];
      let protections = [];
      let ownerships = [];

      if (this.managements && this.managements.length > 0) {
        this.managements.forEach((item: any) => {
          let plans = [];
          if (item.plans && item.plans.length > 0) {
            item.plans.forEach((item: any) => {
              plans.push({
                id_nature: item.plan.id_nomenclature,
                plan_date: item.plan_date,
                duration: item.duration,
                remark: item.remark,
              });
            });
          }
          managements.push({
            structure: item.id_org,
            plans: plans,
          });
        });
      }

      if (this.statusTable && this.statusTable.length > 0) {
        this.statusTable.forEach((item: any) => {
          ownerships.push({
            id_status: item.status.id_nomenclature,
            remark: item.remark,
          });
        });
      }
      if (this.instrumentTable && this.instrumentTable.length > 0) {
        this.instrumentTable.forEach((item: any) => {
          instruments.push({
            id_instrument: item.instrument.id_nomenclature,
            instrument_date: item.instrument_date,
          });
        });
      }
      if (this.urbanDocTable && this.urbanDocTable.length > 0) {
        this.urbanDocTable.forEach((item: any) => {
          urban_docs.push({
            id_area: item.area.id_area,
            id_urban_type: item.typeClassement.typeClassement,
            remark: item.remark,
          });
        });
      }
      if (this.formTab6.value.protections && this.formTab6.value.protections.length > 0) {
        this.formTab6.value.protections.forEach((item: any) => {
          protections.push(item.id_protection_status);
        });
      }

      let formToPost = {
        id_zh: Number(this.currentZh.properties.id_zh),
        ownerships: ownerships,
        managements: managements,
        instruments: instruments,
        protections: protections,
        is_other_inventory: this.formTab6.value.is_other_inventory,
        remark_is_other_inventory: this.formTab6.value.remark_is_other_inventory,
        urban_docs: urban_docs,
      };

      this.posted = true;
      this._dataService.postDataForm(formToPost, 6).subscribe(
        () => {
          this._dataService.getZhById(this.currentZh.properties.id_zh).subscribe((zh: any) => {
            this._dataService.setCurrentZh(zh);
            this.posted = false;
            this.canChangeTab.emit(true);
            this._toastr.success('Vos données sont bien enregistrées', '', {
              positionClass: 'toast-top-right',
            });
            this.nextTab.emit(7);
          });
        },
        (error) => {
          this.posted = false;
          const frontMsg: string = this._error.getFrontError(error.error.message);
          this._toastr.error(frontMsg, '', {
            positionClass: 'toast-top-right',
          });
        }
      );
    }
  }

  sortUrbanDocs() {
    this.urbanDocTable.sort((a, b) =>
      a.area.municipality_name > b.area.municipality_name
        ? 1
        : b.area.municipality_name > a.area.municipality_name
          ? -1
          : 0
    );
  }

  //keep this code and propagate it to other tabs
  ngOnDestroy() {
    if (this.$_getTabChangeSub) this.$_getTabChangeSub.unsubscribe();
    if (this.$_currentZhSub) this.$_currentZhSub.unsubscribe();
  }
}
