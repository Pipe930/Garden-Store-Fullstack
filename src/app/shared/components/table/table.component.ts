import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { TableColumns } from '../../interfaces/table';

@Component({
  selector: 'app-table',
  templateUrl: './table.component.html',
  styleUrls: ['./table.component.scss']
})
export class TableComponent implements OnInit {

  @Input() public tableColumns: Array<TableColumns> = [];
  @Input() public dataRows: Array<any> = [];
  @Input() public showActionButton: boolean = false;
  @Output() public eventPages = new EventEmitter<boolean>();

  ngOnInit(): void {

  }

}
