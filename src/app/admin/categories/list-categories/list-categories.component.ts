import { Component, OnInit, inject } from '@angular/core';
import { CategoryService } from '../../services/category.service';
import { Category, categoryColumns } from '../../interfaces/category';

@Component({
  selector: 'app-list-categories',
  templateUrl: './list-categories.component.html',
  styleUrls: ['./list-categories.component.scss']
})
export class ListCategoriesComponent implements OnInit {

  public listCategories: Array<Category> = [];
  public columns = categoryColumns;

  private _categoryService = inject(CategoryService);

  ngOnInit(): void {

    this._categoryService.getAllCategories().subscribe(result => {

      if(result){

        this.listCategories = result.data;
      }
    })
  }

}
