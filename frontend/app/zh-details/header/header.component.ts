import { Component, Input } from "@angular/core";
import { NgbModal } from "@ng-bootstrap/ng-bootstrap";
import { saveAs } from "file-saver";
import { ZhDataService } from "../../services/zh-data.service";
import { CommonService } from "@geonature_common/service/common.service";
import { Router } from "@angular/router";
import { CruvedStoreService } from "@geonature_common/service/cruved-store.service";

@Component({
  selector: "zh-details-header",
  templateUrl: "./header.component.html",
  styleUrls: ["./header.component.scss"],
})
export class HeaderComponent {
  @Input() zhId: number;
  public loadingPdf: boolean;

  constructor(
    public _cruvedStore: CruvedStoreService,
    private ngModal: NgbModal,
    private router: Router,
    private _zhService: ZhDataService,
    private _commonService: CommonService
  ) {}

  onOpen(modal) {
    const deleteModal = this.ngModal.open(modal, {
      centered: true,
    });

    deleteModal.result.then(
      () => {
        this.deleteZh(this.zhId);
      },
      () => {}
    );
  }

  deleteZh(idZh: number) {
    this._zhService.deleteOneZh(idZh).subscribe(
      () => {
        this._commonService.translateToaster(
          "success",
          "la zh a été supprimée avec succès"
        );
        this.router.navigate(["/zones_humides"]);
      },
      (error) => {
        if (error.status === 403) {
          this._commonService.translateToaster(
            "error",
            "Vous n'avez pas l'autorisation de supprimer la zone humide"
          );
        } else {
          this._commonService.translateToaster("error", `Erreur : ${error}`);
        }
      }
    );
  }

  onDownloadPdf() {
    this.loadingPdf = true;
    this._zhService.getPdf(this.zhId).subscribe(
      (result) => {
        this.loadingPdf = false;
        saveAs(result, "export.pdf");
      },
      (error) => {
        this.loadingPdf = false;
        console.log(error);
      },
      () => (this.loadingPdf = false)
    );
  }
}
