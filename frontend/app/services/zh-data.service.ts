import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { BehaviorSubject } from 'rxjs';
import { AppConfig } from "@geonature_config/app.config";

@Injectable({
  providedIn: "root",
})
export class ZhDataService {

  private zh = new BehaviorSubject(null);
  public currentZh = this.zh.asObservable();

  constructor(private _api: HttpClient) { }

  setCurrentZh(zh: any) {
    this.zh.next(zh);
  }

  getZhById(id: number) {
    return this._api.get<any>(`${AppConfig.API_ENDPOINT}/zones_humides/${id}`);
  }


  deleteOneZh(id) {
    return this._api.delete(`${AppConfig.API_ENDPOINT}/zones_humides/${id}`);
  }


  getMetaDataForms() {
    return this._api.get<any>(`${AppConfig.API_ENDPOINT}/zones_humides/forms`);
  }

  postDataForm(value, idForm) {
    const urlpost = `${AppConfig.API_ENDPOINT}/zones_humides/form/${idForm}`
    return this._api.post<any>(urlpost, value);
  }

  patchDataForm(value, idForm) {
    const urlpost = `${AppConfig.API_ENDPOINT}/zones_humides/form/${idForm}`
    return this._api.patch<any>(urlpost, value);
  }

}