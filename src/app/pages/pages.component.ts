import { Component, OnInit, inject } from '@angular/core';
import { Navbar } from '../shared/interfaces/navbar';
import { AuthService } from '../auth/services/auth.service';

@Component({
  selector: 'app-pages',
  templateUrl: './pages.component.html',
  styleUrls: ['./pages.component.scss']
})
export class PagesComponent implements OnInit {

  public theme: boolean = false;
  public sessionActivate: boolean = false;

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

  public eventSession(event: boolean):void{
    this.sessionActivate = event;
  }

  public eventTheme(event: boolean):void{

    this.theme = event;

    if(!this.theme){
      localStorage.removeItem("theme");
      localStorage.setItem("theme", "light");
    } else {
      localStorage.removeItem("theme");
      localStorage.setItem("theme", "dark");
    }

  }

}
