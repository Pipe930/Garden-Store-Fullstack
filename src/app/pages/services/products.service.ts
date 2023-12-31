import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { Product, ResponseProduct, ResponseProducts, SearchProduct } from '../interfaces/product';
import { environment } from 'src/environments/environment.development';
import { ResponseCategories } from '../interfaces/category';

@Injectable({
  providedIn: 'root'
})
export class ProductsService {

  public listProducts$ = new BehaviorSubject<Array<Product>>([]);
  public disableNext: boolean = false;
  public disablePrevious: boolean = false;
  public url: string = `${environment.url}products/`

  constructor(
    private http: HttpClient
  ) { }

  public getProducts():void {

    this.http.get<ResponseProducts>(this.url).subscribe( result => {

      if(result != null){

        this.listProducts$.next(result.results);
      } else {

        this.disableNext = true;
        this.disablePrevious = true;
      }

    });
  }

  public getProductsPage(page: number):void{
    this.http.get<ResponseProducts>(`${this.url}?page=${page}`).subscribe( result => {

      this.validatedPage(result.next, result.previous);
      this.listProducts$.next(result.results);
    });
  }

  public searchProduct(search: SearchProduct):void{

    this.http.post<ResponseProducts>(`${this.url}search`, search, {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    }).subscribe(result => {

      this.validatedPage(result.next, result.previous);
      this.listProducts$.next(result.results);
    })
  }

  public getProduct(slug: string):Observable<ResponseProduct>{
    return this.http.get<ResponseProduct>(`${this.url}detail/product/${slug}`);
  }

  public getCategories():Observable<ResponseCategories>{

    return this.http.get<ResponseCategories>(`${environment.url}categories/`);
  }

  private validatedPage(next: string | undefined, previous: string | undefined):void{

    if(next == undefined){
      this.disableNext = true;
    } else {
      this.disableNext = false;
    }

    if(previous == undefined){
      this.disablePrevious = true;
    } else {
      this.disablePrevious = false;
    }

  };

}
