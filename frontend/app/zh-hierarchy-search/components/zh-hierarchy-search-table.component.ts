import { Component, OnInit, Input } from '@angular/core';
import { ZhDataService } from '../../services/zh-data.service';
import { ToastrService } from 'ngx-toastr';
import { ErrorTranslatorService } from '../../services/error-translator.service';
import { FormGroup, FormBuilder, FormArray } from '@angular/forms';
import { HierarchyField, HierarchyFields, Note, RiverBasin } from '../../models/hierarchy';
import { TableColumn } from '../../commonComponents/table/table-interface';

type Data = {
  knowledges: string[];
  field: string;
  attributes: string;
};

@Component({
  selector: 'zh-hierarchy-search-table',
  templateUrl: './zh-hierarchy-search-table.component.html',
  styleUrls: ['./zh-hierarchy-search-table.component.scss'],
})
export class ZhHierarchySearchTableComponent implements OnInit {
  private _riverBasin: RiverBasin;

  @Input() set riverBasin(value: RiverBasin) {
    this._riverBasin = value;
    this.setNotesAndFields();
  }
  get riverBasin(): RiverBasin {
    return this._riverBasin;
  }

  @Input() form: FormGroup;

  public localForm: FormGroup;
  public fields: HierarchyField[] = [];
  public notes: Note[] = [];
  public filteredNotes: Note[] = [];
  public attributes: Note[] = [];
  public knowledges: Note[] = [];
  public mainSettings = {
    enableCheckAll: false,
    text: 'Sélectionner',
    searchPlaceholderText: 'Rechercher',
    enableSearchFilter: true,
    disabled: false,
    singleSelection: true,
    noDataLabel: 'Aucune donnée disponible',
    minSelectionLimit: 1,
  };

  public columns: TableColumn[] = [
    { name: 'field', label: 'Rubrique' },
    { name: 'attributes', label: 'Attribut', subarr: { name: 'attribut' } },
    {
      name: 'knowledges',
      label: 'Connaissance',
      subarr: { name: 'note_type' },
    },
  ];

  constructor(
    private _fb: FormBuilder,
    private _zhService: ZhDataService,
    private _toastr: ToastrService,
    private _error: ErrorTranslatorService
  ) {}

  get data() {
    return this.form.controls['hierarchy'] as FormArray;
  }

  ngOnInit() {
    this.createForm();
    this.setNotesAndFields();
  }

  setNotesAndFields() {
    if (this.riverBasin) {
      this._zhService
        .getHierarchyFields(this.riverBasin.code)
        .toPromise()
        .then((result: HierarchyFields) => {
          this.fields = result.categories;
          this.notes = result.items;
        })
        // TODO: catch error
        .catch(() => {
          this.fields = [];
          this.notes = [];
        })
        .finally(() => {
          this.updateAttributesAndKnowledgeForm();
        });
    }
  }

  initialForm() {
    return this._fb.group({
      field: [null],
      attributes: [null],
      knowledges: [null],
    });
  }

  createForm() {
    this.localForm = this.initialForm();
  }

  reset() {
    this.localForm.reset();
    this.attributes = [];
    this.knowledges = [];
  }

  fieldChanged(event) {
    const filteredNotes = this.notes.filter(
      (item) =>
        (item.volet == event && item.rubrique == null && item.sousrubrique == null) ||
        (item.rubrique == event && item.sousrubrique == null) ||
        item.sousrubrique == event
    );

    // Creates kind of a Set to have unique objects
    this.attributes = filteredNotes.filter(
      (v, i, a) => a.findIndex((v2) => ['attribut'].every((k) => v2[k] === v[k])) === i
    );

    //FIXME: problem here
    this.knowledges = [];
    if (this.attributes.length > 0) {
      this.knowledges = this.getKnowledge(this.attributes[0]);
    }

    // Update the form
    this.updateAttributesAndKnowledgeForm();
  }

  updateAttributesAndKnowledgeForm() {
    const knowledgeControl = this.localForm.controls['knowledges'];
    const attributesControl = this.localForm.controls['attributes'];

    attributesControl.reset();
    knowledgeControl.reset();

    if (this.attributes.length) {
      attributesControl.enable();
      attributesControl.setValue([this.attributes[0]]);
    }
    else {
      attributesControl.disable();
    }


    if (this.knowledges.length > 0) {
      knowledgeControl.enable();
      knowledgeControl.setValue(this.knowledges[0]);
    }
    else {
      knowledgeControl.disable();
    }
  }

  getKnowledge(attribute) {
    return this.notes.filter(
      (item) =>
        item.id_attribut == attribute.id_attribut &&
        item.note_type != null &&
        item.cor_rule_id == attribute.cor_rule_id
    );
  }

  attributesChanged(event) {
    this.knowledges = this.getKnowledge(event);
    if (this.knowledges.length > 0) {
      this.localForm.controls['knowledges'].setValue([this.knowledges[0]]);
    }
  }

  getFilterIndex(value) {
    return this.data.value.findIndex(
      (item) =>
        item.field == value.field &&
        item.attributes == value.attributes &&
        item.knowledges == value.knowledges
    );
  }

  onAddFilter() {
    const item = this.getFilterIndex(this.localForm.value);
    if (item === -1) {
      const form = this.initialForm();
      form.patchValue(this.localForm.value);
      this.data.push(form);
      let knowledges_array = [];
      this.data.value.forEach((element) => {
        if (element['knowledges'] !== null && !Array.isArray(element['knowledges'])) {
          // avoid object object in 'connaissance' column of the frontend table
          knowledges_array.push(element['knowledges']);
          element['knowledges'] = knowledges_array;
          knowledges_array = [];
        }
      });
    }
    this.reset();
  }

  onDeleteFilter(event) {
    const item = this.getFilterIndex(event);
    this.data.removeAt(item);
  }
}
