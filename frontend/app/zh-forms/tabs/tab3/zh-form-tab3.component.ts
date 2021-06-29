import { Component, OnInit, Input } from "@angular/core";
import { FormGroup, FormBuilder, Validators } from "@angular/forms";
import { ZhDataService } from "../../../services/zh-data.service";
import { NgbModal } from "@ng-bootstrap/ng-bootstrap";
import { Subscription, Observable } from "rxjs";
import { debounceTime, distinctUntilChanged, map } from "rxjs/operators";

@Component({
  selector: "zh-form-tab3",
  templateUrl: "./zh-form-tab3.component.html",
  styleUrls: ["./zh-form-tab3.component.scss"],
})
export class ZhFormTab3Component implements OnInit {
  @Input() formMetaData;
  public form: FormGroup;
  sdage: any;
  sage: any;
  allSage: any;
  $_currentZhSub: Subscription;
  private _currentZh: any;
  corinBioMetaData: any;
  public corinTableCol = [
    { name: "CB_code", label: "Code corine Biotope" },
    { name: "CB_label", label: "Libellé corine biotope" },
    { name: "CB_humidity", label: "Humidité" },
  ];
  listCorinBio = [];
  solOccupation: any;
  dropdownSettings: any;
  activityForm: FormGroup;
  modalButtonLabel: string;
  patchActivity: boolean;
  modalTitle: string;

  itemList = [];
  selectedItems = [];
  settings = {};

  constructor(
    private fb: FormBuilder,
    private _dataService: ZhDataService,
    public ngbModal: NgbModal
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

    this.itemList = [
      { id: 1, itemName: "India", category: "asia" },
      { id: 2, itemName: "Singapore", category: "asia pacific" },
      { id: 3, itemName: "Germany", category: "Europe" },
      { id: 4, itemName: "France", category: "Europe" },
      { id: 5, itemName: "South Korea", category: "asia" },
      { id: 6, itemName: "Sweden", category: "Europe" },
    ];

    this.selectedItems = [
      { id: 1, itemName: "India" },
      { id: 2, itemName: "Singapore" },
      { id: 4, itemName: "Canada" },
    ];

    this.settings = {
      singleSelection: false,
      text: "Select Fields",
      searchPlaceholderText: "Search Fields",
      enableSearchFilter: true,
      badgeShowLimit: 5,
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
    this.sdage = this.formMetaData["SDAGE"];
    this.allSage = this.formMetaData["SDAGE-SAGE"];
    this.corinBioMetaData = this.formMetaData["CORINE_BIO"];
    this.solOccupation = this.formMetaData["OCCUPATION_SOLS"];
  }

  onFormValueChanges(): void {
    this.form.get("sdage").valueChanges.subscribe((val: number) => {
      this.form.get("sage").reset();
      this.allSage.forEach((item) => {
        if (val in item) {
          this.sage = Object.values(item)[0];
        }
      });
    });
  }

  createForm(): void {
    this.form = this.fb.group({
      sdage: [null, Validators.required],
      sage: null,
      corinBio: null,
    });
    this.onFormValueChanges();
  }

  ngOnDestroy() {
    this.$_currentZhSub.unsubscribe();
  }

  public model: any;

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
    let itemExist = this.listCorinBio.some(
      (item) => item.CB_code == this.form.value.corinBio.CB_code
    );
    if (!itemExist && this.form.value.corinBio.CB_code) {
      this.listCorinBio.push(this.form.value.corinBio);
    }
    this.form.get("corinBio").reset();
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
      humainActivity: [null, Validators.required],
      localisation: null,
      pub_year: null,
      editor: null,
      editor_location: null,
    });
    event.stopPropagation();
    this.ngbModal.open(modal, {
      centered: true,
      size: "lg",
      windowClass: "bib-modal",
    });
  }
}
