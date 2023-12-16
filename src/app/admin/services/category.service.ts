import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ResponseCategory } from '../interfaces/category';
import { environment } from 'src/environments/environment.development';

@Injectable({
  providedIn: 'root'
})
export class CategoryService {

  public urlApi: string = `${environment.url}categories/`

  private _http = inject(HttpClient);

  public getAllCategories():Observable<ResponseCategory>{
    return this._http.get<ResponseCategory>(this.urlApi);
  }
}
