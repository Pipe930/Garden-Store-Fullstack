import { Component, OnInit, inject } from '@angular/core';
import { Product, productColumns } from '../../interfaces/product';
import { ProductService } from '../../services/product.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-list-products',
  templateUrl: './list-products.component.html',
  styleUrls: ['./list-products.component.scss']
})
export class ListProductsComponent implements OnInit {

  public listProducts: Array<Product> = [];
  public columns = productColumns;

  private readonly _productService = inject(ProductService);
  private readonly _router = inject(Router);

  ngOnInit(): void {

    this._productService.getAllProducts().subscribe(result => {

      if(result){

        this.listProducts = result.data;
      }
    })
  }

  public editProduct(product: Product):void{

    this._router.navigate(['/administration/products/update', product.id_product]);
  }

}
