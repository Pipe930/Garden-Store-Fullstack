import { Component, EventEmitter, HostListener, OnInit, Output, inject } from '@angular/core';
import { navbarData } from './navbar-data';
import { Sidenav, SidenavToggle } from '../../interfaces/sidenav';
import { animate, keyframes, style, transition, trigger } from '@angular/animations';
import { Router } from '@angular/router';

@Component({
  selector: 'app-sidenav',
  templateUrl: './sidenav.component.html',
  styleUrls: ['./sidenav.component.scss'],
  animations: [
    trigger("fadeInOut", [
      transition(":enter", [
        style({opacity: 0}),
        animate(".3s",
          style({opacity: 1})
        )
      ]),
      transition(":leave", [
        style({opacity: 1}),
        animate(".3s",
          style({opacity: 0})
        )
      ])
    ]),
    trigger("rotate", [
      transition(":enter", [
        animate("1s",
          keyframes([
            style({transform: "rotate(0deg)", offset: 0}),
            style({transform: "rotate(2turn)", offset: 1})
          ])
        )
      ])
    ])
  ]
})
export class SidenavComponent implements OnInit {

  @Output() public onToggleSideNav = new EventEmitter<SidenavToggle>();
  public collapsed: boolean = false;
  public screenWidth: number = 0;
  public navData = navbarData;
  public multiple: boolean = false;

  private readonly _router = inject(Router);

  @HostListener("window:resize", ["$event"])
  onResize(event: any) {

    this.screenWidth = window.innerWidth;

    if(this.screenWidth <= 768){

      this.collapsed = false;
      this.onToggleSideNav.emit({collapsed: this.collapsed, screenWidth: this.screenWidth});
    }
  }

  ngOnInit(): void {
    this.screenWidth = window.innerWidth;
  }

  public toggleCollapse():void {
    this.collapsed = !this.collapsed;
    this.onToggleSideNav.emit({collapsed: this.collapsed, screenWidth: this.screenWidth});
  }

  public closeSidenav():void{
    this.collapsed = false;
    this.onToggleSideNav.emit({collapsed: this.collapsed, screenWidth: this.screenWidth});
  }

  public handleClick(item: Sidenav):void {

    if(!this.multiple){

      for(let modelItem of this.navData){

        if(item !== modelItem && modelItem.expanded){
          modelItem.expanded = false;
        }
      }
    }

    item.expanded = !item.expanded;
  }

  public getActiveClass(data:Sidenav): string{
    return this._router.url.includes(data.routerLink) ? "active": "";
  }
}
