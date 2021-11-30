import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { BehaviorSubject, pipe } from "rxjs";
import { map } from "rxjs/operators";
import { AppConfig } from "@geonature_config/app.config";
import { DetailsModel } from "../zh-details/models/zh-details.model";
import { HierarchyModel } from "../zh-details/models/hierarchy.model";

@Injectable({
  providedIn: "root",
})
export class ZhDataService {
  private zh = new BehaviorSubject(null);
  public currentZh = this.zh.asObservable();

  constructor(private _api: HttpClient) {}

  setCurrentZh(zh: any) {
    this.zh.next(zh);
  }

  getZhById(id: number) {
    return this._api.get<any>(`${AppConfig.API_ENDPOINT}/zones_humides/${id}`);
  }

  deleteOneZh(id: number) {
    return this._api.delete(`${AppConfig.API_ENDPOINT}/zones_humides/${id}`);
  }

  getMetaDataForms() {
    return this._api.get<any>(`${AppConfig.API_ENDPOINT}/zones_humides/forms`);
  }

  postDataForm(value: any, idForm: number) {
    const urlpost = `${AppConfig.API_ENDPOINT}/zones_humides/form/${idForm}`;
    return this._api.post<any>(urlpost, value);
  }

  postBib(value: any) {
    const urlpost = `${AppConfig.API_ENDPOINT}/zones_humides/references`;
    return this._api.post<any>(urlpost, value);
  }

  autocompletBib(search_title: string) {
    return this._api.get<any>(
      `${AppConfig.API_ENDPOINT}/zones_humides/references/autocomplete?search_title=${search_title}`
    );
  }

  patchBib(value: any) {
    const urlpost = `${AppConfig.API_ENDPOINT}/zones_humides/references`;
    return this._api.patch<any>(urlpost, value);
  }

  checkRefGeo() {
    return this._api.get<any>(
      `${AppConfig.API_ENDPOINT}/zones_humides/check_ref_geo`
    );
  }

  getHabitatByCorine(corineId: string) {
    return this._api.get<any>(
      `${AppConfig.API_ENDPOINT}/zones_humides/forms/cahierhab/${corineId}`
    );
  }

  getEvalZh(zhId: string) {
    return this._api.get<any>(
      `${AppConfig.API_ENDPOINT}/zones_humides/eval/${zhId}`
    );
  }

  getMunicipalitiesByZh(zhId: number) {
    return this._api
      .get<any>(
        `${AppConfig.API_ENDPOINT}/zones_humides/municipalities/${zhId}`
      )
      .pipe(
        map((municipalities: any) => {
          municipalities.map((item) => (item.disabled = false));
          return municipalities;
        })
      );
  }

  getAllZhGeom() {
    return this._api.get<any>(
      `${AppConfig.API_ENDPOINT}/zones_humides/geometries`
    );
  }

  getZhDetails(zhId: number) {
    return this._api.get<DetailsModel>(
      `${AppConfig.API_ENDPOINT}/zones_humides/${zhId}/complete_card`
    );
  }

  getTaxa(zhId: number) {
    return this._api.get(
      `${AppConfig.API_ENDPOINT}/zones_humides/`
    );
  }

  getHierZh(zhId: string) {
    return this._api.get<HierarchyModel>(
      `${AppConfig.API_ENDPOINT}/zones_humides/${zhId}/hierarchy`
    );
  }
}
