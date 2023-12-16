import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Category, ResponseListCategory, ReponseCategory } from '../interfaces/category';
import { environment } from 'src/environments/environment.development';

@Injectable({
  providedIn: 'root'
})
export class CategoryService {

  public urlApi: string = `${environment.url}categories/`

  private _http = inject(HttpClient);

  public getAllCategories():Observable<ResponseListCategory>{
    return this._http.get<ResponseListCategory>(this.urlApi);
  }

  public createCategory(category: Category):Observable<ReponseCategory>{
    return this._http.post<ReponseCategory>(`${this.urlApi}`, category, {
      headers: new HttpHeaders({
        "Content-Type": "application/json"
      })
    })
  }
}
