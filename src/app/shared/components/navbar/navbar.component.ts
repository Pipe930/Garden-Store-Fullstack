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
  public modeOriginal:string = "Normal";
  public modeDark:string = "Oscuro";
  public mode:string = this.modeOriginal;
  public showClass:boolean = false;

  ngOnInit(): void {
    this.eventThemeNavbar.emit(this.themeNavbar);
  }

  public openNavbar():void{
    let containerNavbar = document.querySelector(".navbar__container-right");
    containerNavbar?.classList.add("visible");
  }

  public closeNavbar():void{
    let containerNavbar = document.querySelector(".navbar__container-right");
    containerNavbar?.classList.remove("visible");
  }

  public themeChange():void{

    if(this.mode === this.modeOriginal){
      this.mode = this.modeDark;
    } else {
      this.mode = this.modeOriginal;
    }

    if(!this.themeNavbar){
      this.themeNavbar = true;
    } else {
      this.themeNavbar = false;
    }
  }

}
