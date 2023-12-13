import { Component } from '@angular/core';
import { SidenavToggle } from '../shared/interfaces/sidenav';

@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.scss']
})
export class AdminComponent  {

  public isSidenavCollapsed: boolean = false;
  public screenWidth: number = 0;

  constructor() { }

  public onToggleSideNav(data: SidenavToggle):void {

    this.screenWidth = data.screenWidth;
    this.isSidenavCollapsed = data.collapsed;
  }

  public getBodyClass():string{

    let styleClass = "";
    if(this.isSidenavCollapsed && this.screenWidth > 768){
      styleClass = "body-trimmed";
    } else if(this.isSidenavCollapsed && this.screenWidth <= 768 && this.screenWidth > 0) {
      styleClass = "body-md-screen"
    }
    return styleClass;
  }

}
