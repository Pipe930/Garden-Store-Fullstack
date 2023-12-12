import { Component, OnInit } from '@angular/core';
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

  public product!: Product;
  public slug: string = "";
  public urlApi: string = environment.domain;
  public quantity: number = 1;

  constructor(
    private service: ProductsService,
    private route: ActivatedRoute
  ) {

    this.route.params.subscribe(params => {
      this.slug = params["slug"];
    });
  }

  ngOnInit(): void {

    this.service.getProduct(this.slug).subscribe(result => {
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
