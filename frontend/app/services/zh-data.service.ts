import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { AppConfig } from "@geonature_config/app.config";

@Injectable({
  providedIn: "root",
})
export class ZhDataService {
  constructor(private _api: HttpClient) {}

  /*
  getZhList() {
    return this._api.get<any>(`${AppConfig.API_ENDPOINT}/zones_humides`);
  }
  */

  deleteOneZh(id) {
    return this._api.delete(`${AppConfig.API_ENDPOINT}/zones_humides/${id}`);
  }

  getForm(idTab) {
    return this._api.get<any>(`${AppConfig.API_ENDPOINT}/zones_humides/form/${idTab}`);
  }

  postUserData(value, geom, idTab) {
    value['geom'] = geom;
    const urlpost = `${AppConfig.API_ENDPOINT}/zones_humides/form/${idTab}/data`
    console.log(urlpost);
    console.log(value);
    return this._api.post<any>(urlpost, value);
  }

}