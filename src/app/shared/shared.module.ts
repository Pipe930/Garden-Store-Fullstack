import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { CdkMenuModule } from '@angular/cdk/menu';
import { OverlayModule } from '@angular/cdk/overlay';

import { NavbarComponent } from './components/navbar/navbar.component';
import { FooterComponent } from './components/footer/footer.component';
import { CarouselComponent } from './components/carousel/carousel.component';
import { SidenavComponent } from './components/sidenav/sidenav.component';
import { SublevelMenuComponent } from './components/sidenav/sublevel-menu.component';
import { TableComponent } from './components/table/table.component';
import { HeaderComponent } from './components/header/header.component';

@NgModule({
  declarations: [
    NavbarComponent,
    FooterComponent,
    CarouselComponent,
    SidenavComponent,
    SublevelMenuComponent,
    TableComponent,
    HeaderComponent,
  ],
  exports: [
    NavbarComponent,
    FooterComponent,
    CarouselComponent,
    SidenavComponent,
    TableComponent,
    HeaderComponent
  ],
  imports: [
    CommonModule,
    RouterModule,
    CdkMenuModule,
    OverlayModule,
  ]
})
export class SharedModule { }
