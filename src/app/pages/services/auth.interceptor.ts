import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
  HttpErrorResponse
} from '@angular/common/http';
import { Observable, catchError, switchMap, throwError } from 'rxjs';
import { UserService } from './user.service';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  constructor(
    private _userService: UserService
  ) {}

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {

    if(request.headers.get("Authorization")){

      return next.handle(request).pipe(
        catchError( (err: HttpErrorResponse) => {

          if(err.status === 401){

            return this._userService.getRefreshToken().pipe(

              switchMap(
                (result: any) => {

                  sessionStorage.setItem("access", result.access);
                  sessionStorage.setItem("refresh", result.refresh);

                  return next.handle(request.clone({
                    setHeaders: {
                      Authorization: "JWT " + result.access
                    }
                  }));
                }
              )
            )

          }

          return throwError(() => err);
        }
      ));
    }


    return next.handle(request);
  }
}
