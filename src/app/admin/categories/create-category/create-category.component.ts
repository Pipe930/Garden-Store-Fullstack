import { Component, inject } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { CategoryService } from '../../services/category.service';
import { AlertsService } from 'src/app/shared/services/alerts.service';

@Component({
  selector: 'app-create-category',
  templateUrl: './create-category.component.html',
  styleUrls: ['./create-category.component.scss']
})
export class CreateCategoryComponent {

  private readonly _builder = inject(FormBuilder);
  private readonly _router = inject(Router);
  private readonly _categoryService = inject(CategoryService);
  private readonly _alertService = inject(AlertsService);

  public formCategory: FormGroup = this._builder.group({
    name_category: new FormControl("", [Validators.required, Validators.maxLength(20), Validators.minLength(4)])
  });

  public createCategory():void{

    if(this.formCategory.invalid){

      this.formCategory.markAllAsTouched();
      return;
    }

    this._categoryService.createCategory(this.formCategory.value).subscribe(result => {

      this._alertService.success("Categoria Creada", "La categoria se creo con exito");
      this._router.navigate(["/administration/categories/list"]);
    }, (error) => this._alertService.error("Error", "La categoria no se creo con exito"))
  }

  get name_category(){
    return this.formCategory.controls["name_category"];
  }

}
