import { Component, EventEmitter, OnInit, Input, Output } from "@angular/core";
import { FormGroup, FormBuilder, Validators } from "@angular/forms";
import { NgbModal, NgbModalRef } from "@ng-bootstrap/ng-bootstrap";
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
  public loadingUpload: boolean = false;

  public modalTitle: string;
  public activeModal: NgbModalRef;
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
      author: [null, Validators.required],
      summary: null,
    });
  }

  getCurrentZh() {
    this._dataService.currentZh.subscribe((zh: any) => {
      this.zh = zh;
    });
  }

  onAddDoc(event: any, modal: any) {
    this.modalTitle = "Ajout d'un fichier";
    this.onOpenModal(modal);
  }

  onEditDoc(event: any, modal: any) {
    this.modalTitle = "Edition d'un fichier";
    this.onOpenModal(modal);
  }

  onOpenModal(modal) {
    this.activeModal = this.ngbModal.open(modal, {
      centered: true,
      size: "lg",
      windowClass: "bib-modal",
    });

    this.activeModal.result.then().finally(() => {
      this.resetForm();
    });
  }

  resetForm() {
    this.docForm.reset();
    this.fileToUpload = null;
  }

  onDeleteStatus() {}

  handleFileInput(files: FileList) {
    this.fileToUpload = files.item(0);
    this.docForm.patchValue({
      file: this.fileToUpload,
    });
  }

  postFile() {
    this.loadingUpload = true;
    const uploadForm = new FormData();
    uploadForm.append("id_zh", this.zh.id);
    uploadForm.append("title", this.docForm.value.title);
    uploadForm.append("author", this.docForm.value.author);
    uploadForm.append("summary", this.docForm.value.summary);
    uploadForm.append("file", this.fileToUpload, this.fileToUpload.name);
    this._dataService
      .postDataForm(uploadForm, 8)
      .toPromise()
      .then((res) => {
        this.activeModal.close();
        this.displayInfo("Fichier téléversé avec succès !");
      })
      .catch((error) => {
        this.displayError(
          `Une erreur est survenue, impossible d'uploader un fichier : <${error.message}>`
        );
      })
      .finally(() => {
        this.loadingUpload = false;
      });
  }

  displayInfo(message: string) {
    this._toastr.success(message);
  }
  displayError(error: string) {
    this._toastr.error(error);
  }

  onFormSubmit() {}
}
