import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from 'src/environments/environment.development';
import { Register, RegisterResponse } from '../interfaces/register';
import { Observable, first, map } from 'rxjs';
import { Login, LoginResponse } from '../interfaces/login';
import { Activate } from '../interfaces/activate';
import { ResetPassword, ResetPasswordConfirm } from '../interfaces/reset-password';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private _http = inject(HttpClient);
  private urlApi: string = `${environment.url}auth/`;

  public register(form: Register):Observable<RegisterResponse>{

    return this._http.post<RegisterResponse>(`${this.urlApi}users/`, form, {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    })
  }

  public login(form: Login): Observable<LoginResponse>{

    return this._http.post<LoginResponse>(`${this.urlApi}jwt/create/`, form, {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    }).pipe(
      map(user => {

        if(user && user.access){
          sessionStorage.setItem("access", user.access);
          sessionStorage.setItem("refresh", user.refresh);
        }

        return user
      })
    ).pipe(first())
  }

  public activateAcount(body: Activate):Observable<any>{

    return this._http.post(`${this.urlApi}users/activation/`, body, {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    })
  }

  public resetPassword(form: ResetPassword):Observable<any>{

    return this._http.post(`${this.urlApi}users/reset_password/`, form, {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    })
  }

  public resetPasswordConfirm(form: ResetPasswordConfirm): Observable<any>{

    return this._http.post(`${this.urlApi}users/reset_password_confirm/`, form, {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    })
  }
}
