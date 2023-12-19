import { Component, OnInit, inject } from '@angular/core';
import { ProductsService } from '../../services/products.service';
import { Product } from '../../interfaces/product';
import { Category } from '../../interfaces/category';
import { environment } from 'src/environments/environment.development';

@Component({
  selector: 'app-list-products',
  templateUrl: './list-products.component.html',
  styleUrls: ['./list-products.component.scss']
})
export class ListProductsComponent implements OnInit {

  public pageNumber: number = 1;
  public listProducts: Array<Product> = [];
  public listCategories: Array<Category> = [];
  public urlApi: string = environment.domain;

  private _productsService = inject(ProductsService);

  ngOnInit(): void {

    this._productsService.getProducts();
    this._productsService.listProducts$.subscribe(result => {

      this.listProducts = result;
    })

    this._productsService.getCategories().subscribe(result => {

      if(result != null){
        this.listCategories = result.data;
      }

    })
  }

  public nextPage():void{

    this.pageNumber += 1;
    this._productsService.getProductsPage(this.pageNumber);
  }
  public previousPage():void{

    this.pageNumber -= 1;
    this._productsService.getProductsPage(this.pageNumber);
  }

  public searchProduct():void {

    const search = document.querySelector("#search_product") as HTMLInputElement;
    const select = document.querySelector("#select_category") as HTMLSelectElement;

    let searchProduct = {
      id_category: Number.parseInt(select.value),
      name_product: search.value
    }

    this._productsService.searchProduct(searchProduct);
  }

  get getService(){
    return this._productsService;
  }

}
