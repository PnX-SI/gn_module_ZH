import { FormControl } from "@angular/forms";
export function fileSizeValidator(maxSize: number) {
  return function (control: FormControl) {
    // return (control: AbstractControl): { [key: string]: any } | null => {
    const file: File = control.value;
    if (file) {
      console.log(file);
      const fileSize: number = file.size;
      const fileSizeInKB: number = Math.round(fileSize / 1024);
      if (fileSizeInKB >= maxSize) {
        return {
          fileSizeValidator: true,
        };
      } else {
        return null;
      }
    }
    return null;
  };
}
