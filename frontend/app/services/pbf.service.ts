import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { ZhDataService } from "../services/zh-data.service";
import * as L from "leaflet";
import geobuf from "geobuf";
import Pbf from "pbf";

@Injectable({
  providedIn: "root",
})
export class PbfService {
  public res: ArrayBuffer;
  public vector: L.vectorGrid;

  constructor(private _zhService: ZhDataService) {}

  getPbf(currentMap: L.map): Observable<L.vectorGrid> {
    if (!currentMap.getPane("zhPane")) {
      currentMap.createPane("zhPane");
    }
    return this._zhService.getPbf().map(
      async (result) => {
        const res = await result["arrayBuffer"]();
        const pbf = new Pbf(res);
        const vector = await this.setVectorGrid(geobuf.decode(pbf));
        this.res = res;
        this.vector = vector;
        return vector;
      }
      // To prevent : Property 'arrayBuffer' does not exist on type 'Blob'
    );
  }

  setPaneBackground(currentMap: L.map): void {
    currentMap.getPane("zhPane").style.zIndex = "200";
  }

  setVectorGrid(geojson): L.vectorGrid {
    const vector = L.vectorGrid.slicer(geojson, {
      rendererFactory: L.canvas.tile,
      vectorTileLayerStyles: {
        sliced: function (properties, zoom) {
          return {
            fillColor: "#FFEDA0",
            fillOpacity: 1,
            color: "black",
            opacity: 1,
            weight: 1,
          };
        },
      },
      pane: "zhPane",
      interactive: true,
      maxZoom: 18,
      indexMaxZoom: 5,
    });
    return vector;
  }
}
