import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Subscription, of, Observable } from 'rxjs';
import { debounceTime, distinctUntilChanged, switchMap, catchError, map } from 'rxjs/operators';
import { ToastrService } from 'ngx-toastr';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { ZhDataService } from '../../../services/zh-data.service';
import { TabsService } from '../../../services/tabs.service';
import { ErrorTranslatorService } from '../../../services/error-translator.service';
import { ConfigService } from '@geonature/services/config.service';
import { HierarchyService } from '../../../services/hierarchy.service';

@Component({
  selector: 'zh-form-tab1',
  templateUrl: './zh-form-tab1.component.html',
  styleUrls: ['./zh-form-tab1.component.scss'],
})
export class ZhFormTab1Component implements OnInit {
  @Input() formMetaData;
  @Output() canChangeTab = new EventEmitter<boolean>();
  @Output() nextTab = new EventEmitter<number>();
  public generalInfoForm: FormGroup;
  public bibForm: FormGroup;
  public siteSpaceList: any[];
  public hasSiteSpace = false;
  public appConfig;
  public currentZh: any;
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
  public cols = [
    { name: 'title', label: 'Titre du document' },
    { name: 'authors', label: 'Auteurs' },
    { name: 'pub_year', label: 'Année de parution' },
  ];

  constructor(
    private fb: FormBuilder,
    private _dataService: ZhDataService,
    private _toastr: ToastrService,
    private _tabService: TabsService,
    private _error: ErrorTranslatorService,
    public ngbModal: NgbModal,
    private _config: ConfigService,
    public hierarchy: HierarchyService
  ) {}

  ngOnInit() {
    this.appConfig = this._config;
    this.getMetaData();
    this.createForm();

    this._tabService.getTabChange().subscribe((tabPosition: number) => {
      if (this.$_fromChangeSub) this.$_fromChangeSub.unsubscribe();
      if (this.$_currentZhSub) this.$_currentZhSub.unsubscribe();
      if (tabPosition == 1) {
        this.initTab();
      }
    });
  }

  initTab() {
    this.$_currentZhSub = this._dataService.currentZh.subscribe((zh: any) => {
      if (zh) {
        this.currentZh = zh;
        this.listBib = [...this.currentZh.properties.id_references];
        this.generalInfoForm.patchValue({
          main_name: this.currentZh.properties.main_name,
          secondary_name: this.currentZh.properties.secondary_name,
          is_id_site_space: this.currentZh.properties.is_id_site_space,
          id_site_space: this.currentZh.properties.id_site_space,
          id_zh: this.currentZh.properties.id_zh,
        });
        this.$_fromChangeSub = this.generalInfoForm.valueChanges.subscribe(() => {
          this.canChangeTab.emit(false);
        });
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
    this.generalInfoForm.get('is_id_site_space').valueChanges.subscribe((val: Boolean) => {
      if (val == true) {
        this.generalInfoForm.get('id_site_space').enable();
        this.hasSiteSpace = true;
      } else if (val == false) {
        this.hasSiteSpace = false;
        this.generalInfoForm.get('id_site_space').reset();
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
      let itemExist = this.listBib.some((item) => item.id_reference == bib.id_reference);
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
      id_zh: Number(this.currentZh.properties.id_zh),
      id_site_space: formValues.id_site_space,
      is_id_site_space: formValues.is_id_site_space,
      id_references: [],
    };

    if (this.generalInfoForm.valid) {
      this.$_fromChangeSub.unsubscribe();
      if (formValues.main_name != this.currentZh.properties.main_name) {
        formValues.main_name = formValues.main_name;
      }
      this.listBib.forEach((bib) => {
        formToPost.id_references.push(bib.id_reference);
      });
      this.posted = true;
      this._dataService.postDataForm(formToPost, 1).subscribe(
        () => {
          this._dataService.getZhById(this.currentZh.properties.id_zh).subscribe((zh: any) => {
            this._dataService.setCurrentZh(zh);
            this.posted = false;
            this.canChangeTab.emit(true);
            this._toastr.success('Vos données sont bien enregistrées', '', {
              positionClass: 'toast-top-right',
            });
            if (this.currentZh.properties.main_id_rb) {
              this.hierarchy.getHierarchy(this.currentZh.properties.id_zh);
            }
            this.nextTab.emit(2);
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

  search = (text$: Observable<string>) =>
    text$.pipe(
      debounceTime(200),
      distinctUntilChanged(),
      switchMap((searchText: string) =>
        this._dataService.autocompletBib(searchText).pipe(
          map((res: any) =>
            res.filter((r) => {
              return !this.listBib.map((bib) => bib.id_reference).includes(r.id_reference);
            })
          ),
          catchError(() => {
            return of([]);
          })
        )
      )
    );

  formatter = (result: any) => `${result.title}`;

  ngOnDestroy() {
    if (this.$_currentZhSub) this.$_currentZhSub.unsubscribe();
    this.ngbModal.dismissAll();
    this.hierarchy.warning = '';
  }
}
