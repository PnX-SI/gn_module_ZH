import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class TabsService {
  private tabChange = new BehaviorSubject(null);

  constructor() {}

  setTabChange(tab: any) {
    this.tabChange.next(tab);
  }

  getTabChange() {
    return this.tabChange.asObservable();
  }
}
