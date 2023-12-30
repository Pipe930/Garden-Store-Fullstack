import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ListProductsComponent } from './list-products/list-products.component';
import { CreateProductComponent } from './create-product/create-product.component';
import { UpdateProductComponent } from './update-product/update-product.component';

const routes: Routes = [
  {
    path: "list",
    component: ListProductsComponent
  },
  {
    path: "create",
    component: CreateProductComponent
  },
  {
    path: "update/:id",
    component: UpdateProductComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ProductsRoutingModule { }
