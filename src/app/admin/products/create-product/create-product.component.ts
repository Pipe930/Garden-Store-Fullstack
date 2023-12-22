import { Component, ElementRef, OnInit, ViewChild, inject } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ProductService } from '../../services/product.service';
import { CategoryService } from '../../services/category.service';
import { Category } from '../../interfaces/category';
import { AlertsService } from 'src/app/shared/services/alerts.service';

@Component({
  selector: 'app-create-product',
  templateUrl: './create-product.component.html',
  styleUrls: ['./create-product.component.scss']
})
export class CreateProductComponent implements OnInit {

  private readonly _builder = inject(FormBuilder);
  private readonly _router = inject(Router);
  private readonly _productService = inject(ProductService);
  private readonly _categoryService = inject(CategoryService);
  private readonly _alertService = inject(AlertsService);

  @ViewChild('imageProduct') public imageProduct!: ElementRef;

  private imageBase64: string = "";
  public loadImage: boolean = false;
  public listCategories: Array<Category> = [];

  public formProduct: FormGroup = this._builder.group({

    title: new FormControl("", [Validators.required, Validators.maxLength(255)]),
    brand: new FormControl("", [Validators.required, Validators.maxLength(40)]),
    price: new FormControl(0, [Validators.required, Validators.min(1000), Validators.max(1000000)]),
    description: new FormControl("", Validators.maxLength(255)),
    category: new FormControl("", Validators.required),
    image: new FormControl("", Validators.required)
  });

  ngOnInit(): void {

    this._categoryService.getAllCategories().subscribe(result => {
      this.listCategories = result.data;
    })
  }

  get title_product(){
    return this.formProduct.controls["title"];
  }

  get brand_product(){
    return this.formProduct.controls["brand"];
  }

  get price_product(){
    return this.formProduct.controls["price"];
  }

  get image_product(){
    return this.formProduct.controls["image"];
  }

  get description_product(){
    return this.formProduct.controls["image"];
  }

  get category_product(){
    return this.formProduct.controls["category"];
  }


  public createProduct():void{

    if(this.formProduct.invalid){

      this.formProduct.markAllAsTouched();
      return
    }

    const formulario = {
      ...this.formProduct.value,
      image: this.imageBase64
    }

    this._productService.createProduct(formulario).subscribe(result => {

      this._alertService.success("Producto Creado", "El producto se a creado con exito");
      this._router.navigate(["/administration/products/list"]);
    }, (error) => this._alertService.error("Error", "Error, el producto no se creo con exito"));

  }

  public cambiarFoto(){

    this.loadImage = true;
    const elemento = this.imageProduct.nativeElement;

    if (elemento instanceof HTMLInputElement && elemento.files && elemento.files.length > 0) {
      const archivo = elemento.files[0];
      // Resto del código...
      const reader = new FileReader();
      reader.readAsDataURL(archivo);

      reader.onload = () => {
        this.loadImage = false;
        console.log('Carga terminada :D');
        this.imageBase64 = reader.result as string;
      }
      reader.onerror = () => {

      }
    }
  }

}
