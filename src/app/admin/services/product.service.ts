import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment.development';
import { Product, ResponseListProduct, ResponseProduct, createProduct } from '../interfaces/product';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AuthService } from 'src/app/auth/services/auth.service';

@Injectable({
  providedIn: 'root'
})
export class ProductService {

  public urlApi: string = `${environment.url}admin/`;

  private readonly _http = inject(HttpClient);
  private readonly _authService = inject(AuthService);

  constructor() { }

  public getAllProducts():Observable<ResponseListProduct>{

    return this._http.get<ResponseListProduct>(`${this.urlApi}products/`, {

      headers: new HttpHeaders({
        Authorization: "JWT " + this._authService.getToken()
      })
    });
  }

  public createProduct(form: createProduct):Observable<any>{

    return this._http.post<any>(`${this.urlApi}products/`, form, {
      headers: new HttpHeaders({
        Authorization: "JWT " + this._authService.getToken()
      })
    })
  }

  public getProduct(id: number):Observable<ResponseProduct>{

    return this._http.get<ResponseProduct>(`${this.urlApi}product/${id}`, {
      headers: new HttpHeaders({
        Authorization: "JWT " + this._authService.getToken()
      })
    })
  }

  public updateProduct(product: createProduct, id: number):Observable<createProduct>{

    return this._http.put<createProduct>(`${this.urlApi}product/${id}`, product, {
      headers: new HttpHeaders({
        Authorization: "JWT " + this._authService.getToken()
      })
    })
  }
}
