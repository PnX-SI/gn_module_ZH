import { Component, Input } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { Router } from '@angular/router';
import { TabsService } from '../../services/tabs.service';

@Component({
  selector: 'zh-cancelButton',
  templateUrl: './cancelButton.component.html',
  styleUrls: ['./cancelButton.component.scss'],
})
export class CancelButtonComponent {
  @Input() zhId: number;
  constructor(
    public ngbModal: NgbModal,
    private router: Router,
    private _tabService: TabsService
  ) {}

  onCancel(modal: any) {
    if (!this.zhId) {
      this.router.navigate(['/zones_humides']);
    } else {
      this.ngbModal.open(modal, {
        centered: true,
        windowClass: 'bib-modal cancel-modal',
      });
    }
  }

  onExit() {
    // Theses lines are good => keep it
    // Set the next tab so that this._tabService.tabChange is 0
    this._tabService.setTabChange(0);
    this.router.navigate([`/zones_humides`]);
  }
}
