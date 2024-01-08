import { Component, HostListener, OnInit } from '@angular/core';
import { notifications, userItems } from './header-dummy-data';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {

  public canShowSearchAsOverlay: boolean = true;
  public listNotifications = notifications;
  public listUserItems = userItems;

  ngOnInit(): void {
    this.checkCanShowSearch(window.innerWidth);
  }

  @HostListener('window:resize', ['$event'])
  onResize(event: any){
    this.checkCanShowSearch(window.innerWidth);
  }

  public checkCanShowSearch(innerWidth: number):void {

    if(innerWidth < 845){

      this.canShowSearchAsOverlay = true;
    } else {

      this.canShowSearchAsOverlay = false;
    }
  }

}
