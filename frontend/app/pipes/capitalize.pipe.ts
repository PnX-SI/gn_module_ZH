import { Pipe, PipeTransform } from "@angular/core";

// To be DRY, define a reusable function that converts a
// (word or sentence) to title case

const toTitleCase = (value) => {
  return value.substring(0, 1).toUpperCase() + value.substring(1);
  // alternately, can also use this:
  // return value.charAt(0).toUpperCase() + value.slice(1);
};

@Pipe({
  name: "capitalize",
})
export class CapitalizePipe implements PipeTransform {
  transform(value: any, args?: any): any {
    if (value) {
      return toTitleCase(value);
    }
    return value;
  }
}
