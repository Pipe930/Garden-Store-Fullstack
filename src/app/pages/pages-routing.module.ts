import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PagesComponent } from './pages.component';
import { HomeComponent } from './components/home/home.component';
import { ContactComponent } from './components/contact/contact.component';
import { ListProductsComponent } from './components/list-products/list-products.component';
import { DetailProductComponent } from './components/detail-product/detail-product.component';

const routes: Routes = [
  {
    path: "",
    component: PagesComponent,
    children: [
      {
        path: "home",
        component: HomeComponent
      },
      {
        path: "contact",
        component: ContactComponent
      },
      {
        path: "products",
        component: ListProductsComponent
      },
      {
        path: "product/:slug",
        component: DetailProductComponent
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PagesRoutingModule { }
