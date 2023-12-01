import { Injectable } from '@angular/core';
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

  constructor(
    private http: HttpClient
  ) { }

  public register(form: Register):Observable<RegisterResponse>{

    return this.http.post<RegisterResponse>(`${environment.url}auth/users/`, form, {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    })
  }

  public login(form: Login): Observable<LoginResponse>{

    return this.http.post<LoginResponse>(`${environment.url}auth/jwt/create/`, form, {
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

    return this.http.post(`${environment.url}auth/users/activation/`, body, {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    })
  }

  public resetPassword(form: ResetPassword):Observable<any>{

    return this.http.post(`${environment.url}auth/users/reset_password/`, form, {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    })
  }

  public resetPasswordConfirm(form: ResetPasswordConfirm): Observable<any>{

    return this.http.post(`${environment.url}auth/users/reset_password_confirm/`, form, {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    })
  }
}
