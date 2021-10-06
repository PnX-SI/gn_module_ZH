import { Component, Input } from "@angular/core";
import { TableColumn } from "./table-interface";

@Component({
  selector: "zh-table",
  templateUrl: "./table.component.html",
  styleUrls: ["./table.component.scss"],
})
export class TableComponent {
  @Input() tableCols: TableColumn[];
  @Input() data: any;
}
