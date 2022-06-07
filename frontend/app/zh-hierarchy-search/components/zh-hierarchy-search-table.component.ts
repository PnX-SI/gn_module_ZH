import { Component, OnInit, Input } from "@angular/core";
import "leaflet-easybutton";
import { ZhDataService } from "../../services/zh-data.service";
import { ToastrService } from "ngx-toastr";
import { ErrorTranslatorService } from "../../services/error-translator.service";
import { FormGroup, FormBuilder, FormArray } from "@angular/forms";
import {
  HierarchyField,
  HierarchyFields,
  Note,
  RiverBasin,
} from "../../models/hierarchy";
import { TableColumn } from "../../commonComponents/table/table-interface";

type Data = {
  kownledges: string[];
  field: string;
  attributes: string;
};

@Component({
  selector: "zh-hierarchy-search-table",
  templateUrl: "./zh-hierarchy-search-table.component.html",
  styleUrls: ["./zh-hierarchy-search-table.component.scss"],
})
export class ZhHierarchySearchTableComponent implements OnInit {
  @Input() riverBasin: RiverBasin;
  @Input() form: FormGroup;

  public localForm: FormGroup;
  public fields: HierarchyField[];
  public notes: Note[];
  public filteredNotes: Note[] = [];
  public attributes: Note[] = [];
  public knowledges: Note[] = [];
  public mainSettings = {
    enableCheckAll: false,
    text: "Selectionner",
    searchPlaceholderText: "Rechercher",
    enableSearchFilter: true,
    disabled: false,
    singleSelection: true,
    noDataLabel: "Aucune donnée disponible",
    minSelectionLimit: 1,
  };
  public attributesSettings = {
    ...this.mainSettings,
    labelKey: "attribut",
    primaryKey: "id_attribut",
  };
  public knowledgeSettings = {
    ...this.mainSettings,
    labelKey: "note_type",
    primaryKey: "note_type",
  };

  public columns: TableColumn[] = [
    { name: "field", label: "Champs" },
    { name: "attributes", label: "Attribut", subarr: { name: "attribut" } },
    {
      name: "knowledges",
      label: "Connaissance",
      subarr: { name: "note_type" },
    },
  ];

  constructor(
    private _fb: FormBuilder,
    private _zhService: ZhDataService,
    private _toastr: ToastrService,
    private _error: ErrorTranslatorService
  ) {}

  get data() {
    return this.form.controls["hierarchy"] as FormArray;
  }

  ngOnInit() {
    this.createForm();
    if (this.riverBasin) {
      this._zhService
        .getHierarchyFields(this.riverBasin.code)
        .toPromise()
        .then((result: HierarchyFields) => {
          this.fields = result.categories;
          this.notes = result.items;
        })
        // TODO: catch error
        .catch(() => {})
        .finally(() => {});
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
    this.localForm.controls["attributes"].reset();
    this.localForm.controls["knowledges"].reset();

    const filteredNotes = this.notes.filter(
      (item) =>
        (item.volet == event &&
          item.rubrique == null &&
          item.sousrubrique == null) ||
        (item.rubrique == event && item.sousrubrique == null) ||
        item.sousrubrique == event
    );

    // Creates kind of a Set to have unique objects
    this.attributes = filteredNotes.filter(
      (v, i, a) =>
        a.findIndex((v2) => ["attribut"].every((k) => v2[k] === v[k])) === i
    );

    //FIXME: problem here
    this.knowledges = [];
    if (this.attributes.length > 0) {
      this.knowledges = this.getKnowledge(this.attributes[0]);
    }
    this.knowledgeSettings = {
      ...this.knowledgeSettings,
      disabled: this.knowledges.length === 0,
    };
    this.attributesSettings = {
      ...this.attributesSettings,
      disabled: this.attributes.length === 0,
      singleSelection: this.knowledges.length !== 0,
    };

    if (this.attributes.length > 0) {
      this.localForm.controls["attributes"].setValue([this.attributes[0]]);
    }
    if (this.knowledges.length > 0) {
      this.localForm.controls["knowledges"].setValue([this.knowledges[0]]);
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
      this.localForm.controls["knowledges"].setValue([this.knowledges[0]]);
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
      // Reset all form data
      this.reset();
    }
  }

  onDeleteFilter(event) {
    const item = this.getFilterIndex(event);
    this.data.removeAt(item);
  }
}
