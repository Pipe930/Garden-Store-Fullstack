import { Component, HostListener, OnInit } from '@angular/core';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {

  public canShowSearch: boolean = false;

  ngOnInit(): void {
    this.checkCanShowSearch(window.innerWidth);
  }

  @HostListener('window:resize', ['$event'])
  onResize(event: any){
    this.checkCanShowSearch(window.innerWidth);
  }

  public checkCanShowSearch(innerWidth: number):void {

    if(innerWidth < 845){

      this.canShowSearch = true;
    } else {

      this.canShowSearch = false;
    }
  }

}
