import { Component, EventEmitter, OnInit, Input, Output } from "@angular/core";
import { FormGroup, FormBuilder, Validators } from "@angular/forms";
import { NgbModal, NgbModalRef } from "@ng-bootstrap/ng-bootstrap";

import { ToastrService } from "ngx-toastr";

import { AppConfig } from "@geonature_config/app.config";
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
  public formTab8: FormGroup;
  public fileForm: FormGroup;
  public files: ZhFile[];
  public fileToUpload: File | null = null;
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
    if (AppConfig.fileformat_validated) {
      validators.push(fileFormatValidator(this.fileTypeAccepted));
    }
    if (AppConfig.filename_validated) {
      validators.push(fileNameValidator(this.zh.properties.code));
    }

    if (AppConfig.max_jpg_size) {
      validators.push(fileSizeValidator(AppConfig.max_jpg_size * 1000));
    }

    if (AppConfig.max_jpg_size && AppConfig.max_pdf_size) {
      validators.push(fileSizeValidator(AppConfig.max_jpg_size * 1000));
    }

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
      this.downloadFile(item.id_media).then((res) => {
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
    return this._filesService.filterByExtension(this.files, extensions);
  }

  // Function to gather all the files that do not
  // respect the extensions provided
  getOtherFiles(extensions: string[]): ZhFile[] {
    return this._filesService.unfilterByExtension(this.files, extensions);
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

  getFiles() {
    this._dataService
      .getZhFiles(this.zh.id)
      .toPromise()
      .then((res: ZhFiles) => {
        this.files = res.media_data;
        this.files.map((item) => (item.mainPictureId = res.main_pict_id));
        this.initExtensions();
      })
      .catch((error) => {
        this.displayError(
          `Une erreur est survenue, impossible de récupérer les fichiers : <${error.message}>`
        );
      });
  }

  onDeleteFile(event) {
    this._dataService
      .deleteFile(event.id_media)
      .toPromise()
      .then(() => {
        this.displayInfo("Fichier supprimé avec succès");
      })
      .catch((error) => {
        this.displayError(
          `Une erreur est survenue, impossible de supprimer ce fichier. Erreur : <${error.message}>`
        );
      })
      .finally(() => {
        this.getFiles();
      });
  }

  onDownloadFile(event) {
    this.downloadFile(event.id_media)
      .then((res) => {
        this._filesService.saveFile(res, event.media_path);
      })
      .catch((error) => {
        this.displayError(
          `Une erreur est survenue ! Impossible de télécharger ce fichier. Erreur : <${error.message}>`
        );
      });
  }

  downloadFile(id: number) {
    return this._dataService.downloadFile(id).toPromise();
  }

  onChangeMainPhoto(event) {
    console.log(event);
    this._dataService
      .postMainPicture(this.zh.id, event.id_media)
      .toPromise()
      .then(() => {
        this.displayInfo("Photo principale changée avec succès");
      })
      .catch((error) => {
        this.displayError(
          `Une erreur est survenue ! Impossible de changer la photo principale. Erreur : <${error.message}>`
        );
      })
      .finally(() => {
        this.getFiles();
      });
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

  postFile() {
    this.loadingUpload = true;
    const uploadForm = new FormData();
    uploadForm.append("id_zh", this.zh.id);
    uploadForm.append("title", this.fileForm.value.title);
    uploadForm.append("author", this.fileForm.value.author);
    uploadForm.append("summary", this.fileForm.value.summary);
    uploadForm.append("file", this.fileToUpload, this.fileToUpload.name);
    this._dataService
      .postDataForm(uploadForm, 8)
      .toPromise()
      .then(() => {
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
        this.getFiles();
      });
  }

  patchFile() {
    // Check if file is empty: not changed
    console.log("Not implemented yet");
  }

  resetForm() {
    this.fileForm.reset();
    this.fileToUpload = null;
  }

  displayInfo(message: string) {
    this._toastr.success(message);
  }
  displayError(error: string) {
    this._toastr.error(error);
  }
}
