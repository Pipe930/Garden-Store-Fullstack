import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { NavbarComponent } from './components/navbar/navbar.component';
import { FooterComponent } from './components/footer/footer.component';
import { CarouselComponent } from './components/carousel/carousel.component';

@NgModule({
  declarations: [
    NavbarComponent,
    FooterComponent,
    CarouselComponent
  ],
  exports: [
    NavbarComponent,
    FooterComponent,
    CarouselComponent
  ],
  imports: [
    CommonModule,
    RouterModule
  ]
})
export class SharedModule { }
