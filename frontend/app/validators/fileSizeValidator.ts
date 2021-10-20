import { FormControl } from "@angular/forms";
export function fileSizeValidator(maxSize: number, maxSizePdf?) {
  return function (control: FormControl) {
    const file: File = control.value;
    if (file) {
      if (file.type == "application/pdf") {
        maxSize = maxSizePdf;
      }
      const fileSize: number = file.size;
      const fileSizeInKB: number = Math.round(fileSize / 1024);
      if (fileSizeInKB >= maxSize) {
        return {
          fileSizeValidator: true,
        };
      }
    }
    return null;
  };
}
