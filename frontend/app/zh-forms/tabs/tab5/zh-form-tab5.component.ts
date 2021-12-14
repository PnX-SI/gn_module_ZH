import { Component, EventEmitter, OnInit, Input, Output } from "@angular/core";
import { FormGroup, FormBuilder, Validators } from "@angular/forms";
import { NgbModal } from "@ng-bootstrap/ng-bootstrap";
import { ToastrService } from "ngx-toastr";
import { Subscription, Observable } from "rxjs";
import { debounceTime, distinctUntilChanged, map } from "rxjs/operators";
import { ZhDataService } from "../../../services/zh-data.service";
import { TabsService } from "../../../services/tabs.service";
import { ModalService } from "../../../services/modal.service";
import { TaxaFile } from "./zh-form-tab5.models";
import { FilesService } from "../../../services/files.service";
import { ErrorTranslatorService } from "../../../services/error-translator.service";

@Component({
  selector: "zh-form-tab5",
  templateUrl: "./zh-form-tab5.component.html",
  styleUrls: ["./zh-form-tab5.component.scss"],
})
export class ZhFormTab5Component implements OnInit {
  @Input() public formMetaData: any;
  @Output() public canChangeTab = new EventEmitter<boolean>();
  @Output() nextTab = new EventEmitter<number>();
  public formTab5: FormGroup;
  public patchModal: boolean;
  public modalFormSubmitted: boolean;
  public modalTitle: string;
  public addModalBtnLabel: string;
  public hydroFctForm: FormGroup;
  public bioFctForm: FormGroup;
  public interetPatForm: FormGroup;
  public valSocEcoForm: FormGroup;
  public corineBioForm: FormGroup;
  public fctHydroInput: any;
  public bioFctInput: any;
  public valSocEcoInput: any;
  public interetPatInput: any;
  public corineBioInput: any;
  public cahierHabInput: any;
  public fctHydroTable: any[] = [];
  public bioFctTable: any[] = [];
  public interetPatTable: any[] = [];
  public valSocEcoTable: any[] = [];
  public corineBioTable: any[] = [];

  public hydroFctTableCol = [
    {
      name: "function",
      label: "Fonctions hydrologiques / biogéochimiques",
      subcell: { name: "mnemonique" },
    },
    { name: "justification", label: "Justifications" },
    {
      name: "qualification",
      label: "Qualifications",
      subcell: { name: "mnemonique" },
    },
    {
      name: "knowledge",
      label: "Connaissance",
      subcell: { name: "mnemonique" },
    },
  ];
  public bioFctTableCol = [
    {
      name: "function",
      label: "Fonctions biologiques / écologiques",
      subcell: { name: "mnemonique" },
    },
    { name: "justification", label: "Justifications" },
    {
      name: "qualification",
      label: "Qualifications",
      subcell: { name: "mnemonique" },
    },
    {
      name: "knowledge",
      label: "Connaissance",
      subcell: { name: "mnemonique" },
    },
  ];

  public interetsTableCol = [
    {
      name: "function",
      label: "Intérêts patrimoniaux",
      subcell: { name: "mnemonique" },
    },
    { name: "justification", label: "Justifications" },
    {
      name: "qualification",
      label: "Qualifications",
      subcell: { name: "mnemonique" },
    },
    {
      name: "knowledge",
      label: "Connaissance",
      subcell: { name: "mnemonique" },
    },
  ];

  public corineTableCol = [
    {
      name: "corinBio",
      label: "Corine biotopes",
      subcell: { name: "CB_label" },
    },
    {
      name: "cahierHab",
      label: "Cahier d'habitats",
      subcell: { name: "lb_hab_fr" },
    },
    {
      name: "preservationState",
      label: "État de conservation",
      subcell: { name: "mnemonique" },
    },
    { name: "habCover", label: "Recouvrement sur la ZH (%)" },
  ];

  public socioEcoTableCol = [
    {
      name: "function",
      label: "Valeurs socio-économiques",
      subcell: { name: "mnemonique" },
    },
    { name: "justification", label: "Justifications" },
    {
      name: "qualification",
      label: "Qualifications",
      subcell: { name: "mnemonique" },
    },
    {
      name: "knowledge",
      label: "Connaissance",
      subcell: { name: "mnemonique" },
    },
  ];

  public fileTableCol = [
    {
      name: "title_fr",
      label: "Titre du document",
    },
    { name: "author", label: "Auteur" },
    { name: "description_fr", label: "Résumé" },
  ];

  private tempID: any;
  corinBioMetaData: any[];
  public submitted: boolean;
  private $_currentZhSub: Subscription;
  private $_fromChangeSub: Subscription;
  public currentZh: any;
  posted: boolean;
  public taxaLoading: boolean;

  constructor(
    private fb: FormBuilder,
    public ngbModal: NgbModal,
    private _toastr: ToastrService,
    private _dataService: ZhDataService,
    private _modalService: ModalService,
    private _tabService: TabsService,
    private _filesService: FilesService,
    private _error: ErrorTranslatorService
  ) {}

  ngOnInit() {
    this.getMetaData();
    this.initForms();
    this.getCurrentZh();
    this._tabService.getTabChange().subscribe((tabPosition: number) => {
      if (this.$_fromChangeSub) this.$_fromChangeSub.unsubscribe();
      this.$_currentZhSub.unsubscribe();
      if (tabPosition == 5) {
        this.getCurrentZh();
      }
    });
  }

  // initialize forms
  initForms(): void {
    this.formTab5 = this.fb.group({
      is_carto_hab: false,
      nb_hab: [null, Validators.min(0)],
      total_hab_cover: [
        0,
        Validators.compose([Validators.min(0), Validators.max(100)]),
      ],
      nb_flora_sp: [null, Validators.min(0)],
      nb_vertebrate_sp: [null, Validators.min(0)],
      nb_invertebrate_sp: [null, Validators.min(0)],
    });

    this.hydroFctForm = this.fb.group({
      function: [null, Validators.required],
      qualification: [null, Validators.required],
      knowledge: [null, Validators.required],
      justification: null,
    });
    this.bioFctForm = this.fb.group({
      function: [null, Validators.required],
      qualification: [null, Validators.required],
      knowledge: [null, Validators.required],
      justification: null,
    });
    this.interetPatForm = this.fb.group({
      function: [null, Validators.required],
      qualification: [null, Validators.required],
      knowledge: [null, Validators.required],
      justification: null,
    });
    this.valSocEcoForm = this.fb.group({
      function: [null, Validators.required],
      qualification: [null, Validators.required],
      knowledge: [null, Validators.required],
      justification: null,
    });
    this.corineBioForm = this.fb.group({
      corinBio: [null, Validators.required],
      preservationState: [null, Validators.required],
      cahierHab: [{ value: "", disabled: true }, Validators.required],
      habCover: [
        0,
        Validators.compose([Validators.min(0), Validators.max(100)]),
      ],
    });
  }

  // get metaData forms
  getMetaData() {
    this.fctHydroInput = this.groupArrayByCategory(
      this.formMetaData["FONCTIONS_HYDRO"]
    );
    this.bioFctInput = this.groupArrayByCategory(
      this.formMetaData["FONCTIONS_BIO"]
    );
    this.interetPatInput = this.groupArrayByCategory(
      this.formMetaData["INTERET_PATRIM"]
    );
    this.valSocEcoInput = [...this.formMetaData["VAL_SOC_ECO"]];
    this.corinBioMetaData = [...this.formMetaData["CORINE_BIO"]].filter(
      (corine) => corine.CB_is_ch == true
    );
  }

  // group array by category
  groupArrayByCategory(array: any) {
    let group = array.reduce((r, a) => {
      r[a.id_category] = [...(r[a.id_category] || []), a];
      return r;
    }, {});
    let grpupedArray = Object.values(group) as any;
    // add disabled property to inflowInput options list
    grpupedArray.flat().map((item: any) => {
      item.disabled = false;
    });
    return grpupedArray;
  }

  // get current zone humides && patch forms values
  getCurrentZh() {
    this.$_currentZhSub = this._dataService.currentZh.subscribe(
      async (zh: any) => {
        if (zh) {
          this.currentZh = zh;
          //patch forms values
          this.formTab5.patchValue({
            is_carto_hab: this.currentZh.properties.is_carto_hab,
            nb_hab: this.currentZh.properties.nb_hab,
            total_hab_cover: this.currentZh.properties.total_hab_cover,
            nb_flora_sp: this.currentZh.properties.nb_flora_sp,
            nb_vertebrate_sp: this.currentZh.properties.nb_vertebrate_sp,
            nb_invertebrate_sp: this.currentZh.properties.nb_invertebrate_sp,
          });
          if (
            this.currentZh.properties.fonctions_hydro &&
            this.currentZh.properties.fonctions_hydro.length > 0
          ) {
            this.getHydro(this.currentZh.properties.fonctions_hydro);
          }
          if (
            this.currentZh.properties.fonctions_bio &&
            this.currentZh.properties.fonctions_bio.length > 0
          ) {
            this.getBio(this.currentZh.properties.fonctions_bio);
          }
          if (
            this.currentZh.properties.val_soc_eco &&
            this.currentZh.properties.val_soc_eco.length > 0
          ) {
            this.getValSocEco(this.currentZh.properties.val_soc_eco);
          }
          if (
            this.currentZh.properties.interet_patrim &&
            this.currentZh.properties.interet_patrim.length > 0
          ) {
            this.getInteretPatrim(this.currentZh.properties.interet_patrim);
          }
          if (
            this.currentZh.properties.hab_heritages &&
            this.currentZh.properties.hab_heritages.length > 0
          ) {
            await this.getCorineBio(this.currentZh.properties.hab_heritages);
          }
          this.$_fromChangeSub = this.formTab5.valueChanges.subscribe(() => {
            this.canChangeTab.emit(false);
          });
        }
      }
    );
  }

  getInteretPatrim(fonctions) {
    this.interetPatTable = [];
    fonctions.forEach((pat: any) => {
      this.interetPatTable.push({
        function: this.interetPatInput
          .flat()
          .find((item: any) => item.id_nomenclature == pat.id_function),
        qualification: this.formMetaData["FONCTIONS_QUALIF"].find(
          (item: any) => item.id_nomenclature == pat.id_qualification
        ),
        knowledge: this.formMetaData["FONCTIONS_CONNAISSANCE"].find(
          (item: any) => item.id_nomenclature == pat.id_knowledge
        ),
        justification: pat.justification,
      });
    });
  }

  getValSocEco(fonctions) {
    this.valSocEcoTable = [];
    fonctions.forEach((valSoc: any) => {
      this.valSocEcoTable.push({
        function: this.valSocEcoInput
          .flat()
          .find((item: any) => item.id_nomenclature == valSoc.id_function),
        qualification: this.formMetaData["FONCTIONS_QUALIF"].find(
          (item: any) => item.id_nomenclature == valSoc.id_qualification
        ),
        knowledge: this.formMetaData["FONCTIONS_CONNAISSANCE"].find(
          (item: any) => item.id_nomenclature == valSoc.id_knowledge
        ),
        justification: valSoc.justification,
      });
    });
  }

  getBio(fonctions) {
    this.bioFctTable = [];
    fonctions.forEach((bioFct: any) => {
      this.bioFctTable.push({
        function: this.bioFctInput
          .flat()
          .find((item: any) => item.id_nomenclature == bioFct.id_function),
        qualification: this.formMetaData["FONCTIONS_QUALIF"].find(
          (item: any) => item.id_nomenclature == bioFct.id_qualification
        ),
        knowledge: this.formMetaData["FONCTIONS_CONNAISSANCE"].find(
          (item: any) => item.id_nomenclature == bioFct.id_knowledge
        ),
        justification: bioFct.justification,
      });
    });
  }

  getHydro(fonctions) {
    this.fctHydroTable = [];
    fonctions.forEach((hydroFct: any) => {
      this.fctHydroTable.push({
        function: this.fctHydroInput
          .flat()
          .find((item: any) => item.id_nomenclature == hydroFct.id_function),
        qualification: this.formMetaData["FONCTIONS_QUALIF"].find(
          (item: any) => item.id_nomenclature == hydroFct.id_qualification
        ),
        knowledge: this.formMetaData["FONCTIONS_CONNAISSANCE"].find(
          (item: any) => item.id_nomenclature == hydroFct.id_knowledge
        ),
        justification: hydroFct.justification,
      });
    });
  }

  async getCorineBio(habitats) {
    // Since it is async, need to set a temporary
    //   table. This prevents duplicate pushes on
    //   this.corineBioTable
    const tempCorineTable: any[] = [];
    habitats.forEach(async (corineBio: any) => {
      let selectedCahierHab;
      await this._dataService
        .getHabitatByCorine(corineBio.id_corine_bio)
        .toPromise()
        .then((habitats: any) => {
          this.cahierHabInput = habitats;
          selectedCahierHab = this.cahierHabInput.find(
            (item: any) => item.cd_hab == Number(corineBio.id_cahier_hab)
          );
          tempCorineTable.push({
            corinBio: this.corinBioMetaData.find(
              (item: any) => item.CB_code == corineBio.id_corine_bio
            ),
            preservationState: this.formMetaData["ETAT_CONSERVATION"].find(
              (item: any) =>
                item.id_nomenclature == corineBio.id_preservation_state
            ),
            cahierHab: selectedCahierHab,
            habCover: corineBio.hab_cover,
          });
          this.sortCorineBio();
        });
    });
    this.corineBioTable = tempCorineTable;
  }

  // open the add fonction hydrologique modal
  onAddHydroFct(event: any, modal: any) {
    this.hydroFctForm.reset();
    this.patchModal = false;
    this.addModalBtnLabel = "Ajouter";
    this.modalTitle = "Ajout d'une fonction hydrologique / biogéochimique";
    event.stopPropagation();

    this._modalService.open(
      modal,
      this.fctHydroTable.map((item) => item.function),
      this.fctHydroInput.flat()
    );
  }

  // add a new hydroFct to hydroFcts array
  onPostHydroFct() {
    this.modalFormSubmitted = true;
    if (this.hydroFctForm.valid) {
      let formValues = this.hydroFctForm.value;
      // check if the hydroFct to add is already added
      let itemExist = this.fctHydroTable.some(
        (item: any) =>
          item.function.id_nomenclature == formValues.function.id_nomenclature
      );
      if (!itemExist) {
        this.fctHydroTable.push(formValues);
      }

      this.ngbModal.dismissAll();
      this.hydroFctForm.reset();
      this.canChangeTab.emit(false);
      this.modalFormSubmitted = false;
      this.sortFunction(this.fctHydroTable);
    }
  }

  //delete hydroFct from the hydroFcts array
  onDeleteHydroFct(hydroFct: any) {
    this.fctHydroTable = this.fctHydroTable.filter((item: any) => {
      return item.function.id_nomenclature != hydroFct.function.id_nomenclature;
    });
    this.canChangeTab.emit(false);
  }

  // open the edit hydroFct modal
  onEditHydroFct(modal: any, hydroFct: any) {
    this.patchModal = true;
    this.addModalBtnLabel = "Modifier";
    this.modalTitle = "Modifier la fonction hydrologique / biogéochimique";
    // init inputs object type
    const selectedFunction = this.fctHydroInput
      .flat()
      .find(
        (item: any) => item.id_nomenclature == hydroFct.function.id_nomenclature
      );
    const selectedKnowledge = this.formMetaData["FONCTIONS_CONNAISSANCE"].find(
      (item: any) => item.id_nomenclature == hydroFct.knowledge.id_nomenclature
    );
    const selectedQualif = this.formMetaData["FONCTIONS_QUALIF"].find(
      (item: any) =>
        item.id_nomenclature == hydroFct.qualification.id_nomenclature
    );

    // patch form values
    this.hydroFctForm.patchValue({
      function: selectedFunction,
      qualification: selectedQualif,
      knowledge: selectedKnowledge,
      justification: hydroFct.justification,
    });
    this.tempID = hydroFct.function.id_nomenclature;
    this._modalService.open(
      modal,
      this.fctHydroTable.map((item) => item.function),
      this.fctHydroInput.flat(),
      hydroFct.function
    );
  }

  // edit hydroFct and save into hydroFcts array
  onPatchHydroFct() {
    this.patchModal = false;
    this.modalFormSubmitted = true;
    if (this.hydroFctForm.valid) {
      let formValues = this.hydroFctForm.value;
      this.fctHydroTable = this.fctHydroTable.map((item: any) =>
        item.function.id_nomenclature != this.tempID ? item : formValues
      );
      this.tempID = null;
      this.ngbModal.dismissAll();
      this.hydroFctForm.reset();

      this.canChangeTab.emit(false);
      this.modalFormSubmitted = false;
      this.sortFunction(this.fctHydroTable);
    }
  }

  // open the add fonction biologique modal
  onAddBioFct(event: any, modal: any) {
    this.bioFctForm.reset();
    this.patchModal = false;
    this.addModalBtnLabel = "Ajouter";
    this.modalTitle = "Ajout d'une fonction biologique / écologique";
    event.stopPropagation();
    this._modalService.open(
      modal,
      this.bioFctTable.map((item) => item.function),
      this.bioFctInput.flat()
    );
  }

  // add a new bioFct to bioFcts array
  onPostBioFct() {
    this.modalFormSubmitted = true;
    if (this.bioFctForm.valid) {
      let formValues = this.bioFctForm.value;
      // check if the bioFct to add is already added
      let itemExist = this.bioFctTable.some(
        (item: any) =>
          item.function.id_nomenclature == formValues.function.id_nomenclature
      );
      if (!itemExist) {
        this.bioFctTable.push(formValues);
      }
      this.ngbModal.dismissAll();
      this.bioFctForm.reset();
      this.canChangeTab.emit(false);
      this.modalFormSubmitted = false;
      this.sortFunction(this.bioFctTable);
    }
  }

  //delete bioFct from the bioFcts array
  onDeleteBioFct(bioFct: any) {
    this.bioFctTable = this.bioFctTable.filter((item: any) => {
      return item.function.id_nomenclature != bioFct.function.id_nomenclature;
    });
    this.canChangeTab.emit(false);
  }

  // open the edit bioFct modal
  onEditBioFct(modal: any, bioFct: any) {
    this.patchModal = true;
    this.addModalBtnLabel = "Modifier";
    this.modalTitle = "Modifier la fonction biologique / écologique";
    // init inputs object type
    const selectedFunction = this.bioFctInput
      .flat()
      .find(
        (item: any) => item.id_nomenclature == bioFct.function.id_nomenclature
      );
    const selectedKnowledge = this.formMetaData["FONCTIONS_CONNAISSANCE"].find(
      (item: any) => item.id_nomenclature == bioFct.knowledge.id_nomenclature
    );
    const selectedQualif = this.formMetaData["FONCTIONS_QUALIF"].find(
      (item: any) =>
        item.id_nomenclature == bioFct.qualification.id_nomenclature
    );

    // patch form values
    this.bioFctForm.patchValue({
      function: selectedFunction,
      qualification: selectedQualif,
      knowledge: selectedKnowledge,
      justification: bioFct.justification,
    });
    this.tempID = bioFct.function.id_nomenclature;

    this._modalService.open(
      modal,
      this.bioFctTable.map((item) => item.function),
      this.bioFctInput.flat(),
      bioFct.function
    );
  }
  // edit bioFct and save into bioFcts array
  onPatchBioFct() {
    this.patchModal = false;
    this.modalFormSubmitted = true;
    if (this.bioFctForm.valid) {
      let formValues = this.bioFctForm.value;
      this.bioFctTable = this.bioFctTable.map((item: any) =>
        item.function.id_nomenclature != this.tempID ? item : formValues
      );
      this.tempID = null;
      this.ngbModal.dismissAll();
      this.bioFctForm.reset();

      this.canChangeTab.emit(false);
      this.modalFormSubmitted = false;
      this.sortFunction(this.bioFctTable);
    }
  }

  // open the add fonction intérêt patrimonal modal
  onAddInteretPat(event: any, modal: any) {
    this.interetPatForm.reset();
    this.patchModal = false;
    this.addModalBtnLabel = "Ajouter";
    this.modalTitle = "Ajout d'un intérêt patrimonal";
    event.stopPropagation();
    this._modalService.open(
      modal,
      this.interetPatTable.map((item) => item.function),
      this.interetPatInput.flat()
    );
  }

  // add a new bioFct to bioFcts array
  onPostInteretPat() {
    this.modalFormSubmitted = true;
    if (this.interetPatForm.valid) {
      let formValues = this.interetPatForm.value;
      // check if the interetPat to add is already added
      let itemExist = this.interetPatTable.some(
        (item: any) =>
          item.function.id_nomenclature == formValues.function.id_nomenclature
      );
      if (!itemExist) {
        this.interetPatTable.push(formValues);
      }

      this.ngbModal.dismissAll();
      this.interetPatForm.reset();
      this.canChangeTab.emit(false);
      this.modalFormSubmitted = false;
      this.sortFunction(this.interetPatTable);
    }
  }

  //delete interetPat from the interetPat array
  onDeleteInteretPat(interetPat: any) {
    this.interetPatTable = this.interetPatTable.filter((item: any) => {
      return (
        item.function.id_nomenclature != interetPat.function.id_nomenclature
      );
    });

    this.canChangeTab.emit(false);
  }

  // open the edit interetPat modal
  onEditInteretPat(modal: any, interetPat: any) {
    this.patchModal = true;
    this.addModalBtnLabel = "Modifier";
    this.modalTitle = "Modifier l'intérêt patrimonal";
    // init inputs object type
    const selectedFunction = this.interetPatInput
      .flat()
      .find(
        (item: any) =>
          item.id_nomenclature == interetPat.function.id_nomenclature
      );
    const selectedKnowledge = this.formMetaData["FONCTIONS_CONNAISSANCE"].find(
      (item: any) =>
        item.id_nomenclature == interetPat.knowledge.id_nomenclature
    );
    const selectedQualif = this.formMetaData["FONCTIONS_QUALIF"].find(
      (item: any) =>
        item.id_nomenclature == interetPat.qualification.id_nomenclature
    );

    // patch form values
    this.interetPatForm.patchValue({
      function: selectedFunction,
      qualification: selectedQualif,
      knowledge: selectedKnowledge,
      justification: interetPat.justification,
    });
    this.tempID = interetPat.function.id_nomenclature;

    this._modalService.open(
      modal,
      this.interetPatTable.map((item) => item.function),
      this.interetPatInput.flat(),
      interetPat.function
    );
  }
  // edit interetPat and save into interetPats array
  onPatchInteretPat() {
    this.patchModal = false;
    this.modalFormSubmitted = true;
    if (this.interetPatForm.valid) {
      let formValues = this.interetPatForm.value;
      this.interetPatTable = this.interetPatTable.map((item: any) =>
        item.function.id_nomenclature != this.tempID ? item : formValues
      );
      this.tempID = null;
      this.ngbModal.dismissAll();
      this.interetPatForm.reset();

      this.canChangeTab.emit(false);
      this.modalFormSubmitted = false;
      this.sortFunction(this.interetPatTable);
    }
  }

  onGenerateTaxa() {
    this.taxaLoading = true;
    this._dataService
      .getTaxa(this.currentZh.id)
      .toPromise()
      .then((res: TaxaFile) => {
        if (res.file_names.length == 0) {
          const msg =
            "Aucun fichier n'a été généré car aucune espèce n'a été trouvée dans la zone humide";
          this._toastr.error(msg, "", {
            disableTimeOut: true, // to be sure the user sees the toast
            closeButton: true,
          });
        } else {
          const files = res.file_names.map((file) =>
            file.replace(/^.*[\\\/]/, "")
          );
          const msg = `Les fichiers suivants ont été générés </br> ${files.join(
            "</br>"
          )}`;
          this._toastr.success(msg, "", {
            disableTimeOut: true, // to be sure the user sees the toast
            closeButton: true,
            enableHtml: true,
          });
        }
      })
      .catch((error) => {
        let frontError: string = "";
        if (error.status === 404) {
          frontError = "Erreur 404 : URL non trouvé";
        } else {
          frontError = this._error.getFrontError(
            error ? error.error.message : null
          );
        }
        this._toastr.error(frontError, "", {
          positionClass: "toast-top-right",
        });
      })
      .finally(() => {
        this.taxaLoading = false;
        this._filesService
          .loadFiles(this.currentZh.properties.id_zh)
          .toPromise()
          .then(() => {});
      });
  }

  onAddValSocEco(event: any, modal: any) {
    this.valSocEcoForm.reset();
    this.patchModal = false;
    this.addModalBtnLabel = "Ajouter";
    this.modalTitle = "Ajout d'une valeur socio-économique";
    event.stopPropagation();
    this._modalService.open(
      modal,
      this.valSocEcoTable.map((item) => item.function),
      this.valSocEcoInput.flat()
    );
  }

  // add a new valSocEco to valSocEco array
  onPostValSocEco() {
    this.modalFormSubmitted = true;
    if (this.valSocEcoForm.valid) {
      let formValues = this.valSocEcoForm.value;
      // check if the valSocEco to add is already added
      let itemExist = this.valSocEcoTable.some(
        (item: any) =>
          item.function.id_nomenclature == formValues.function.id_nomenclature
      );
      if (!itemExist) {
        this.valSocEcoTable.push(formValues);
      }

      this.ngbModal.dismissAll();
      this.valSocEcoForm.reset();
      this.canChangeTab.emit(false);
      this.modalFormSubmitted = false;
      this.sortFunction(this.valSocEcoTable);
    }
  }

  //delete valSocEco from the valSocEco array
  onDeleteValSocEco(valSocEco: any) {
    this.valSocEcoTable = this.valSocEcoTable.filter((item: any) => {
      return (
        item.function.id_nomenclature != valSocEco.function.id_nomenclature
      );
    });
    this.canChangeTab.emit(false);
  }

  // open the edit valSocEco modal
  onEditValSocEco(modal: any, valSocEco: any) {
    this.patchModal = true;
    this.addModalBtnLabel = "Modifier";
    this.modalTitle = "Modifier une valeur socio-économique";
    // init inputs object type
    const selectedFunction = this.valSocEcoInput
      .flat()
      .find(
        (item: any) =>
          item.id_nomenclature == valSocEco.function.id_nomenclature
      );
    const selectedKnowledge = this.formMetaData["FONCTIONS_CONNAISSANCE"].find(
      (item: any) => item.id_nomenclature == valSocEco.knowledge.id_nomenclature
    );
    const selectedQualif = this.formMetaData["FONCTIONS_QUALIF"].find(
      (item: any) =>
        item.id_nomenclature == valSocEco.qualification.id_nomenclature
    );

    // patch form values
    this.valSocEcoForm.patchValue({
      function: selectedFunction,
      qualification: selectedQualif,
      knowledge: selectedKnowledge,
      justification: valSocEco.justification,
    });
    this.tempID = valSocEco.function.id_nomenclature;
    // manger disabled valSocEco input items

    this._modalService.open(
      modal,
      this.valSocEcoTable.map((item) => item.function),
      this.valSocEcoInput.flat(),
      valSocEco.function
    );
  }
  // edit valSocEco and save into valSocEcos array
  onPatchValSocEco() {
    this.patchModal = false;
    this.modalFormSubmitted = true;
    if (this.valSocEcoForm.valid) {
      let formValues = this.valSocEcoForm.value;
      this.valSocEcoTable = this.valSocEcoTable.map((item: any) =>
        item.function.id_nomenclature != this.tempID ? item : formValues
      );
      this.tempID = null;
      this.ngbModal.dismissAll();
      this.valSocEcoForm.reset();

      this.canChangeTab.emit(false);
      this.modalFormSubmitted = false;
      this.sortFunction(this.valSocEcoTable);
    }
  }

  // open the add CorineBio modal
  onAddCorineBio(event: any, modal: any) {
    this.corineBioForm.reset();
    this.patchModal = false;
    this.addModalBtnLabel = "Ajouter";
    this.modalTitle = "Ajout d'un habitat humide patrimonial";
    event.stopPropagation();
    this.ngbModal.open(modal, {
      centered: true,
      size: "lg",
      windowClass: "bib-modal",
    });
  }

  // add a new CorineBio to CorineBio array
  onPostCorineBio() {
    this.modalFormSubmitted = true;
    if (this.corineBioForm.valid) {
      this.corineBioTable.push(this.corineBioForm.value);
      this.sortCorineBio();
      this.ngbModal.dismissAll();
      this.corineBioForm.reset();
      this.corineBioForm.get("cahierHab").disable();
      this.canChangeTab.emit(false);
      this.modalFormSubmitted = false;
    }
  }

  //delete corineBio from the corineBio array
  onDeleteCorineBio(corineBio: any) {
    this.corineBioTable = this.corineBioTable.filter(
      (item: any) => item != corineBio
    );
    this.canChangeTab.emit(false);
  }

  // open the edit corineBio modal
  onEditCorineBio(modal: any, corineBio: any) {
    this.patchModal = true;
    this.addModalBtnLabel = "Modifier";
    this.modalTitle = "Modifier un habitat humide patrimonial";
    let selectedCahierHab;
    // init inputs object type
    const selectedCorin = this.corinBioMetaData.find(
      (item: any) => item.CB_code == corineBio.corinBio.CB_code
    );
    const selectedState = this.formMetaData["ETAT_CONSERVATION"].find(
      (item: any) =>
        item.id_nomenclature == corineBio.preservationState.id_nomenclature
    );
    this._dataService
      .getHabitatByCorine(corineBio.corinBio.CB_code)
      .subscribe((habitats: any) => {
        this.cahierHabInput = habitats;
        selectedCahierHab = this.cahierHabInput.find(
          (item: any) => item.cd_hab == corineBio.cahierHab.cd_hab
        );
        this.corineBioForm.get("cahierHab").enable();
        // patch form values
        this.corineBioForm.patchValue({
          corinBio: selectedCorin,
          preservationState: selectedState,
          cahierHab: selectedCahierHab,
          habCover: corineBio.habCover,
        });
        this.tempID = corineBio.corinBio.CB_code;
        this.ngbModal.open(modal, {
          centered: true,
          size: "lg",
          windowClass: "bib-modal",
        });
      });
  }
  // edit corineBio and save into corineBios array
  onPatchCorineBio() {
    this.patchModal = false;
    this.modalFormSubmitted = true;
    if (this.corineBioForm.valid) {
      let formValues = this.corineBioForm.value;
      this.corineBioTable = this.corineBioTable.map((item: any) =>
        item.corinBio.CB_code != this.tempID ? item : formValues
      );
      this.sortCorineBio();
      this.tempID = null;
      this.ngbModal.dismissAll();
      this.corineBioForm.reset();
      this.canChangeTab.emit(false);
      this.modalFormSubmitted = false;
    }
  }

  // autocomplet corine biotope
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

  onSelectedCorin(corineBio: any) {
    this._dataService
      .getHabitatByCorine(corineBio.CB_code)
      .subscribe((habitats: any) => {
        this.cahierHabInput = habitats.map((item) => {
          item.disabled = this.corineBioTable
            .map((cor) => cor.cahierHab)
            .some((e) => e.cd_hab === item.cd_hab);
          return item;
        });
        this.corineBioForm.get("cahierHab").enable();
      });
  }

  onFormSubmit() {
    if (this.formTab5.valid) {
      this.submitted = true;
      this.$_fromChangeSub.unsubscribe();
      let fonctions_hydro = [];
      let fonctions_bio = [];
      let interet_patrim = [];
      let val_soc_eco = [];
      let hab_heritages = [];

      if (this.fctHydroTable && this.fctHydroTable.length > 0) {
        this.fctHydroTable.forEach((item: any) => {
          fonctions_hydro.push({
            id_function: item.function.id_nomenclature,
            justification: item.justification,
            id_qualification: item.qualification.id_nomenclature,
            id_knowledge: item.knowledge.id_nomenclature,
          });
        });
      }

      if (this.bioFctTable && this.bioFctTable.length > 0) {
        this.bioFctTable.forEach((item: any) => {
          fonctions_bio.push({
            id_function: item.function.id_nomenclature,
            justification: item.justification,
            id_qualification: item.qualification.id_nomenclature,
            id_knowledge: item.knowledge.id_nomenclature,
          });
        });
      }

      if (this.interetPatTable && this.interetPatTable.length > 0) {
        this.interetPatTable.forEach((item: any) => {
          interet_patrim.push({
            id_function: item.function.id_nomenclature,
            justification: item.justification,
            id_qualification: item.qualification.id_nomenclature,
            id_knowledge: item.knowledge.id_nomenclature,
          });
        });
      }
      if (this.valSocEcoTable && this.valSocEcoTable.length > 0) {
        this.valSocEcoTable.forEach((item: any) => {
          val_soc_eco.push({
            id_function: item.function.id_nomenclature,
            justification: item.justification,
            id_qualification: item.qualification.id_nomenclature,
            id_knowledge: item.knowledge.id_nomenclature,
          });
        });
      }

      if (this.corineBioTable && this.corineBioTable.length > 0) {
        this.corineBioTable.forEach((item: any) => {
          hab_heritages.push({
            id_corine_bio: item.corinBio.CB_code,
            id_cahier_hab: item.cahierHab.cd_hab,
            id_preservation_state: item.preservationState.id_nomenclature,
            hab_cover: item.habCover,
          });
        });
      }

      let formToPost = {
        id_zh: Number(this.currentZh.properties.id_zh),
        is_carto_hab: this.formTab5.value.is_carto_hab,
        nb_hab: this.formTab5.value.nb_hab,
        total_hab_cover: this.formTab5.value.total_hab_cover,
        nb_flora_sp: this.formTab5.value.nb_flora_sp,
        nb_vertebrate_sp: this.formTab5.value.nb_vertebrate_sp,
        nb_invertebrate_sp: this.formTab5.value.nb_invertebrate_sp,
        fonctions_hydro: fonctions_hydro,
        fonctions_bio: fonctions_bio,
        interet_patrim: interet_patrim,
        val_soc_eco: val_soc_eco,
        hab_heritages: hab_heritages,
      };

      this.posted = true;
      this._dataService.postDataForm(formToPost, 5).subscribe(
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
              this.nextTab.emit(6);
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

  sortFunction(_function) {
    _function.sort((a, b) =>
      a.function.mnemonique.slice(0, 2) > b.function.mnemonique.slice(0, 2)
        ? 1
        : b.function.mnemonique.slice(0, 2) > a.function.mnemonique.slice(0, 2)
        ? -1
        : 0
    );
  }

  sortCorineBio() {
    this.corineBioTable.sort((a, b) =>
      a.corinBio.CB_label > b.corinBio.CB_label
        ? 1
        : b.corinBio.CB_label > a.corinBio.CB_label
        ? -1
        : 0
    );
  }
}
