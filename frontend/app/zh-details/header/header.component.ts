import { Component, Input } from "@angular/core";
import { NgbModal } from "@ng-bootstrap/ng-bootstrap";
import { DeleteModalComponent } from "../../commonComponents/delete-modal/delete-modal.component";
import { ZhDataService } from "../../services/zh-data.service";
import { CommonService } from "@geonature_common/service/common.service";
import { Router } from "@angular/router";

@Component({
  selector: "zh-details-header",
  templateUrl: "./header.component.html",
  styleUrls: ["./header.component.scss"],
})
export class HeaderComponent {
  @Input() zhId: number;

  constructor(
    private ngModal: NgbModal,
    private router: Router,
    private _zhService: ZhDataService,
    private _commonService: CommonService
  ) {}

  onOpen() {
    const deleteModal = this.ngModal.open(DeleteModalComponent, {
      centered: true,
    });

    deleteModal.componentInstance.title = "World";
    deleteModal.componentInstance.message =
      "Etes-vous sûr de vouloir supprimer cette Zone Humide ? Cette action est irréversible";
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
}
