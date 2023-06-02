import { FormControl } from '@angular/forms';
export function fileFormatValidator(formats: string[]) {
  return function (control: FormControl) {
    const file: File = control.value;
    if (file) {
      const format = file.type;
      if (!formats.some((item) => format.match(item) !== null)) {
        return { fileFormatValidator: true };
      }
    }
    return null;
  };
}
