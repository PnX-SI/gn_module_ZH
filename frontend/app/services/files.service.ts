import { Injectable } from "@angular/core";
import { ZhFile } from "../zh-forms/tabs/tab8/zh-form-tab8.models";
import { saveAs } from "file-saver";

@Injectable({
  providedIn: "root",
})
export class FilesService {
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
  constructor() {}

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
}
