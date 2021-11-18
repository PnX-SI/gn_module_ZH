import { Component, EventEmitter, OnInit, Input, Output } from "@angular/core";
import { FormGroup, FormBuilder, Validators } from "@angular/forms";
import { NgbModal, NgbModalRef } from "@ng-bootstrap/ng-bootstrap";

import { ToastrService } from "ngx-toastr";

import { ModuleConfig } from "../../../module.config";
import { ZhDataService } from "../../../services/zh-data.service";
import { fileSizeValidator } from "../../../validators/fileSizeValidator";
import { fileNameValidator } from "../../../validators/fileNameValidator";
import { fileFormatValidator } from "../../../validators/fileFormatValidator";

import { ZhFile, ZhFiles } from "./zh-form-tab8.models";
import { FilesService } from "../../../services/files.service";
import { TabsService } from "../../../services/tabs.service";

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
  public config = ModuleConfig;
  public formTab8: FormGroup;
  public fileForm: FormGroup;
  public files: ZhFile[];
  public fileToUpload: File | null = null;
  public fileIdToPatch: number | null = null;
  public loadingUpload: boolean = false;

  public modalTitle: string;
  public patchModal: boolean = false;
  public activeModal: NgbModalRef;
  public addModalBtnLabel: string;
  public posted: boolean;
  public submitted: boolean;

  public fileTypeAccepted: string[] = ["application/pdf", "image/*"];

  public fileTableCol = [
    {
      name: "title_fr",
      label: "Titre du document",
    },
    { name: "author", label: "Auteur" },
    { name: "description_fr", label: "Résumé" },
  ];

  public corFilesExt = [];
  public imageFiles = {};

  constructor(
    private fb: FormBuilder,
    public ngbModal: NgbModal,
    private _dataService: ZhDataService,
    private _toastr: ToastrService,
    private _filesService: FilesService,
    private _tabService: TabsService
  ) {}

  ngOnInit() {
    this._tabService.getTabChange().subscribe((tabPosition: number) => {
      if (tabPosition == 8) {
        this.getCurrentZh();
      }
    });
    this.getCurrentZh();
  }

  // initialize forms
  initForms() {
    this.fileForm = this.fb.group({
      file: [null, Validators.compose(this.getValidators())],
      title: [null, Validators.required],
      author: [null, Validators.required],
      summary: null,
    });
  }

  getValidators() {
    let validators = [Validators.required];
    if (this.config.fileformat_validated) {
      validators.push(fileFormatValidator(this.fileTypeAccepted));
    }
    if (this.config.filename_validated) {
      validators.push(fileNameValidator(this.zh.properties.code));
    }

    validators.push(
      fileSizeValidator(
        this.config.max_jpg_size * 1000,
        this.config.max_pdf_size * 1000
      )
    );

    return validators;
  }

  initExtensions() {
    const EXT_PDF = this._filesService.EXT_PDF;
    const EXT_IMAGES = this._filesService.EXT_IMAGES;
    const EXT_CSV = this._filesService.EXT_CSV;
    this.handleImages();
    this.corFilesExt = [
      { name: "Fichiers pdf", files: this.getFilesByExtensions(EXT_PDF) },
      { name: "Fichiers CSV", files: this.getFilesByExtensions(EXT_CSV) },
      {
        name: "Autres fichiers",
        files: this.getOtherFiles(EXT_PDF.concat(EXT_IMAGES, EXT_CSV)),
      },
    ];
  }

  handleImages() {
    let files = this.getFilesByExtensions(this._filesService.EXT_IMAGES);
    files.map((item) => {
      this._filesService.downloadFile(item.id_media).then((res) => {
        const reader = new FileReader();
        reader.readAsDataURL(res);
        reader.onloadend = () => {
          item.image = reader.result;
        };
      });
    });
    this.imageFiles = {
      name: "Photos",
      files: files,
    };
  }

  getCurrentZh() {
    this._dataService.currentZh.subscribe((zh: any) => {
      if (zh) {
        this.zh = zh;
        this.initForms();
        this.getFiles();
      }
    });
  }

  // Enables to filter files from their extension
  // so that they can be separated in the html
  getFilesByExtensions(extensions: string[]): ZhFile[] {
    return this._filesService.filterByExtension(
      this._filesService.files,
      extensions
    );
  }

  // Function to gather all the files that do not
  // respect the extensions provided
  getOtherFiles(extensions: string[]): ZhFile[] {
    return this._filesService.unfilterByExtension(
      this._filesService.files,
      extensions
    );
  }

  onAddFile(event: any, modal: any) {
    this.modalTitle = "Ajout d'un fichier";
    this.patchModal = false;
    this.onOpenModal(modal);
  }

  onEditFile(event: any, modal: any) {
    this.modalTitle = "Edition d'un fichier";
    this.fillForm(
      event.media_path,
      event.title_fr,
      event.author,
      event.description_fr
    );
    this.fileIdToPatch = event.id_media;
    this.patchModal = true;
    this.onOpenModal(modal);
  }

  fillForm(filepath: string, title: string, author: string, summary: string) {
    const filename: string = this._filesService.getFileNameFromPath(filepath);
    // Set empty file, to be checked in PATCH
    this.fileToUpload = new File([""], filename);
    this.fileForm.patchValue({
      title: title,
      author: author,
      summary: summary,
    });
  }

  async getFiles() {
    await this._filesService
      .loadFiles(this.zh.id)
      .toPromise()
      .then(() => this.initExtensions());
  }

  onDeleteFile(event) {
    this._filesService
      .deleteFile(event.id_media)
      .toPromise()
      .finally(() => this.getFiles());
  }

  onDownloadFile(event) {
    this._filesService
      .downloadFile(event.id_media)
      .then((res) => {
        this._filesService.saveFile(res, event.media_path);
      })
      // TODO: to remove !
      .catch((error) => {
        this.displayError(
          `Une erreur est survenue ! Impossible de télécharger ce fichier. Erreur : <${error.message}>`
        );
      });
  }

  onChangeMainPhoto(event) {
    this._filesService
      .changeMainPhoto(this.zh.id, event.id_media)
      .toPromise()
      .finally(() => this.getFiles());
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

  handleFileInput(files: FileList) {
    this.fileToUpload = files.item(0);
    this.fileForm.patchValue({
      file: this.fileToUpload,
    });
  }

  fillUploadForm(patchFile: boolean = true): FormData {
    const uploadForm = new FormData();
    uploadForm.append("id_zh", this.zh.id);
    uploadForm.append("title", this.fileForm.value.title);
    uploadForm.append("author", this.fileForm.value.author);
    uploadForm.append("summary", this.fileForm.value.summary);
    if (patchFile) {
      uploadForm.append("file", this.fileToUpload, this.fileToUpload.name);
    }
    return uploadForm;
  }

  postFile() {
    this.loadingUpload = true;
    const uploadForm = this.fillUploadForm(true);
    this._filesService
      .postFile(uploadForm)
      .toPromise()
      .then(() => this.activeModal.close())
      .finally(() => {
        this.loadingUpload = false;
        this.getFiles();
      });
  }

  patchFile() {
    this.loadingUpload = true;
    const uploadForm: FormData = this.fillUploadForm(
      this.fileToUpload.size !== 0
    );
    this._filesService
      .patchFile(this.fileIdToPatch, uploadForm)
      .toPromise()
      .then(() => {
        this.activeModal.close();
        this.getFiles();
      })
      .catch((err) => console.log(err))
      .finally(() => {
        this.loadingUpload = false;
      });
  }

  resetForm() {
    this.fileForm.reset();
    this.fileToUpload = null;
  }

  displayError(error: string) {
    this._toastr.error(error);
  }
}
