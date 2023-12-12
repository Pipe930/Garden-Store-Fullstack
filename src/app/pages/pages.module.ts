import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';

import { PagesRoutingModule } from './pages-routing.module';
import { PagesComponent } from './pages.component';
import { HomeComponent } from './components/home/home.component';
import { SharedModule } from '../shared/shared.module';
import { ContactComponent } from './components/contact/contact.component';
import { PagesService } from './services/pages.service';
import { ListProductsComponent } from './components/list-products/list-products.component';
import { ProductsService } from './services/products.service';
import { DetailProductComponent } from './components/detail-product/detail-product.component';


@NgModule({
  declarations: [
    PagesComponent,
    HomeComponent,
    ContactComponent,
    ListProductsComponent,
    DetailProductComponent
  ],
  imports: [
    CommonModule,
    PagesRoutingModule,
    SharedModule,
    ReactiveFormsModule,
    HttpClientModule
  ],
  providers: [
    PagesService,
    ProductsService
  ]
})
export class PagesModule { }
