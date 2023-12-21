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
  @Output() public eventEdit = new EventEmitter<any>();

  ngOnInit(): void {

  }

  public onEdit(object: any):void{

    this.eventEdit.emit(object);
  }

}
