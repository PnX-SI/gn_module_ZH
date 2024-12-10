import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { BehaviorSubject } from 'rxjs';
import { map } from 'rxjs/operators';
import { ConfigService } from '@geonature/services/config.service';

import { DetailsModel } from '../zh-details/models/zh-details.model';
import { HierarchyModel } from '../zh-details/models/hierarchy.model';

@Injectable({
  providedIn: 'root',
})
export class ZhDataService {
  private zh = new BehaviorSubject(null);
  public currentZh = this.zh.asObservable();

  constructor(
    private _api: HttpClient,
    public config: ConfigService
  ) {}

  setCurrentZh(zh: any) {
    this.zh.next(zh);
  }

  getStatic(filename: string) {
    return `${this.config.API_ENDPOINT}/zones_humides/static/${filename}`;
  }

  getZhById(id: number) {
    return this._api.get<any>(`${this.config.API_ENDPOINT}/zones_humides/${id}`);
  }

  deleteOneZh(id: number) {
    return this._api.delete(`${this.config.API_ENDPOINT}/zones_humides/${id}`);
  }

  getMetaDataForms() {
    this.config.API_ENDPOINT;
    return this._api.get<any>(`${this.config.API_ENDPOINT}/zones_humides/forms`);
  }

  postDataForm(value: any, idForm: number) {
    const urlpost = `${this.config.API_ENDPOINT}/zones_humides/form/${idForm}`;
    return this._api.post<any>(urlpost, value);
  }

  autocompletBib(search_title: string) {
    return this._api.get<any>(
      `${this.config.API_ENDPOINT}/zones_humides/references/autocomplete?search_title=${search_title}`
    );
  }

  checkRefGeo() {
    return this._api.get<any>(`${this.config.API_ENDPOINT}/zones_humides/check_ref_geo`);
  }

  getHabitatByCorine(corineId: string) {
    return this._api.get<any>(
      `${this.config.API_ENDPOINT}/zones_humides/forms/cahierhab/${corineId}`
    );
  }

  getEvalZh(zhId: string) {
    return this._api.get<any>(`${this.config.API_ENDPOINT}/zones_humides/eval/${zhId}`);
  }

  getMunicipalitiesByZh(zhId: number) {
    return this._api
      .get<any>(`${this.config.API_ENDPOINT}/zones_humides/municipalities/${zhId}`)
      .pipe(
        map((municipalities: any) => {
          municipalities.map((item) => (item.disabled = false));
          return municipalities;
        })
      );
  }

  getAllZhGeom() {
    return this._api.get<any>(`${this.config.API_ENDPOINT}/zones_humides/geometries`);
  }

  getZhDetails(zhId: number) {
    return this._api.get<DetailsModel>(
      `${this.config.API_ENDPOINT}/zones_humides/${zhId}/complete_card`
    );
  }

  getZhFiles(zhId: number) {
    return this._api.get(`${this.config.API_ENDPOINT}/zones_humides/${zhId}/files`);
  }

  deleteFile(mediaId: number) {
    return this._api.delete(`${this.config.API_ENDPOINT}/zones_humides/files/${mediaId}`);
  }

  downloadFile(mediaId: number) {
    return this._api.get(`${this.config.API_ENDPOINT}/zones_humides/files/${mediaId}`, {
      responseType: 'blob',
    });
  }

  patchFile(mediaId: number, form: FormData) {
    return this._api.patch(`${this.config.API_ENDPOINT}/zones_humides/files/${mediaId}`, form);
  }

  postMainPicture(zhId: number, mediaId: number) {
    return this._api.patch(
      `${this.config.API_ENDPOINT}/zones_humides/${zhId}/main_pict/${mediaId}`,
      {}
    );
  }

  getTaxa(zhId: number) {
    return this._api.get(`${this.config.API_ENDPOINT}/zones_humides/${zhId}/taxa`);
  }

  getHierZh(zhId: string, headers?: HttpHeaders | { [header: string]: string | string[] }) {
    return this._api.get(`${this.config.API_ENDPOINT}/zones_humides/${zhId}/hierarchy`, {
      headers,
    });
  }

  getPdf(zhId: number) {
    return this._api.get(`${this.config.API_ENDPOINT}/zones_humides/export_pdf/${zhId}`, {
      responseType: 'blob',
    });
  }

  getDepartments() {
    return this._api.get(`${this.config.API_ENDPOINT}/zones_humides/departments`);
  }

  getCommuneFromDepartment(code: number) {
    const payload = { code: code };
    return this._api.post(`${this.config.API_ENDPOINT}/zones_humides/communes`, payload);
  }

  getBasins() {
    return this._api.get(`${this.config.API_ENDPOINT}/zones_humides/bassins`);
  }

  getHydroZoneFromBasin(code: number) {
    const payload = { code: code };
    return this._api.post(`${this.config.API_ENDPOINT}/zones_humides/zones_hydro`, payload);
  }

  getHierarchyFields(basinId: number) {
    return this._api.get(`${this.config.API_ENDPOINT}/zones_humides/hierarchy/fields/${basinId}`);
  }

  // Search is a function that filter or not all the ZH
  search(payload: Object, options?) {
    return this._api.post(`${this.config.API_ENDPOINT}/zones_humides`, payload, {
      params: options,
    });
  }

  getPbf() {
    return this._api.get(`${this.config.API_ENDPOINT}/zones_humides/pbf`, {
      responseType: 'blob',
    });
  }
  getRights(idZh: number) {
    return this._api.get(`${this.config.API_ENDPOINT}/zones_humides/user/rights/${idZh}`);
  }
}
