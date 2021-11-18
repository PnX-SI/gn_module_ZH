import { Injectable } from "@angular/core";
import { throwError } from "rxjs";
import { map, catchError } from "rxjs/operators";
import { saveAs } from "file-saver";
import { ToastrService } from "ngx-toastr";

import { ZhDataService } from "./zh-data.service";

type ZhFile = {
  id_media: number;
  id_nomenclature_media_type: number;
  id_table_location: number;
  unique_id_media: string;
  uuid_attached_row: string;
  title_fr: string;
  title_en: string | null;
  title_it: string | null;
  title_es: string | null;
  title_de: string | null;
  media_url: string | null;
  media_path: string;
  author: string;
  description_fr: string;
  description_en: string | null;
  description_it: string | null;
  description_es: string | null;
  description_de: string | null;
  is_public: boolean;
  meta_create_date: Date;
  meta_update_date: Date;
  image?: string | ArrayBuffer;
  mainPictureId?: number;
};

type ZhFiles = {
  media_data: ZhFile[];
  main_pict_id: number;
};

@Injectable({
  providedIn: "root",
})
export class FilesService {
  public files: ZhFile[];
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
  filterByExtension(files: ZhFile[], extensions: string[]): ZhFile[] {
    return files.filter((file) =>
      extensions.includes(file.media_path.split(".").slice(-1)[0])
    );
  }

  // Function to gather all the files that do not
  // respect the extensions provided
  unfilterByExtension(files: ZhFile[], extensions: string[]): ZhFile[] {
    return files.filter(
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
          `Une erreur est survenue, impossible de récupérer les fichiers : <${error.message}>`
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
