import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { environment } from 'src/environments/environment.development';
import { Observable, catchError, throwError } from 'rxjs';
import { User } from '../interfaces/user';
import { AuthService } from 'src/app/auth/services/auth.service';
import { LoginResponse } from 'src/app/auth/interfaces/login';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  private _http = inject(HttpClient);
  private _authService = inject(AuthService);
  private urlApi: string = `${environment.url}auth/`;

  public getUser():Observable<User>{
    return this._http.get<User>(`${this.urlApi}users/me/`, {
      headers: new HttpHeaders({
        Authorization: "JWT " + this._authService.getToken()
      })
    });
  }

  public getRefreshToken():Observable<LoginResponse>{

    let tokenRefresh = sessionStorage.getItem("refresh");
    return this._http.post<LoginResponse>(`${this.urlApi}jwt/refresh`, {refresh: tokenRefresh});
  }
}
