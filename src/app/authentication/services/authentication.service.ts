import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';
import { Register } from '../interfaces/register';
import { Activate, ResetPassword, ResetPasswordConfirm } from '../interfaces/activate';
import { Login, LoginResponse } from '../interfaces/login';
import { environment } from 'src/environments/environment.development';
import Swal from 'sweetalert2';
import { first, map } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {

  public message_error_password: string[] = [];
  public message_error_username: string = "";
  public message_error_email: string = "";

  constructor(
    private http: HttpClient,
    private router: Router
  ) { }

  public register(form: Register):void{

    this.http.post(`${environment.url}auth/users/`, form, {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    }).subscribe(result => {
      if(result){

        Swal.fire({
          title: "Registro Exitoso",
          html: `
          <p>Su cuenta se a registrado correctamente</p> <br>
          <p><strong>Le enviamos un correo para activar su cuenta</strong></p>
          `,
          icon: "success",
          timer: 10000
        });
        this.router.navigate(["auth/login"]);
      }
    }, error => {
      if(error.error.password){
        for (let message of error.error.password) {
          this.message_error_password = [];
          this.message_error_password.push(message);
        }
      }

      if(error.error.username){
        this.message_error_username = "Ya existe un usuario con este username";
      }

      if(error.error.email){
        this.message_error_email = "Ya existe un usuario con este correo";
      }

      Swal.fire({
        title: "Error en Registro",
        text: "El usuario no se a registrado correctamente",
        icon: "error",
        timer: 5000
      });
    })
  }

  public activateAcount(info: Activate):void{

    this.http.post(`${environment.url}auth/users/activation/`, info, {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    }).subscribe(result =>{
      Swal.fire({
        title: "Cuenta Activada",
        text: "Su cuenta a sido activada con exito",
        icon: "success",
        timer: 5000
      })
      this.router.navigate(["auth/login"]);
    }, error => {
      Swal.fire({
        title: "Error de Activacion",
        text: "Error, no se puedo activar la cuenta",
        icon: "error",
        timer: 5000
      })
    })
  }

  public login(form: Login):void{

    this.http.post<LoginResponse>(`${environment.url}auth/jwt/create/`, form, {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    }).pipe(

      map(user => {

        if(user && user.access){
          sessionStorage.setItem('access', user.access);
          sessionStorage.setItem('refresh', user.refresh);
        }

        return user;
      })

    ).pipe(first()).subscribe(result => {

      if(result){
        Swal.fire({
          toast: true,
          position: "top-end",
          timerProgressBar: true,
          title: "Inicio Sesion Exitoso",
          icon: "success",
          timer: 5000
        })
      }
    }, error => {

      Swal.fire({
        title: "Error Inicio Sesion",
        text: "Error, no se inicio sesion correctamente",
        icon: "error",
        timer: 5000
      })
    })
  }

  public resetPassword(form: ResetPassword):void {

    this.http.post(`${environment.url}auth/users/reset_password/`, form, {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    }).subscribe(result => {

      Swal.fire({
        title: "Correo Enviado",
        text: "Te enviamos un correo con un link para que cambies la contraseña",
        icon: "success",
        timer: 5000
      });
      this.router.navigate(["auth/login"]);
    }, error => {

      Swal.fire({
        title: "Error",
        text: "El correo que proporcionaste no existe",
        icon: "error",
        timer: 5000
      });
    })
  }

  public resetPasswordConfirm(form: ResetPasswordConfirm):void{

    this.http.post(`${environment.url}auth/users/reset_password_confirm/`, form, {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    }).subscribe(result => {

      Swal.fire({
        title: "Contraseña Cambiada",
        text: "Su contraseña se cambio con exito",
        icon: "success",
        timer: 5000
      });
      this.router.navigate(["auth/login"]);
    }, error => {

      if(error.error.password){
        for (let message of error.error.password) {
          this.message_error_password = [];
          this.message_error_password.push(message);
        }
      }
    })
  }
}
