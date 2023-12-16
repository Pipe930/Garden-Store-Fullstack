import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';

import { CategoriesRoutingModule } from './categories-routing.module';
import { ListCategoriesComponent } from './list-categories/list-categories.component';
import { SharedModule } from 'src/app/shared/shared.module';
import { CreateCategoryComponent } from './create-category/create-category.component';


@NgModule({
  declarations: [
    ListCategoriesComponent,
    CreateCategoryComponent
  ],
  imports: [
    CommonModule,
    CategoriesRoutingModule,
    SharedModule,
    ReactiveFormsModule
  ]
})
export class CategoriesModule { }
