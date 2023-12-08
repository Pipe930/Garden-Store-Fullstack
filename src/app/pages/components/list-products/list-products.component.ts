import { Component, OnInit } from '@angular/core';
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

  constructor(
    private service: ProductsService
  ) {
  }

  ngOnInit(): void {

    this.service.getProducts();
    this.service.listProducts$.subscribe(result => {
      this.listProducts = result;
    })

    this.service.getCategories().subscribe(result => {
      this.listCategories = result.data;
    })
  }

  public nextPage():void{

    this.pageNumber += 1;
    this.service.getProductsPage(this.pageNumber);
  }
  public previousPage():void{

    this.pageNumber -= 1;
    this.service.getProductsPage(this.pageNumber);
  }

  public searchProduct():void {

    const search = document.querySelector("#search_product") as HTMLInputElement;
    const select = document.querySelector("#select_category") as HTMLSelectElement;

    let searchProduct = {
      id_category: Number.parseInt(select.value),
      name_product: search.value
    }

    this.service.searchProduct(searchProduct);
  }

  get getService(){
    return this.service
  }

}
