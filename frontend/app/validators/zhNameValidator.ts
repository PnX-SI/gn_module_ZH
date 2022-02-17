import { FormControl } from "@angular/forms";
import { timer } from "rxjs";
import { switchMap, map } from "rxjs/operators";
import { ZhDataService } from "../services/zh-data.service";

/*
export function zhNameValidator(dataService: ZhDataService, time: number) {
  return function (control: FormControl) {
    const name: string = control.value;
    return timer(time).pipe(
      switchMap(() => dataService.search({ nameorcode: name })),
      map((res: any) => {
        let currentZhId: number = null;
        dataService.currentZh.subscribe((data) => {
          if (data) currentZhId = data.id;
        });
        return res.total === 0
          ? null
          : res.items.features[0].id === currentZhId
          ? null
          : { zh_exists: true };
      })
    );
  };
}
*/
