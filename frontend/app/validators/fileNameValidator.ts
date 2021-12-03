import { FormControl } from "@angular/forms";
export function fileNameValidator(zhId) {
  return function (control: FormControl) {
    const file: File = control.value;
    if (file) {
      if (file.type != "application/pdf") {
        const name: string = file.name;
        const regex: RegExp = new RegExp("^" + zhId + "_[0-9]", "gm");
        if (regex.exec(name) == null) {
          return {
            fileNameValidator: true,
          };
        }
      }
    }
    return null;
  };
}
