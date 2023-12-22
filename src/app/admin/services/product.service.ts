import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment.development';
import { ResponseListProduct, createProduct } from '../interfaces/product';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AuthService } from 'src/app/auth/services/auth.service';

@Injectable({
  providedIn: 'root'
})
export class ProductService {

  public urlApi: string = `${environment.url}products/`;

  private readonly _http = inject(HttpClient);
  private readonly _authService = inject(AuthService);

  constructor() { }

  public getAllProducts():Observable<ResponseListProduct>{

    return this._http.get<ResponseListProduct>(this.urlApi, {

      headers: new HttpHeaders({
        Authorization: "JWT " + this._authService.getToken()
      })
    });
  }

  public createProduct(form: createProduct):Observable<any>{

    return this._http.post<any>(this.urlApi, form, {
      headers: new HttpHeaders({
        Authorization: "JWT " + this._authService.getToken()
      })
    })
  }
}
