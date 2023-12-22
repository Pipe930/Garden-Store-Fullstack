import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AdminComponent } from './admin.component';
import { DashboardComponent } from './dashboard/dashboard.component';

const routes: Routes = [
  {
    path: "administration",
    component: AdminComponent,
    children: [
      {
        path: "dashboard",
        component: DashboardComponent
      },
      {
        path: "categories",
        loadChildren: () => import('./categories/categories.module').then(module => module.CategoriesModule)
      },
      {
        path: "products",
        loadChildren: () => import('./products/products.module').then(module => module.ProductsModule)
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AdminRoutingModule { }
