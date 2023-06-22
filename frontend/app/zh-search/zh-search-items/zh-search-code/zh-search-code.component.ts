import { Component, OnInit, Input } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { of, Observable } from 'rxjs';
import { ZhDataService } from '../../../services/zh-data.service';
import { debounceTime, distinctUntilChanged, switchMap, catchError, map } from 'rxjs/operators';
@Component({
  selector: 'zh-search-code',
  templateUrl: './zh-search-code.component.html',
  styleUrls: ['./zh-search-code.component.scss'],
})
export class ZhSearchCodeComponent implements OnInit {
  @Input() form: FormGroup;

  constructor(private _dataService: ZhDataService) {}

  ngOnInit() {}

  search = (text$: Observable<string>) =>
    text$.pipe(
      debounceTime(200),
      distinctUntilChanged(),
      switchMap((searchText: string) =>
        searchText
          ? // FIXME: hardcoded nameorcode.........
            this._dataService.search({ nameorcode: searchText }, { limit: 15 }).pipe(
              map((res: any) => res.items.features.map((feat) => feat.properties.fullname)),
              catchError(() => {
                return of([]);
              })
            )
          : of([])
      )
    );
}
