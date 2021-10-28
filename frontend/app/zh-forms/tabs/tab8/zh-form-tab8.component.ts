import { Component, EventEmitter, OnInit, Input, Output } from "@angular/core";
import { FormGroup, FormBuilder, Validators } from "@angular/forms";
import { NgbModal, NgbModalRef } from "@ng-bootstrap/ng-bootstrap";
import { TabsService } from "../../../services/tabs.service";
import { saveAs } from "file-saver";

import { ToastrService } from "ngx-toastr";

import { ZhDataService } from "../../../services/zh-data.service";
import { fileSizeValidator } from "../../../validators/fileSizeValidator";
import { fileNameValidator } from "../../../validators/fileNameValidator";
import { fileFormatValidator } from "../../../validators/fileFormatValidator";

import { ZhFile } from "./zh-form-tab8.models";

const EXT_CSV = ["csv"];
const EXT_PDF = ["pdf"];
const EXT_IMAGES = [
  "png",
  "tif",
  "tiff",
  "wbmp",
  "ico",
  "jng",
  "bmp",
  "svg",
  "webp",
  "gif",
  "jpeg",
  "jpg",
];

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

  public docTableCol = [
    {
      name: "title_fr",
      label: "Titre du document",
    },
    { name: "author", label: "Auteur" },
    { name: "description_fr", label: "Résumé" },
  ];

  public corFilesExt = [];

  constructor(
    private fb: FormBuilder,
    public ngbModal: NgbModal,
    private _dataService: ZhDataService,
    private _toastr: ToastrService,
    private _tabService: TabsService
  ) {}

  ngOnInit() {
    this.getCurrentZh();
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
          fileNameValidator(this.zh.properties.code),
        ]),
      ],
      title: [null, Validators.required],
      author: [null, Validators.required],
      summary: null,
    });
  }

  initExtensions() {
    this.corFilesExt = [
      { name: "Fichiers pdf", files: this.getFilesByExtensions(EXT_PDF) },
      { name: "Photos", files: this.getFilesByExtensions(EXT_IMAGES) },
      { name: "Fichiers CSV", files: this.getFilesByExtensions(EXT_CSV) },
      {
        name: "Autres fichiers",
        files: this.getOtherFiles(EXT_PDF.concat(EXT_IMAGES, EXT_CSV)),
      },
    ];
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

  getFiles() {
    this._dataService
      .getZhFiles(this.zh.id)
      .toPromise()
      .then((res: ZhFile[]) => {
        this.files = res;
        this.initExtensions();
      })
      .catch((error) => {
        this.displayError(
          `Une erreur est survenue, impossible de récupérer les fichiers : <${error.message}>`
        );
      });
  }

  // Enables to filter files from their extension
  // so that they can be separated in the html
  getFilesByExtensions(extensions: string[]): ZhFile[] {
    return this.files.filter((file) =>
      extensions.includes(file.media_path.split(".").slice(-1)[0])
    );
  }

  // Function to gather all the files that do not
  // respect the extensions provided
  getOtherFiles(extensions: string[]): ZhFile[] {
    return this.files.filter(
      (file) => !extensions.includes(file.media_path.split(".").slice(-1)[0])
    );
  }

  onAddDoc(event: any, modal: any) {
    this.modalTitle = "Ajout d'un fichier";
    this.patchModal = false;
    this.onOpenModal(modal);
  }

  onEditDoc(event: any, modal: any) {
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

  //TODO: filename, filecontent
  fillForm(filepath: string, title: string, author: string, summary: string) {
    const filename: string = this.getFileNameFromPath(filepath);
    this.fileToUpload = new File([""], filename);
    this.docForm.patchValue({
      title: title,
      author: author,
      summary: summary,
    });
  }

  getFileNameFromPath(path: string): string {
    return path.split(/(\\|\/)/g).pop();
  }

  onDeleteDoc(event) {
    this._dataService
      .deleteFile(event.id_media)
      .toPromise()
      .then((res) => {
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

  onDownloadDoc(event) {
    this._dataService
      .downloadFile(event.id_media)
      .toPromise()
      .then((res) => {
        let blob = new Blob([res]);
        saveAs(blob, this.getFileNameFromPath(event.media_path));
      })
      .catch((error) => {
        console.log(error);
        this.displayError(
          `Une erreur est survenue, impossible de télécharger ce fichier. Erreur : <${error.message}>`
        );
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

  resetForm() {
    this.docForm.reset();
    this.fileToUpload = null;
  }

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
        this.getFiles();
      });
  }

  patchFile() {
    // Check if file is empty: not changed
    console.log("Not implemented yet");
  }

  displayInfo(message: string) {
    this._toastr.success(message);
  }
  displayError(error: string) {
    this._toastr.error(error);
  }
}
