import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Category, ResponseListCategory, ReponseCreateCategory, ReponseCategory } from '../interfaces/category';
import { environment } from 'src/environments/environment.development';
import { AuthService } from 'src/app/auth/services/auth.service';

@Injectable({
  providedIn: 'root'
})
export class CategoryService {

  public urlApi: string = `${environment.url}categories/`

  private readonly _http = inject(HttpClient);
  private readonly _authService = inject(AuthService);

  public getAllCategories():Observable<ResponseListCategory>{
    return this._http.get<ResponseListCategory>(this.urlApi);
  }


  public getCategory(id_category:number):Observable<ReponseCategory>{
    return this._http.get<ReponseCategory>(`${this.urlApi}category/${id_category}`);
  }

  public createCategory(category: Category):Observable<ReponseCreateCategory>{
    return this._http.post<ReponseCreateCategory>(`${this.urlApi}`, category, {
      headers: new HttpHeaders({
        "Content-Type": "application/json",
        Authorization: "JWT " + this._authService.getToken()
      })
    })
  }

  public updateCategory(category: Category, id_category: number):Observable<ReponseCreateCategory>{
    return this._http.put<ReponseCreateCategory>(`${this.urlApi}category/${id_category}`, category, {
      headers: new HttpHeaders({
        "Content-Type": "application/json",
        Authorization: "JWT " + this._authService.getToken()
      })
    })
  }
}
