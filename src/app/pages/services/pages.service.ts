import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { SendEmail, SendEmailResponse } from '../interfaces/send-email';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment.development';

@Injectable({
  providedIn: 'root'
})
export class PagesService {

  constructor(
    private http: HttpClient
  ) { }

  public sendEmail(form: SendEmail): Observable<SendEmailResponse>{

    return this.http.post<SendEmailResponse>(`${environment.url}users/sendEmail/`, form, {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    });

  }
}
