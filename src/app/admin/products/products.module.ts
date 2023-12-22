import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ProductsRoutingModule } from './products-routing.module';
import { ListProductsComponent } from './list-products/list-products.component';
import { SharedModule } from 'src/app/shared/shared.module';
import { CreateProductComponent } from './create-product/create-product.component';
import { ReactiveFormsModule } from '@angular/forms';


@NgModule({
  declarations: [
    ListProductsComponent,
    CreateProductComponent
  ],
  imports: [
    CommonModule,
    ProductsRoutingModule,
    SharedModule,
    ReactiveFormsModule
  ]
})
export class ProductsModule { }
