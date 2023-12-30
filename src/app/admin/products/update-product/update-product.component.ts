import { Component, ElementRef, OnInit, ViewChild, inject } from '@angular/core';
import { ProductService } from '../../services/product.service';
import { CategoryService } from '../../services/category.service';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { Product } from '../../interfaces/product';
import { Category } from '../../interfaces/category';
import { AlertsService } from 'src/app/shared/services/alerts.service';

@Component({
  selector: 'app-update-product',
  templateUrl: './update-product.component.html',
  styleUrls: ['./update-product.component.scss']
})
export class UpdateProductComponent implements OnInit {

  private readonly _productService = inject(ProductService);
  private readonly _categoryService = inject(CategoryService);
  private readonly _alertService = inject(AlertsService);
  private readonly _router = inject(Router);
  private readonly _builder = inject(FormBuilder);
  private readonly _activeRouter = inject(ActivatedRoute);

  @ViewChild('imageProduct') public imageProduct!: ElementRef;
  @ViewChild('imagePreview') public imagePreview!: ElementRef;

  public formUpdateProduct: FormGroup = this._builder.group({

    title: new FormControl("", [Validators.required, Validators.maxLength(255)]),
    brand: new FormControl("", [Validators.required, Validators.maxLength(40)]),
    price: new FormControl(0, [Validators.required, Validators.min(1000), Validators.max(1000000)]),
    description: new FormControl("", Validators.maxLength(255)),
    category: new FormControl("", Validators.required),
    image: new FormControl("", Validators.required)
  });

  public product: Product = {
    id_product: 0,
    title: "",
    brand: "",
    stock: 0,
    price: 0,
    sold: 0,
    discount_price: 0,
    aviable: false,
    created: "",
    slug: "",
    image: "",
    description: "",
    category: "",
  };

  public productID: number = 0;
  public imageBase64: string = "";
  public listCategories: Array<Category> = [];
  public loadImage: boolean = false;

  ngOnInit(): void {

    this._activeRouter.params.subscribe(result => {
      this.productID = result["id"];
    });

    this._categoryService.getAllCategories().subscribe(result => {
      this.listCategories = result.data;
    })

    this._productService.getProduct(this.productID).subscribe(result => {

      this.product = result.data;
      this.formUpdateProduct.get("title")?.setValue(result.data.title);
      this.formUpdateProduct.get("brand")?.setValue(result.data.brand);
      this.formUpdateProduct.get("price")?.setValue(result.data.price);
      this.formUpdateProduct.get("description")?.setValue(result.data.description);
      this.formUpdateProduct.get("category")?.setValue(result.data.category);
      this.imageBase64 = result.data.image;
      this.formUpdateProduct.updateValueAndValidity();
    });
  }

  get title_product(){
    return this.formUpdateProduct.controls["title"];
  }

  get brand_product(){
    return this.formUpdateProduct.controls["brand"];
  }

  get price_product(){
    return this.formUpdateProduct.controls["price"];
  }

  get image_product(){
    return this.formUpdateProduct.controls["image"];
  }

  get description_product(){
    return this.formUpdateProduct.controls["image"];
  }

  get category_product(){
    return this.formUpdateProduct.controls["category"];
  }

  public updateProduct():void {

    if(this.formUpdateProduct.invalid){

      this.formUpdateProduct.markAllAsTouched();
      return;
    }

    const formulario = {
      ...this.formUpdateProduct.value,
      image: this.imageBase64
    }

    this._productService.updateProduct(formulario, this.product.id_product).subscribe(result => {
      console.log(result);
      this._alertService.success("Producto Actualizado", "El producto se a actualizado correctamente");
      this._router.navigate(["/administration/products/list"]);
    }, (error) => this._alertService.error("Error", "El producto no se a actualizado correctamente"))

  }

  public changeImage():void{

    this.loadImage = true;
    const imageProduct = this.imageProduct.nativeElement;
    const imagePreview = this.imagePreview.nativeElement;

    if (imageProduct instanceof HTMLInputElement && imageProduct.files && imageProduct.files.length > 0) {

      const archivo = imageProduct.files[0];
      const src = URL.createObjectURL(imageProduct.files[0]);

      imagePreview.src = src;

      const reader = new FileReader();
      reader.readAsDataURL(archivo);

      reader.onload = () => {
        this.loadImage = false;
        this.imageBase64 = reader.result as string;
      }
      return;
    }

    imagePreview.src = "/assets/imgs/upload-image_2023-04-11-023334_kxuh.png";
  }
}
