import { Component, Input } from "@angular/core";
import { NgbModal } from "@ng-bootstrap/ng-bootstrap";
import { ZhDataService } from "../../services/zh-data.service";
import { CommonService } from "@geonature_common/service/common.service";
import { Router } from "@angular/router";
import { ErrorTranslatorService } from "../../services/error-translator.service";
import { TabsService } from "../../services/tabs.service";

@Component({
  selector: "zh-details-header",
  templateUrl: "./header.component.html",
  styleUrls: ["./header.component.scss"],
})
export class HeaderComponent {
  @Input() zhId: number;
  @Input() zhCode: number;
  @Input() rights;
  public loadingPdf: boolean = false;

  constructor(
    private ngModal: NgbModal,
    private router: Router,
    private _zhService: ZhDataService,
    private _commonService: CommonService,
    private _error: ErrorTranslatorService,
    private _tabService: TabsService
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
        this._commonService.translateToaster("success", "la zh a été supprimée avec succès");
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
        const rawDate: string = new Date().toLocaleDateString();
        const date: string = rawDate.replace(/\//g, "-");
        const filename: string = `${this.zhCode}_${date}_fiche.pdf`;
        // Not possible to use saveas since it does not open it in a
        // new tab => create a <a> then click on it...
        const blob = new Blob([result], { type: "application/type" });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = filename;
        link.target = "_blank";
        link.click();
      },
      (error) => {
        this.loadingPdf = false;
        const frontMsg: string =
          "Erreur de téléchargement du PDF " + this._error.getFrontError(error.error.message);
        this._commonService.translateToaster("error", frontMsg);
      },
      () => (this.loadingPdf = false)
    );
  }

  resetTabService() {
    // Set the next tab so that this._tabService.tabChange is 0
    this._tabService.setTabChange(0);
  }

  onModify(zhId) {
    this.resetTabService();
    this.router.navigate([`/zones_humides/forms/${zhId}`]);
  }

  onReturn() {
    this.resetTabService();
    this.router.navigate([`/zones_humides`]);
  }
}
