import { Injectable } from "@angular/core";
import { throwError, of, Observable } from "rxjs";
import { map, catchError } from "rxjs/operators";
import { saveAs } from "file-saver";
import { ToastrService } from "ngx-toastr";

import { ZhDataService } from "./zh-data.service";
import { ZhFile, ZhFiles } from "../zh-forms/tabs/tab8/zh-form-tab8.models";

@Injectable({
  providedIn: "root",
})
export class FilesService {
  public files: ZhFile[] = [];
  public EXT_CSV = ["csv"];
  public EXT_PDF = ["pdf"];
  public EXT_IMAGES = [
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
  constructor(
    private _dataService: ZhDataService,
    private _toastr: ToastrService
  ) {}

  // Enables to filter files from their extension
  // so that they can be separated in the html
  filterByExtension(extensions: string[]): ZhFile[] {
    return this.files.filter((file) =>
      extensions.includes(file.media_path.split(".").slice(-1)[0])
    );
  }

  // Function to gather all the files that do not
  // respect the extensions provided
  unfilterByExtension(extensions: string[]): ZhFile[] {
    return this.files.filter(
      (file) => !extensions.includes(file.media_path.split(".").slice(-1)[0])
    );
  }

  getFileNameFromPath(path: string): string {
    return path.split(/(\\|\/)/g).pop();
  }

  // Function that saves the filename and guesses the type
  saveFile(blob: Blob, filename: string) {
    const name: string = this.getFileNameFromPath(filename);
    saveAs(blob, name);
  }

  loadFiles(zhId: number) {
    return this._dataService.getZhFiles(zhId).pipe(
      map((res: ZhFiles) => {
        this.files = res.media_data;
        this.files.map((item) => (item.mainPictureId = res.main_pict_id));
        return this.files;
      }),
      catchError((error) => {
        console.log(
          `Une erreur est survenue, impossible de récupérer les fichiers : <${error}>`
        );
        return throwError(error);
      })
    );
  }

  deleteFile(idMedia: number) {
    return this._dataService.deleteFile(idMedia).pipe(
      map(() => {
        this.displayInfo("Fichier supprimé avec succès");
      }),
      catchError((error) => {
        this.displayError(
          `Une erreur est survenue, impossible de supprimer ce fichier. Erreur : <${error.message}>`
        );
        return throwError(error);
      })
    );
  }

  changeMainPhoto(zhId: number, idMedia: number) {
    return this._dataService.postMainPicture(zhId, idMedia).pipe(
      map(() => {
        this.displayInfo("Photo principale changée avec succès");
      }),
      catchError((error) => {
        this.displayError(
          `Une erreur est survenue ! Impossible de changer la photo principale. Erreur : <${error.message}>`
        );
        return throwError(error);
      })
    );
  }

  downloadFile(id: number) {
    return this._dataService.downloadFile(id).toPromise();
  }

  postFile(uploadForm) {
    return this._dataService.postDataForm(uploadForm, 8).pipe(
      map(() => {
        this.displayInfo("Fichier téléversé avec succès !");
      }),
      catchError((error) => {
        this.displayError(
          `Une erreur est survenue, impossible de téléverser un fichier : <${error.message}>`
        );
        return throwError(error);
      })
    );
  }

  patchFile(fileIdToPatch: number, uploadForm: FormData) {
    return this._dataService.patchFile(fileIdToPatch, uploadForm).pipe(
      map(() => {
        this.displayInfo("Fichier téléversé avec succès !");
      }),
      catchError((error) => {
        this.displayError(
          `Une erreur est survenue, impossible de mettre à jour un fichier : <${error.message}>`
        );
        return throwError(error);
      })
    );
  }

  displayInfo(message: string) {
    this._toastr.success(message);
  }
  displayError(error: string) {
    this._toastr.error(error);
  }
}
