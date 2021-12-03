import { FormControl } from "@angular/forms";
export function fileSizeValidator(maxSizePhoto?: number, maxSizePdf?: number) {
  return function (control: FormControl) {
    const file: File = control.value;
    if (file) {
      let maxSize: number = maxSizePhoto;
      if (file.type == "application/pdf") {
        maxSize = maxSizePdf;
      }
      const fileSize: number = file.size;
      const fileSizeInKB: number = Math.round(fileSize / 1024);
      if (maxSize && fileSizeInKB >= maxSize) {
        return {
          fileSizeValidator: true,
        };
      }
    }
    return null;
  };
}
