import { Component, OnInit, inject } from '@angular/core';
import { CategoryService } from '../../services/category.service';
import { Category, categoryColumns } from '../../interfaces/category';
import { Router } from '@angular/router';

@Component({
  selector: 'app-list-categories',
  templateUrl: './list-categories.component.html',
  styleUrls: ['./list-categories.component.scss']
})
export class ListCategoriesComponent implements OnInit {

  private readonly _router = inject(Router);

  public listCategories: Array<Category> = [];
  public columns = categoryColumns;

  private readonly _categoryService = inject(CategoryService);

  ngOnInit(): void {

    this._categoryService.getAllCategories().subscribe(result => {

      if(result){

        this.listCategories = result.data;
      }
    })
  }

  public editCategory(event: Category):void{

    this._router.navigate(["/administration/categories/update", event.id_category]);
  }

}
