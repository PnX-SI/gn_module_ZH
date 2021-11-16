import { FormControl } from "@angular/forms";
import { timer } from "rxjs";
import { switchMap, map } from "rxjs/operators";
import { ZhDataService } from "../services/zh-data.service";

export function zhNameValidator(dataService: ZhDataService, time: number) {
  return function (control: FormControl) {
    const name: string = control.value;
    return timer(time).pipe(
      switchMap(() => dataService.search({ code: name })),
      map((res: any) => {
        console.log(res.total);
        return res.total === 0 ? null : { zh_exists: true };
      })
    );
  };
}
// import { Injectable } from "@angular/core";
// import {
//   ValidationErrors,
//   AbstractControl,
//   AsyncValidator,
// } from "@angular/forms";
// import { Observable } from "rxjs";
// import { map, catchError, of } from "rxjs/operators";
// import { ZhDataService } from "../services/zh-data.service";

// @Injectable({ providedIn: "root" })
// export class zhNameValidator implements AsyncValidator {
//   constructor(private dataService: ZhDataService) {}

//   validate(
//     name: AbstractControl
//   ): Promise<ValidationErrors | null> | Observable<ValidationErrors | null> {
//     return this.dataService.search({ code: name }).pipe(
//       map((res) => (res.total !== 0 ? { zh_exists: true } : null)),
//       catchError(() => of(null))
//     );
//   }
// }
