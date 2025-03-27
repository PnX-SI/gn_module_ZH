import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { ZhDataService } from '../services/zh-data.service';
import * as L from 'leaflet';
import geobuf from 'geobuf';
import Pbf from 'pbf';
import 'leaflet.vectorgrid';
/// <reference path="leaflet.vectorgrid.d.ts"/>

@Injectable({
  providedIn: 'root',
})
export class PbfService {
  public res: ArrayBuffer;
  public vector: any;

  constructor(private _zhService: ZhDataService) {}

  // FIXME : return Observable<L.vectorGrid>
  getPbf(currentMap: L.Map): Observable<any> {
    if (!currentMap.getPane('zhPane')) {
      currentMap.createPane('zhPane');
    }
    return this._zhService.getPbf().pipe(
      map(async (result) => {
        const res = await result['arrayBuffer']();
        if (res.byteLength === 0) return null;
        const pbf = new Pbf(res);
        const vector = await this.setVectorGrid(geobuf.decode(pbf));
        this.res = res;
        this.vector = vector;
        return vector;
      })
      // To prevent : Property 'arrayBuffer' does not exist on type 'Blob'
    );
  }

  setPaneBackground(currentMap: L.Map): void {
    currentMap.getPane('zhPane').style.zIndex = '200';
  }

  // FIXME : return a L.vectorGrid
  setVectorGrid(geojson) {
    const vector = (L as any).vectorGrid.slicer(geojson, {
      rendererFactory: (L as any).svg.tile,
      vectorTileLayerStyles: {
        sliced: function (properties, zoom) {
          let opacity = 0.8;

          return {
            fillColor: '#800080',
            fillOpacity: 0.5,
            color: '#800080',
            opacity: opacity,
            weight: 2,
            fill: true,
          };
        },
      },
      pane: 'zhPane',
      interactive: true,
      maxZoom: 18,
      indexMaxZoom: 5,
    });
    return vector;
  }
}
