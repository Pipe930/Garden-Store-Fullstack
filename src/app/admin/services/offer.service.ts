import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { CreateOffer, ResponseListOffer, ResponseOffer } from '../interfaces/offer';
import { environment } from 'src/environments/environment.development';
import { AuthService } from 'src/app/auth/services/auth.service';

@Injectable({
  providedIn: 'root'
})
export class OfferService {

  private readonly _http = inject(HttpClient);
  private readonly _authService = inject(AuthService);
  private urlApi = environment.url + "admin/"

  public getAllOffers():Observable<ResponseListOffer>{

    return this._http.get<ResponseListOffer>(`${this.urlApi}offers/`, {
      headers: new HttpHeaders({
        Authorization: "JWT " + this._authService.getToken()
      })
    });
  }

  public createOffer(offer: CreateOffer):Observable<CreateOffer>{

    return this._http.post<CreateOffer>(`${this.urlApi}offers/`, offer, {
      headers: new HttpHeaders({
        Authorization: "JWT " + this._authService.getToken()
      })
    })
  }

  public getOffer(id: number):Observable<ResponseOffer>{
    return this._http.get<ResponseOffer>(`${this.urlApi}offer/${id}`, {
      headers: new HttpHeaders({
        Authorization: "JWT " + this._authService.getToken()
      })
    });
  }

  public updateOffer(offer: CreateOffer, id: number):Observable<CreateOffer>{
    return this._http.put<CreateOffer>(`${this.urlApi}offer/${id}`, offer, {
      headers: new HttpHeaders({
        Authorization: "JWT " + this._authService.getToken()
      })
    })
  }

}
