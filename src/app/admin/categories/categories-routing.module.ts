import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ListCategoriesComponent } from './list-categories/list-categories.component';
import { CreateCategoryComponent } from './create-category/create-category.component';

const routes: Routes = [
  {
    path: "list",
    component: ListCategoriesComponent
  },
  {
    path: "create",
    component: CreateCategoryComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CategoriesRoutingModule { }
