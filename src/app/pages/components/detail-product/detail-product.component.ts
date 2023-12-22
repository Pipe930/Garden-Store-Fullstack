import { Component, OnInit, inject } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Product } from '../../interfaces/product';
import { ProductsService } from '../../services/products.service';
import { environment } from 'src/environments/environment.development';

@Component({
  selector: 'app-detail-product',
  templateUrl: './detail-product.component.html',
  styleUrls: ['./detail-product.component.scss']
})
export class DetailProductComponent implements OnInit {

  public product: Product = {
    id_product: 0,
    title: "",
    brand: "",
    stock: 0,
    price: 0,
    discount_price: 0,
    aviable: false,
    created: "",
    slug: "",
    image: "",
    description: "",
    category: "",
  };

  public slug: string = "";
  public urlApi: string = environment.domain;
  public quantity: number = 1;

  private readonly _productsService = inject(ProductsService);
  private readonly _activated = inject(ActivatedRoute);

  ngOnInit(): void {

    this._activated.params.subscribe(params => {
      this.slug = params["slug"];
    });

    this._productsService.getProduct(this.slug).subscribe(result => {
      this.product = result.data;
    }, error => console.error(error))
  }

  public sumQuantity():void {

    if (this.product.stock >= this.quantity) {
      this.quantity += 1;
    }
  }

  public subQuantity():void {
    if (1 < this.quantity) {
      this.quantity -= 1;
    }
  }

}
