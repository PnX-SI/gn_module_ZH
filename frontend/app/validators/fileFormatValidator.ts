import { FormControl } from "@angular/forms";
export function fileFormatValidator(formats: string[]) {
  return function (control: FormControl) {
    const file: File = control.value;
    if (file) {
      const format = file.type;
      console.log(formats.some((item) => format.match(item)));
      if (!formats.some((item) => format.match(item))) {
        return { fileFormatValidator: true };
      }
    }
    return null;
  };
}
