import { FormControl } from "@angular/forms";
import { timer } from "rxjs";
import { switchMap, map } from "rxjs/operators";
import { ZhDataService } from "../services/zh-data.service";

export function zhNameValidator(dataService: ZhDataService, time: number) {
  return function (control: FormControl) {
    const name: string = control.value;
    return timer(time).pipe(
      switchMap(() => dataService.search({ nameorcode: name })),
      map((res: any) => {
        return res.total === 0 ? null : { zh_exists: true };
      })
    );
  };
}
