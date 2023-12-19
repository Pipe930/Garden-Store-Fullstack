import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from 'src/environments/environment.development';
import { Register, RegisterResponse } from '../interfaces/register';
import { Observable, first, map } from 'rxjs';
import { Login, LoginResponse, UserInfo } from '../interfaces/login';
import { Activate } from '../interfaces/activate';
import { ResetPassword, ResetPasswordConfirm } from '../interfaces/reset-password';
import { jwtDecode } from 'jwt-decode';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private _http = inject(HttpClient);
  private urlApi: string = `${environment.url}auth/`;

  public getToken(){
    return sessionStorage.getItem("access") || null;
  }

  public getInfoUser(): UserInfo{

    let token = this.getToken();
    let tokenDecrypt = JSON.stringify(jwtDecode(token!));
    let userJson = JSON.parse(tokenDecrypt);

    const user: UserInfo = {
      email: userJson["email"],
      username: userJson["username"],
      is_staff: userJson["is_staff"],
      is_superuser: userJson["is_superuser"]
    }

    return user;

  }

  public register(form: Register):Observable<RegisterResponse>{

    return this._http.post<RegisterResponse>(`${this.urlApi}users/`, form, {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    })
  }

  public login(form: Login): Observable<LoginResponse>{

    return this._http.post<LoginResponse>(`${this.urlApi}jwt/login`, form, {
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

  public logout():Observable<any>{

    let refresh_token = sessionStorage.getItem("refresh");
    return this._http.post(`${this.urlApi}jwt/logout`, {refresh_token: refresh_token}, {
      headers: new HttpHeaders({
        Authorization: "JWT " + this.getToken(),
        'Content-Type': 'application/json'
      })
    })
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
