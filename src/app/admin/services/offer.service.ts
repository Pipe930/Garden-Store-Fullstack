import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { CreateOffer, ResponseListOffer } from '../interfaces/offer';
import { environment } from 'src/environments/environment.development';
import { AuthService } from 'src/app/auth/services/auth.service';

@Injectable({
  providedIn: 'root'
})
export class OfferService {

  private readonly _http = inject(HttpClient);
  private readonly _authService = inject(AuthService);
  private urlApi = environment.url + "admin/offers/"

  public getAllOffers():Observable<ResponseListOffer>{

    return this._http.get<ResponseListOffer>(this.urlApi, {
      headers: new HttpHeaders({
        Authorization: "JWT " + this._authService.getToken()
      })
    });
  }

  public createOffer(formulario: CreateOffer):Observable<CreateOffer>{

    return this._http.post<CreateOffer>(this.urlApi, formulario, {
      headers: new HttpHeaders({
        Authorization: "JWT " + this._authService.getToken()
      })
    })
  }

}
