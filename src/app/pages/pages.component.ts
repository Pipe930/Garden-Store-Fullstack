import { Component, OnInit } from '@angular/core';
import { Navbar } from '../shared/interfaces/navbar';

@Component({
  selector: 'app-pages',
  templateUrl: './pages.component.html',
  styleUrls: ['./pages.component.scss']
})
export class PagesComponent implements OnInit {

  public theme: boolean = false;
  public sessionActivate: boolean = false;

  constructor() {}

  // The Icons are found on the page https://boxicons.com/
  public listObjectsNavbar: Array<Navbar> = [
    {
      name: "Productos",
      link: "/products",
      icon: "bx bxs-shopping-bag"
    },
    {
      name: "Ofertas",
      link: "/offers",
      icon: "bx bxs-offer"
    },
    {
      name: "Blog",
      link: "/blog",
      icon: "bx bxl-blogger"
    }
  ];

  ngOnInit(): void {

    if(sessionStorage.getItem("access") || sessionStorage.getItem("refresh")){
      this.sessionActivate = true;
    } else {
      this.sessionActivate = false;
    }

  }

  public eventTheme(event: boolean):void{
    this.theme = event;
  }

}
