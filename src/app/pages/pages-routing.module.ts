import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PagesComponent } from './pages.component';
import { HomeComponent } from './components/home/home.component';
import { ContactComponent } from './components/contact/contact.component';
import { ListProductsComponent } from './components/list-products/list-products.component';
import { DetailProductComponent } from './components/detail-product/detail-product.component';
import { AccountComponent } from './components/account/account.component';
import { authGuard } from '../shared/guards/auth.guard';


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
      },
      {
        path: "account/:username",
        component: AccountComponent,
        canActivate: [authGuard]
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PagesRoutingModule { }
