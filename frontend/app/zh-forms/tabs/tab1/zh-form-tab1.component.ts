import { Component, EventEmitter, Input, OnInit, Output } from "@angular/core";
import { FormGroup, FormBuilder, Validators } from "@angular/forms";
import { Subscription, of, Observable } from "rxjs";
import {
  debounceTime,
  distinctUntilChanged,
  switchMap,
  tap,
  catchError,
} from "rxjs/operators";
import { ToastrService } from "ngx-toastr";
import { NgbModal } from "@ng-bootstrap/ng-bootstrap";
import { ZhDataService } from "../../../services/zh-data.service";
import { AppConfig } from "@geonature_config/app.config";
import { TabsService } from "../../../services/tabs.service";

@Component({
  selector: "zh-form-tab1",
  templateUrl: "./zh-form-tab1.component.html",
  styleUrls: ["./zh-form-tab1.component.scss"],
})
export class ZhFormTab1Component implements OnInit {
  @Input() formMetaData;
  @Output() canChangeTab = new EventEmitter<boolean>();
  public generalInfoForm: FormGroup;
  public bibForm: FormGroup;
  public siteSpaceList: any[];
  public hasSiteSpace = false;
  public appConfig = AppConfig;
  public cols = ["title", "authors", "pub_year"];
  private _currentZh: any;
  public $_currentZhSub: Subscription;
  public $_fromChangeSub: Subscription;
  public listBib: any[] = [];
  public submitted: boolean;
  public posted: boolean = false;
  public postedBib: boolean = false;
  public modalBibButtonLabel: string;
  public modalBibTitle: string;
  public patchBib: boolean = false;
  public autocompleteBib: string;

  constructor(
    private fb: FormBuilder,
    private _dataService: ZhDataService,
    private _toastr: ToastrService,
    private _tabService: TabsService,
    public ngbModal: NgbModal
  ) {}

  ngOnInit() {
    this.getMetaData();
    this.createForm();
    this.initTab();
    this._tabService.getTabChange().subscribe((tabPosition: number) => {
      this.$_fromChangeSub.unsubscribe();
      if (tabPosition == 1) {
        this.initTab();
      }
    });
  }

  initTab() {
    this.$_currentZhSub = this._dataService.currentZh.subscribe((zh: any) => {
      if (zh) {
        this._currentZh = zh;
        this.listBib = [...this._currentZh.properties.id_references];
        this.generalInfoForm.patchValue({
          main_name: this._currentZh.properties.main_name,
          secondary_name: this._currentZh.properties.secondary_name,
          is_id_site_space: this._currentZh.properties.is_id_site_space,
          id_site_space: this._currentZh.properties.id_site_space,
          id_zh: this._currentZh.properties.id_zh,
        });
        this.$_fromChangeSub = this.generalInfoForm.valueChanges.subscribe(
          () => {
            this.canChangeTab.emit(false);
          }
        );
      }
    });
  }

  createForm(): void {
    this.generalInfoForm = this.fb.group({
      main_name: [null, Validators.required],
      secondary_name: null,
      id_zh: [{ value: null, disabled: true }, Validators.required],
      id_site_space: null,
      is_id_site_space: null,
    });
    this.onFormValueChanges();
  }

  onFormValueChanges(): void {
    this.generalInfoForm
      .get("is_id_site_space")
      .valueChanges.subscribe((val: Boolean) => {
        if (val == true) {
          this.generalInfoForm.get("id_site_space").enable();
          this.hasSiteSpace = true;
        } else if (val == false) {
          this.hasSiteSpace = false;
          this.generalInfoForm.get("id_site_space").reset();
        }
      });
  }

  getMetaData() {
    this.siteSpaceList = this.formMetaData.BIB_SITE_SPACE;
  }

  onSelectBib(seletedBib) {
    seletedBib.preventDefault();
    const bib = seletedBib.item;
    if (bib) {
      let itemExist = this.listBib.some(
        (item) => item.id_reference == bib.id_reference
      );
      if (!itemExist) {
        this.listBib.push(bib);
        this.canChangeTab.emit(false);
      }
    }
    this.autocompleteBib = null;
  }

  onDeleteBib(id_reference: number) {
    this.listBib = this.listBib.filter((item) => {
      return item.id_reference != id_reference;
    });
    this.canChangeTab.emit(false);
  }

  onFormSubmit(formValues: any) {
    this.submitted = true;
    let formToPost = {
      main_name: formValues.main_name,
      secondary_name: formValues.secondary_name,
      id_zh: Number(this._currentZh.properties.id_zh),
      id_site_space: formValues.id_site_space,
      is_id_site_space: formValues.is_id_site_space,
      id_references: [],
    };

    if (this.generalInfoForm.valid) {
      if (formValues.main_name != this._currentZh.properties.main_name) {
        formValues.main_name = formValues.main_name;
      }
      this.listBib.forEach((bib) => {
        formToPost.id_references.push(bib.id_reference);
      });
      this.posted = true;
      this._dataService.postDataForm(formToPost, 1).subscribe(
        () => {
          this.posted = false;
          this.canChangeTab.emit(true);
          this._toastr.success("Vos données sont bien enregistrées", "", {
            positionClass: "toast-top-right",
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

  onCreateBib(event, modal) {
    this.patchBib = false;
    this.modalBibButtonLabel = "Créer";
    this.modalBibTitle = "Ajout d'une référence bibliographique";
    this.bibForm = this.fb.group({
      title: [null, Validators.required],
      authors: null,
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

  onAddBib() {
    if (this.bibForm.valid) {
      this.postedBib = true;
      this._dataService.postBib(this.bibForm.value).subscribe(
        (bib) => {
          this.bibForm.reset();
          this.postedBib = false;
          let itemExist = this.listBib.some(
            (item) => item.id_reference == bib.id_reference
          );
          if (!itemExist) {
            this.listBib.push(bib);
            this.canChangeTab.emit(false);
          }
          this.ngbModal.dismissAll();
        },
        (error) => {
          this.postedBib = false;
          this._toastr.error(error.error, "", {
            positionClass: "toast-top-right",
          });
        }
      );
    }
  }

  onEditBib(modal: any, bib: any) {
    this.patchBib = true;
    this.modalBibButtonLabel = "Modifier";
    this.modalBibTitle = "Modifier la référence bibliographique";
    this.bibForm = this.fb.group({
      id_reference: [bib.id_reference, Validators.required],
      title: [bib.title, Validators.required],
      authors: bib.authors,
      pub_year: bib.pub_year,
      editor: bib.editor,
      editor_location: bib.editor_location,
    });
    this.ngbModal.open(modal, {
      centered: true,
      size: "lg",
      windowClass: "bib-modal",
    });
  }

  onPatchBib() {
    if (this.bibForm.valid) {
      this._dataService.patchBib(this.bibForm.value).subscribe(
        (bib) => {
          this.bibForm.reset();
          this.postedBib = false;
          const index = this.listBib.findIndex(
            (item) => item.id_reference == bib.id_reference
          );
          if (index > -1) this.listBib.splice(index, 1, bib);
          this.canChangeTab.emit(false);
          this.ngbModal.dismissAll();
        },
        (error) => {
          this.postedBib = false;
          this._toastr.error(error.error, "", {
            positionClass: "toast-top-right",
          });
        }
      );
    }
  }

  search = (text$: Observable<string>) =>
    text$.pipe(
      debounceTime(200),
      distinctUntilChanged(),
      switchMap((searchText: string) =>
        this._dataService.autocompletBib(searchText).pipe(
          catchError(() => {
            return of([]);
          })
        )
      )
    );

  formatter = (result: any) => `${result.title}`;

  ngOnDestroy() {
    this.$_currentZhSub.unsubscribe();
    this.ngbModal.dismissAll();
  }
}
