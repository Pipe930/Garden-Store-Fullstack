import { Component, Input, OnInit } from '@angular/core';
import { Sidenav } from '../../interfaces/sidenav';
import { animate, state, style, transition, trigger } from '@angular/animations';
import { Router } from '@angular/router';

@Component({
  selector: 'app-sublevel-menu',
  template: `

    <ul *ngIf="collapsed && data.items && data.items.length > 0"
    class="sublevel-nav"
    [@submenu]="expanded
    ? {value: 'visible', params: {transitionParams: '.4s cubic-bezier(0.86, 0, 0.07, 1)', height: '*'}}
    :{value: 'hidden', params: {transitionParams: '.4s cubic-bezier(0.86, 0, 0.07, 1)', height: '0'}}"
    >
      <li class="sublevel-nav__item" *ngFor="let item of data.items">
        <a class="sublevel-nav__link"
        (click)="handleClick(item)"
        *ngIf="item.items && item.items.length > 0"
        [ngClass]="getActiveClass(item)"
        >

          <i class="bx bxs-circle sublevel-nav__icon"></i>
          <span class="sublevel-nav__text" *ngIf="collapsed">{{item.label}}</span>
          <i *ngIf="item.items && collapsed"
          class="sublevel-nav__menu-collapse-icon"
          [ngClass]="!item.expanded ? 'bx bx-chevron-right':'bx bx-chevron-down'"
          ></i>
        </a>

        <a class="sublevel-nav__link"
        *ngIf="!item.items || (item.items && item.items.length === 0)"
        [routerLink]="[item.routerLink]"
        routerLinkActive="active-sublevel"
        [routerLinkActiveOptions]="{exact: true}"
        >
          <i class="bx bxs-circle sublevel-nav__icon"></i>
          <span class="sublevel-nav__text " *ngIf="collapsed">{{item.label}}</span>
        </a>
        <div *ngIf="item.items && item.items.length > 0">
          <app-sublevel-menu
          [data]="item"
          [collapsed]="collapsed"
          [multiple]="multiple"
          [expanded]="item.expanded"
          >
          </app-sublevel-menu>
        </div>
      </li>
    </ul>

  `,
  styleUrls: ['./sidenav.component.scss'],
  animations: [

    trigger("submenu", [
      state("hidden", style({
        height: "0",
        overflow: "hidden"
      })),
      state("visible", style({
        height: "*"
      })),
      transition("visible <=> hidden", [style({overflow: "hidden"}),
        animate("{{transitionParams}}")]),
      transition("void => *", animate(0))
    ])
  ]

})
export class SublevelMenuComponent implements OnInit {

  @Input() public data: Sidenav = {
    routerLink: "",
    icon: "",
    label: "",
    items: []
  };

  @Input() public collapsed: boolean = false;
  @Input() public expanded: boolean | undefined;
  @Input() public multiple: boolean = false;

  constructor(
    private _router: Router
  ) { }

  ngOnInit(): void {

  }

  public handleClick(item:any):void {

    if(!this.multiple){

      if(this.data.items && this.data.items.length > 0){

        for(let modelItem of this.data.items){

          if(item !== modelItem && modelItem.expanded){

            modelItem.expanded = false;
          }
        }
      }
    }

    item.expanded = !item.expanded;
  }

  public getActiveClass(item: Sidenav): string{
    return item.expanded && this._router.url.includes(item.routerLink) ? "active-sublevel": "";
  }

}
