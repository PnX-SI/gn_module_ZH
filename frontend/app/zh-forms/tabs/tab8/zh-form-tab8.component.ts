import { Component, EventEmitter, OnInit, Input, Output } from "@angular/core";
import { FormGroup, FormBuilder, Validators } from "@angular/forms";
import { NgbModal } from "@ng-bootstrap/ng-bootstrap";
import { TabsService } from "../../../services/tabs.service";

import { ToastrService } from "ngx-toastr";

import { ZhDataService } from "../../../services/zh-data.service";
import { fileSizeValidator } from "../../../validators/fileSizeValidator";
import { fileNameValidator } from "../../../validators/fileNameValidator";
import { fileFormatValidator } from "../../../validators/fileFormatValidator";

@Component({
  selector: "zh-form-tab8",
  templateUrl: "./zh-form-tab8.component.html",
  styleUrls: ["./zh-form-tab8.component.scss"],
})
export class ZhFormTab8Component implements OnInit {
  @Input() public formMetaData: any;
  @Output() public canChangeTab = new EventEmitter<boolean>();
  @Output() nextTab = new EventEmitter<number>();
  public zh: any;
  public formTab8: FormGroup;
  public docForm: FormGroup;
  public fileToUpload: File | null = null;

  public modalTitle: string;
  public addModalBtnLabel: string;
  public posted: boolean;
  public submitted: boolean;
  private $_fromChangeSub: any;

  public fileTypeAccepted: string[] = ["application/pdf", "image/*"];

  constructor(
    private fb: FormBuilder,
    public ngbModal: NgbModal,
    private _dataService: ZhDataService,
    private _toastr: ToastrService,
    private _tabService: TabsService
  ) {}

  ngOnInit() {
    this.getCurrentZh();
    this.initForms();
  }

  // initialize forms
  initForms() {
    this.docForm = this.fb.group({
      file: [
        null,
        Validators.compose([
          Validators.required,
          fileFormatValidator(this.fileTypeAccepted),
          fileSizeValidator(500, 1500),
          fileNameValidator(this.zh.id),
        ]),
      ],
      title: [null, Validators.required],
      profile: [null, Validators.required],
      author: [null, Validators.required],
      summary: null,
    });
  }

  getCurrentZh() {
    this._dataService.currentZh.subscribe((zh: any) => {
      this.zh = zh;
      console.log(this.zh);
    });
  }

  onAddDoc(event: any, modal: any) {
    this.modalTitle = "Ajout d'un fichier";
    const modalRef = this.ngbModal.open(modal, {
      centered: true,
      size: "lg",
      windowClass: "bib-modal",
    });

    modalRef.result.then().finally(() => {
      this.resetForm();
    });
  }

  resetForm() {
    this.docForm.reset();
    this.fileToUpload = null;
  }

  onDeleteStatus() {}

  onEditDoc() {
    this.modalTitle = "Editer un fichier";
  }

  handleFileInput(files: FileList) {
    this.fileToUpload = files.item(0);
    this.docForm.patchValue({
      file: this.fileToUpload,
    });
    console.log(this.docForm);
  }

  postFile() {
    const reader = new FileReader();
    reader.readAsDataURL(this.fileToUpload);

    reader.onload = () => {};
  }

  onFormSubmit() {}
}
