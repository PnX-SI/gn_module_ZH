import { Component, Input, ChangeDetectionStrategy } from "@angular/core";
import { TableColumn } from "./table-interface";

@Component({
  selector: "zh-table",
  templateUrl: "./table.component.html",
  styleUrls: ["./table.component.scss"],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class TableComponent {
  @Input() tableCols: TableColumn[];
  @Input() data: any;

  isArray(value) {
    return Array.isArray(value);
  }
}
