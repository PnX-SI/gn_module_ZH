import { Injectable } from "@angular/core";
import { ZhFile } from "../zh-forms/tabs/tab8/zh-form-tab8.models";

@Injectable({
  providedIn: "root",
})
export class FilesService {
  constructor() {}

  filterByExtension(files: ZhFile[], extensions: string[]): ZhFile[] {
    return files.filter((file) =>
      extensions.includes(file.media_path.split(".").slice(-1)[0])
    );
  }
}
