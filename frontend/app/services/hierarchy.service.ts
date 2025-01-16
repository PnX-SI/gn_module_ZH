import { Injectable } from '@angular/core';
import { ZhDataService } from './zh-data.service';
import { HierarchyModel } from '../zh-details/models/hierarchy.model';
import { ItemModel } from '../zh-details/models/hierarchy.model';
import { TableColumn } from '../commonComponents/table/table-interface';
import { ToastrService } from 'ngx-toastr';
import { ErrorTranslatorService } from './error-translator.service';

@Injectable({
  providedIn: 'root',
})
export class HierarchyService {
  public hierTableCols: TableColumn[] = [
    { name: 'name', label: 'RUBRIQUE' },
    { name: 'qualification', label: 'QUALIFICATION' },
    { name: 'knowledge', label: 'CONNAISSANCE' },
    { name: 'note', label: 'NOTE' },
  ];

  public bold_row_values: any = [' '];
  public italic_row_values: any = ['Total rubrique'];
  public color_col_name: string = 'name';
  public color_value: string = '';
  public currentZh: any;
  //public hierZh: HierarchyModel = null;
  public items: ItemModel[];
  public isLoading: boolean = false;
  public warning: string = '';

  constructor(
    private _dataService: ZhDataService,
    private _error: ErrorTranslatorService,
    private _toastr: ToastrService
  ) {}

  ngOnInit(): void {
    this.isLoading = false;
  }

  getHierarchyFromZh(zh) {
    if (zh.properties.main_id_rb) {
      this.getHierarchy(zh.properties.id_zh);
    }
  }

  // get current zone humides
  getHierarchy(zhId) {
    this.isLoading = true;
    this.warning = '';
    this._dataService
      .getHierZh(zhId, {
        'not-to-handle': '1',
      })
      .subscribe(
        (data: HierarchyModel) => {
          this.setItems(data);
        },
        (error) => {
          this.isLoading = false;
          this.items = [];
          if (error.status === 404) {
            this.warning = "La ZH n'est présente dans aucun bassin versant";
          } else if (error.status === 400) {
            this.warning = this._error['errors'].filter(
              (i) => error.error['message'] === i.api
            )[0].front;
          }
          this.deleteNotes(zhId);
        },
        () => {
          this.isLoading = false;
        }
      );
  }

  deleteNotes(idZH: number) {
    return this._dataService.deleteNotes(idZH).subscribe();
  }

  // set list of hierarchy items
  setItems(data) {
    if (data == null) {
      this.items = [];
      return;
    }

    this.items = [{ name: '', active: true, qualification: '', knowledge: '', note: '' }];

    // cat 1
    this.items.push({
      name: data.volet1.cat1_sdage.name.toUpperCase(),
      active: true,
      qualification: '',
      knowledge: '',
      note: '',
    });
    this.bold_row_values.push(data.volet1.cat1_sdage.name.toUpperCase());
    this.items.push(data.volet1.cat1_sdage.items[0]);
    this.items.push({
      name: ' ',
      active: true,
      qualification: '',
      knowledge: 'Total rubrique',
      note: data.volet1.cat1_sdage.note,
    });

    this.items.push({
      name: '',
      active: true,
      qualification: '',
      knowledge: '',
      note: '',
    });

    // cat 4
    this.items.push({
      name: data.volet1.cat4_hydro.name.toUpperCase(),
      active: true,
      qualification: '',
      knowledge: '',
      note: '',
    });
    this.bold_row_values.push(data.volet1.cat4_hydro.name.toUpperCase());
    this.items.push(data.volet1.cat4_hydro.items[0]);
    this.items.push(data.volet1.cat4_hydro.items[1]);
    this.items.push(data.volet1.cat4_hydro.items[2]);
    this.items.push({
      name: ' ',
      active: true,
      qualification: '',
      knowledge: 'Total rubrique',
      note: data.volet1.cat4_hydro.note,
    });

    this.items.push({
      name: '',
      active: true,
      qualification: '',
      knowledge: '',
      note: '',
    });

    // cat 3
    this.items.push({
      name: data.volet1.cat3_eco.name.toUpperCase(),
      active: true,
      qualification: '',
      knowledge: '',
      note: '',
    });
    this.bold_row_values.push(data.volet1.cat3_eco.name.toUpperCase());
    this.items.push(data.volet1.cat3_eco.items[0]);
    this.items.push({
      name: ' ',
      active: true,
      qualification: '',
      knowledge: 'Total rubrique',
      note: data.volet1.cat3_eco.note,
    });

    this.items.push({
      name: '',
      active: true,
      qualification: '',
      knowledge: '',
      note: '',
    });

    // cat 2
    this.items.push({
      name: data.volet1.cat2_heritage.name.toUpperCase(),
      active: true,
      qualification: '',
      knowledge: '',
      note: '',
    });
    this.bold_row_values.push(data.volet1.cat2_heritage.name.toUpperCase());
    this.items.push(data.volet1.cat2_heritage.items[0]);
    this.items.push(data.volet1.cat2_heritage.items[1]);
    this.items.push(data.volet1.cat2_heritage.items[2]);
    this.items.push(data.volet1.cat2_heritage.items[3]);
    this.items.push({
      name: ' ',
      active: true,
      qualification: '',
      knowledge: 'Total rubrique',
      note: data.volet1.cat2_heritage.note,
    });

    this.items.push({
      name: '',
      active: true,
      qualification: '',
      knowledge: '',
      note: '',
    });

    // cat 5
    this.items.push({
      name: data.volet1.cat5_soc_eco.name.toUpperCase(),
      active: true,
      qualification: '',
      knowledge: '',
      note: '',
    });
    this.bold_row_values.push(data.volet1.cat5_soc_eco.name.toUpperCase());
    this.items.push(data.volet1.cat5_soc_eco.items[0]);
    this.items.push(data.volet1.cat5_soc_eco.items[1]);
    this.items.push({
      name: ' ',
      active: true,
      qualification: '',
      knowledge: 'Total rubrique',
      note: data.volet1.cat5_soc_eco.note,
    });

    this.items.push({
      name: '',
      active: true,
      qualification: '',
      knowledge: '',
      note: '',
    });

    // note volet 1
    this.items.push({
      name: ' ',
      active: true,
      qualification: '',
      knowledge: 'NOTE VOLET 1 - VALEUR GLOBALE',
      note: data.volet1.note,
    });
    //this.bold_row_values.push("NOTE VOLET 1 - VALEUR GLOBALE");
    this.items.push({
      name: '',
      active: true,
      qualification: '',
      knowledge: '',
      note: '',
    });

    // cat 6
    this.items.push({
      name: data.volet2.cat6_status.name.toUpperCase(),
      active: true,
      qualification: '',
      knowledge: '',
      note: '',
    });
    this.bold_row_values.push(data.volet2.cat6_status.name.toUpperCase());
    this.items.push(data.volet2.cat6_status.items[0]);
    this.items.push(data.volet2.cat6_status.items[1]);
    this.items.push({
      name: ' ',
      active: true,
      qualification: '',
      knowledge: 'Total rubrique',
      note: data.volet2.cat6_status.note,
    });

    this.items.push({
      name: '',
      active: true,
      qualification: '',
      knowledge: '',
      note: '',
    });

    // cat 7
    this.items.push({
      name: data.volet2.cat7_fct_state.name.toUpperCase(),
      active: true,
      qualification: '',
      knowledge: '',
      note: '',
    });
    this.bold_row_values.push(data.volet2.cat7_fct_state.name.toUpperCase());
    this.items.push(data.volet2.cat7_fct_state.items[0]);
    this.items.push(data.volet2.cat7_fct_state.items[1]);
    this.items.push({
      name: ' ',
      active: true,
      qualification: '',
      knowledge: 'Total rubrique',
      note: data.volet2.cat7_fct_state.note,
    });

    this.items.push({
      name: '',
      active: true,
      qualification: '',
      knowledge: '',
      note: '',
    });

    // cat 8
    this.items.push({
      name: data.volet2.cat8_thread.name.toUpperCase(),
      active: true,
      qualification: '',
      knowledge: '',
      note: '',
    });
    this.bold_row_values.push(data.volet2.cat8_thread.name.toUpperCase());
    this.items.push(data.volet2.cat8_thread.items[0]);
    this.items.push({
      name: ' ',
      active: true,
      qualification: '',
      knowledge: 'Total rubrique',
      note: data.volet2.cat8_thread.note,
    });

    this.items.push({
      name: '',
      active: true,
      qualification: '',
      knowledge: '',
      note: '',
    });

    // note volet 2 - priorite d'intervention
    this.items.push({
      name: ' ',
      active: true,
      qualification: '',
      knowledge: "NOTE VOLET 2 - PRIORITE D'INTERVENTION",
      note: data.volet2.note,
    });
    //this.bold_row_values.push("NOTE VOLET 2 - PRIORITE D'INTERVENTION");

    this.items.push({
      name: '',
      active: true,
      qualification: '',
      knowledge: '',
      note: '',
    });

    // note globale
    this.items.push({
      name: ' ',
      active: true,
      qualification: '',
      knowledge: 'TOTAL',
      note: data.global_note,
    });
    //this.bold_row_values.push("TOTAL");

    // note globale
    this.items.push({
      name: ' ',
      active: true,
      qualification: '',
      knowledge: 'NOTE FINALE',
      note: data.final_note,
    });
    //this.bold_row_values.push("NOTE FINALE");
  }
}
