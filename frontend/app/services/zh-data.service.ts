import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { AppConfig } from "@geonature_config/app.config";

@Injectable({
  providedIn: "root",
})
export class ZhDataService {
  constructor(private _api: HttpClient) { }

  /*
  getZhList() {
    return this._api.get<any>(`${AppConfig.API_ENDPOINT}/zones_humides`);
  }
  */

  deleteOneZh(id) {
    return this._api.delete(`${AppConfig.API_ENDPOINT}/zones_humides/${id}`);
  }

  getMetaDataForm(idForm: number) {
    return this._api.get<any>(`${AppConfig.API_ENDPOINT}/zones_humides/form/${idForm}`);
  }

  postDataForm(value, idForm) {
    const urlpost = `${AppConfig.API_ENDPOINT}/zones_humides/form/${idForm}`
    return this._api.post<any>(urlpost, value);
  }

}