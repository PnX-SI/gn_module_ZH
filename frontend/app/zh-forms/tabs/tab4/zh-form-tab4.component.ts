import { Component, EventEmitter, OnInit, Input, Output } from "@angular/core";
import { FormGroup, FormBuilder, Validators } from "@angular/forms";
import { NgbModal } from "@ng-bootstrap/ng-bootstrap";
import { ToastrService } from "ngx-toastr";
import { Subscription } from "rxjs";
import { ZhDataService } from "../../../services/zh-data.service";
import { TabsService } from "../../../services/tabs.service";

@Component({
  selector: "zh-form-tab4",
  templateUrl: "./zh-form-tab4.component.html",
  styleUrls: ["./zh-form-tab4.component.scss"],
})
export class ZhFormTab4Component implements OnInit {
  @Input() public formMetaData: any;
  @Output() public canChangeTab = new EventEmitter<boolean>();
  @Output() nextTab = new EventEmitter<number>();
  public formTab4: FormGroup;
  public patchInflow: boolean;
  public inflowModalTitle: string;
  public inflowModalBtnLabel: string;
  public inflowForm: FormGroup;
  public inflowFormSubmitted: boolean;
  public inflowInput: any[];
  public inflowsTable: any = [];
  private $_inflowInputSub: Subscription;

  public patchOutflow: boolean;
  public outflowModalTitle: string;
  public outflowModalBtnLabel: string;
  public outflowForm: FormGroup;
  public outflowFormSubmitted: boolean;
  public outflowInput: any[];
  public outflowsTable: any = [];
  private $_outflowInputSub: Subscription;
  posted: boolean;
  public submitted: boolean;
  private $_currentZhSub: Subscription;
  private $_fromChangeSub: Subscription;
  public currentZh: any;

  public inflowTableCol = [
    { name: "inflow", label: "Entrée d'eau" },
    { name: "permanance", label: "Permanence" },
    { name: "topo", label: "Toponymie et compléments d'information" },
  ];

  public outflowTableCol = [
    { name: "outflow", label: "Sorite d'eau" },
    { name: "permanance", label: "Permanence" },
    { name: "topo", label: "Toponymie et compléments d'information" },
  ];

  constructor(
    private fb: FormBuilder,
    public ngbModal: NgbModal,
    private _toastr: ToastrService,
    private _dataService: ZhDataService,
    private _tabService: TabsService
  ) {}

  ngOnInit() {
    this.getMetaData();

    this.initForms();
    this.getCurrentZh();
    this._tabService.getTabChange().subscribe((tabPosition: number) => {
      this.$_fromChangeSub.unsubscribe();
      this.$_currentZhSub.unsubscribe();
      if (tabPosition == 4) {
        this.getCurrentZh();
      }
    });
  }

  // initialize forms
  initForms(): void {
    this.inflowForm = this.fb.group({
      inflow: [null, Validators.required],
      permanance: [null, Validators.required],
      topo: null,
    });
    this.outflowForm = this.fb.group({
      outflow: [null, Validators.required],
      permanance: [null, Validators.required],
      topo: null,
    });
    this.formTab4 = this.fb.group({
      frequency: null,
      spread: null,
      connexion: null,
      diag_hydro: null,
      diag_bio: null,
      remark_diag: null,
    });
  }

  // get metaData forms
  getMetaData() {
    this.inflowInput = [...this.formMetaData["ENTREE_EAU"]];
    this.outflowInput = [...this.formMetaData["SORTIE_EAU"]];
    // add disabled property to inflowInput options list
    this.inflowInput.map((item: any) => {
      item.disabled = false;
    });
    this.outflowInput.map((item: any) => {
      item.disabled = false;
    });
  }

  // get current zone humides && patch forms values
  getCurrentZh() {
    this.$_currentZhSub = this._dataService.currentZh.subscribe((zh: any) => {
      if (zh) {
        this.currentZh = zh;
        this.inflowsTable = [];
        this.outflowsTable = [];
        //patch forms values
        if (
          this.currentZh.properties.flows &&
          this.currentZh.properties.flows.length > 0
        ) {
          this.currentZh.properties.flows.forEach((element: any) => {
            for (const key in element) {
              if (key == "inflows") {
                if (element[key].length > 0) {
                  element[key].forEach((inflow) => {
                    this.inflowsTable.push({
                      inflow: this.formMetaData["ENTREE_EAU"].find((item) => {
                        return item.id_nomenclature == inflow.id_inflow;
                      }),
                      permanance: this.formMetaData["PERMANENCE_ENTREE"].find(
                        (item) => {
                          return item.id_nomenclature == inflow.id_permanance;
                        }
                      ),
                      topo: inflow.topo,
                    });
                    this.inflowInput.map((item: any) => {
                      if (item.id_nomenclature == inflow.id_inflow) {
                        item.disabled = true;
                      }
                    });
                  });
                }
              }
              if (key == "outflows") {
                if (element[key].length > 0) {
                  element[key].forEach((outflow) => {
                    this.outflowsTable.push({
                      outflow: this.formMetaData["SORTIE_EAU"].find((item) => {
                        return item.id_nomenclature == outflow.id_outflow;
                      }),
                      permanance: this.formMetaData["PERMANENCE_SORTIE"].find(
                        (item) => {
                          return item.id_nomenclature == outflow.id_permanance;
                        }
                      ),
                      topo: outflow.topo,
                    });
                    this.outflowInput.map((item: any) => {
                      if (item.id_nomenclature == outflow.id_outflow) {
                        item.disabled = true;
                      }
                    });
                  });
                }
              }
            }
          });
        }
        this.formTab4.patchValue({
          spread: this.formMetaData["SUBMERSION_ETENDUE"].find((item) => {
            return item.id_nomenclature == this.currentZh.properties.id_spread;
          }),
          frequency: this.formMetaData["SUBMERSION_FREQ"].find((item) => {
            return (
              item.id_nomenclature == this.currentZh.properties.id_frequency
            );
          }),
          connexion: this.currentZh.properties.id_connexion,
          diag_hydro: this.formMetaData["FONCTIONNALITE_HYDRO"].find((item) => {
            return (
              item.id_nomenclature == this.currentZh.properties.id_diag_hydro
            );
          }),
          diag_bio: this.formMetaData["FONCTIONNALITE_BIO"].find((item) => {
            return (
              item.id_nomenclature == this.currentZh.properties.id_diag_bio
            );
          }),
          remark_diag: this.currentZh.properties.remark_diag,
        });
      }
      this.$_fromChangeSub = this.formTab4.valueChanges.subscribe(() => {
        this.canChangeTab.emit(false);
      });
    });
  }

  // open the add inFlow modal
  onAddInflow(event: any, modal: any) {
    this.patchInflow = false;
    this.inflowModalBtnLabel = "Ajouter";
    this.inflowModalTitle = "Ajout d'une entrée d'eau";
    event.stopPropagation();
    this.ngbModal.open(modal, {
      centered: true,
      size: "lg",
      windowClass: "bib-modal",
    });
  }

  // add a new inflow to inflows array
  onPostInflow() {
    this.inflowFormSubmitted = true;
    if (this.inflowForm.valid) {
      let inflowValues = this.inflowForm.value;
      // check if the inflow to add is already added
      let itemExist = this.inflowsTable.some(
        (item: any) =>
          item.inflow.id_nomenclature == inflowValues.inflow.id_nomenclature
      );
      if (!itemExist) {
        this.inflowsTable.push(inflowValues);
      }
      // disable the added inflow on the select input list
      this.inflowInput.map((item: any) => {
        if (item.id_nomenclature == inflowValues.inflow.id_nomenclature) {
          item.disabled = true;
        }
      });

      this.ngbModal.dismissAll();
      this.inflowForm.reset();
      this.canChangeTab.emit(false);
      this.inflowFormSubmitted = false;
    }
  }

  //delete inflow from the inflows array
  onDeleteInflow(inflow: any) {
    this.inflowsTable = this.inflowsTable.filter((item: any) => {
      return item.inflow.id_nomenclature != inflow.inflow.id_nomenclature;
    });
    this.inflowInput.map((item: any) => {
      if (item.id_nomenclature == inflow.inflow.id_nomenclature) {
        item.disabled = false;
      }
    });
    this.canChangeTab.emit(false);
  }

  // open the edit inFlow modal
  onEditInflow(modal: any, inflow: any) {
    this.patchInflow = true;
    this.inflowModalBtnLabel = "Modifier";
    this.inflowModalTitle = "Modifier l'entrée d'eau";
    // init inputs object type
    const selectedInflow = this.inflowInput.find(
      (item: any) => item.id_nomenclature == inflow.inflow.id_nomenclature
    );
    const selectePermanance = this.formMetaData["PERMANENCE_ENTREE"].find(
      (item: any) => item.id_nomenclature == inflow.permanance.id_nomenclature
    );
    // patch form values
    this.inflowForm.patchValue({
      inflow: selectedInflow,
      permanance: selectePermanance,
      topo: inflow.topo,
    });
    // manger disabled inflow input items
    this.$_inflowInputSub = this.inflowForm
      .get("inflow")
      .valueChanges.subscribe(() => {
        this.inflowInput.map((item: any) => {
          if (item.id_nomenclature == inflow.inflow.id_nomenclature) {
            item.disabled = false;
          }
        });
      });

    this.ngbModal.open(modal, {
      centered: true,
      size: "lg",
      windowClass: "bib-modal",
    });
  }

  // edit inflow and save into inflows array
  onPatchInflow() {
    this.patchInflow = false;
    this.inflowFormSubmitted = true;
    if (this.inflowForm.valid) {
      let inflowValues = this.inflowForm.value;
      this.inflowsTable = this.inflowsTable.map((item: any) =>
        item.inflow.id_nomenclature != inflowValues.inflow.id_nomenclature
          ? item
          : inflowValues
      );
      this.inflowInput.map((item: any) => {
        if (item.id_nomenclature == inflowValues.inflow.id_nomenclature) {
          item.disabled = true;
        }
      });
      this.ngbModal.dismissAll();
      this.inflowForm.reset();

      this.$_inflowInputSub.unsubscribe();
      this.canChangeTab.emit(false);
      this.inflowFormSubmitted = false;
    }
  }

  // open the add outFlow modal
  onAddOutflow(event: any, modal: any) {
    this.patchOutflow = false;
    this.outflowModalBtnLabel = "Ajouter";
    this.outflowModalTitle = "Ajout d'une sortie d'eau";
    event.stopPropagation();
    this.ngbModal.open(modal, {
      centered: true,
      size: "lg",
      windowClass: "bib-modal",
    });
  }

  // add a new outflow to outflows array
  onPostOutflow() {
    this.outflowFormSubmitted = true;
    if (this.outflowForm.valid) {
      let outflowValues = this.outflowForm.value;
      // check if the outflow to add is already added
      let itemExist = this.outflowsTable.some(
        (item: any) =>
          item.outflow.id_nomenclature == outflowValues.outflow.id_nomenclature
      );
      if (!itemExist) {
        this.outflowsTable.push(outflowValues);
      }
      // disable the added outflow on the select input list
      this.outflowInput.map((item: any) => {
        if (item.id_nomenclature == outflowValues.outflow.id_nomenclature) {
          item.disabled = true;
        }
      });

      this.ngbModal.dismissAll();
      this.outflowForm.reset();
      this.canChangeTab.emit(false);
      this.outflowFormSubmitted = false;
    }
  }

  //delete outflow from the outflows array
  onDeleteOutflow(outflow: any) {
    this.outflowsTable = this.outflowsTable.filter((item: any) => {
      return item.outflow.id_nomenclature != outflow.outflow.id_nomenclature;
    });
    this.outflowInput.map((item: any) => {
      if (item.id_nomenclature == outflow.outflow.id_nomenclature) {
        item.disabled = false;
      }
    });
    this.canChangeTab.emit(false);
  }

  // open the edit outFlow modal
  onEditOutflow(modal: any, outflow: any) {
    this.patchOutflow = true;
    this.outflowModalBtnLabel = "Modifier";
    this.outflowModalTitle = "Modifier la sortie d'eau";
    // init inputs object type
    const selectedOutflow = this.outflowInput.find(
      (item: any) => item.id_nomenclature == outflow.outflow.id_nomenclature
    );
    const selectePermanance = this.formMetaData["PERMANENCE_SORTIE"].find(
      (item: any) => item.id_nomenclature == outflow.permanance.id_nomenclature
    );
    // patch form values
    this.outflowForm.patchValue({
      outflow: selectedOutflow,
      permanance: selectePermanance,
      topo: outflow.topo,
    });
    // manger disabled outflow input items
    this.$_outflowInputSub = this.outflowForm
      .get("outflow")
      .valueChanges.subscribe(() => {
        this.outflowInput.map((item: any) => {
          if (item.id_nomenclature == outflow.outflow.id_nomenclature) {
            item.disabled = false;
          }
        });
      });

    this.ngbModal.open(modal, {
      centered: true,
      size: "lg",
      windowClass: "bib-modal",
    });
  }
  // edit outflow and save into outflows array
  onPatchOutflow() {
    this.patchOutflow = false;
    this.outflowFormSubmitted = true;
    if (this.outflowForm.valid) {
      let outflowValues = this.outflowForm.value;
      this.outflowsTable = this.outflowsTable.map((item: any) =>
        item.outflow.id_nomenclature != outflowValues.outflow.id_nomenclature
          ? item
          : outflowValues
      );
      this.outflowInput.map((item: any) => {
        if (item.id_nomenclature == outflowValues.outflow.id_nomenclature) {
          item.disabled = true;
        }
      });
      this.ngbModal.dismissAll();
      this.outflowForm.reset();

      this.$_outflowInputSub.unsubscribe();
      this.canChangeTab.emit(false);
      this.outflowFormSubmitted = false;
    }
  }

  onFormSubmit() {
    if (this.formTab4.valid) {
      this.submitted = true;
      this.$_fromChangeSub.unsubscribe();
      let outflows = [];
      let inflows = [];
      if (this.outflowsTable && this.outflowsTable.length > 0) {
        this.outflowsTable.forEach((item: any) => {
          outflows.push({
            id_outflow: item.outflow.id_nomenclature,
            id_permanance: item.permanance.id_nomenclature,
            topo: item.topo,
          });
        });
      }
      if (this.inflowsTable && this.inflowsTable.length > 0) {
        this.inflowsTable.forEach((item: any) => {
          inflows.push({
            id_inflow: item.inflow.id_nomenclature,
            id_permanance: item.permanance.id_nomenclature,
            topo: item.topo,
          });
        });
      }

      let formToPost = {
        id_zh: Number(this.currentZh.properties.id_zh),
        id_frequency: this.formTab4.value.frequency
          ? this.formTab4.value.frequency.id_nomenclature
          : null,
        id_spread: this.formTab4.value.spread
          ? this.formTab4.value.spread.id_nomenclature
          : null,
        id_connexion: this.formTab4.value.connexion
          ? Number(this.formTab4.value.connexion)
          : null,
        id_diag_hydro: this.formTab4.value.diag_hydro
          ? this.formTab4.value.diag_hydro.id_nomenclature
          : null,
        id_diag_bio: this.formTab4.value.diag_bio
          ? this.formTab4.value.diag_bio.id_nomenclature
          : null,
        remark_diag: this.formTab4.value.remark_diag,
        outflows: outflows,
        inflows: inflows,
      };
      this.posted = true;
      this._dataService.postDataForm(formToPost, 4).subscribe(
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
              this.nextTab.emit(5);
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

  ngOnDestroy() {}
}
