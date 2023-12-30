import { Component, inject, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormControl, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { CategoryService } from '../../services/category.service';
import { AlertsService } from 'src/app/shared/services/alerts.service';
import { Category } from '../../interfaces/category';

@Component({
  selector: 'app-update-category',
  templateUrl: './update-category.component.html',
  styleUrls: ['./update-category.component.scss']
})
export class UpdateCategoryComponent implements OnInit {

  public id_category: number = 0;
  public category!: Category;

  private readonly _builder = inject(FormBuilder);
  private readonly _router = inject(Router);
  private readonly _activeRoute = inject(ActivatedRoute);
  private readonly _categoryService = inject(CategoryService);
  private readonly _alertService = inject(AlertsService);

  public formUpdateCategory: FormGroup = this._builder.group({
    name_category: new FormControl("", [Validators.required, Validators.maxLength(40), Validators.minLength(4)])
  })

  public updateCategory():void{

    if(this.formUpdateCategory.invalid){

      this.formUpdateCategory.markAllAsTouched();

      return;
    }

    const form = this.formUpdateCategory.value;

    let category = {

      id_category: this.id_category,
      name_category: form.name_category
    }

    this._categoryService.updateCategory(category, this.id_category).subscribe(result => {

      this._alertService.success("Categoria Actualizada", "La categoria se actualizo con exito");
      this._router.navigate(["/administration/categories/list"]);
    }, error => this._alertService.error("Error", "No se actualizo la cateogria"))
  }

  ngOnInit(): void {
    this._activeRoute.params.subscribe(result => {
      this.id_category = result["id"];
    });

    this._categoryService.getCategory(this.id_category).subscribe(result => {
      this.category = result.data;
      this.formUpdateCategory.get("name_category")?.setValue(result.data.name_category);
      this.formUpdateCategory.updateValueAndValidity();
    });
  }


  get name_category(){
    return this.formUpdateCategory.controls["name_category"];
  }

}
