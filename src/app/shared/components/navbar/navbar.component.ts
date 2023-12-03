import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Navbar } from '../../interfaces/navbar';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent implements OnInit {

  @Input() public sessionActivate: boolean = false;
  @Input() public ObjectsNavbar: Array<Navbar> = [];
  @Output() public eventThemeNavbar = new EventEmitter<boolean>();

  public themeNavbar: boolean = false;

  constructor() { }

  ngOnInit(): void {
    this.eventThemeNavbar.emit(this.themeNavbar);
  }

  public themeChange():void{

    if(!this.themeNavbar){
      this.themeNavbar = true;
    } else {
      this.themeNavbar = false;
    }
  }

}
