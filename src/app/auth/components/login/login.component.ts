import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { AlertsService } from 'src/app/shared/services/alerts.service';
import { ValidatorService } from 'src/app/shared/services/validator.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  public formLogin: FormGroup;

  constructor(
    private builder: FormBuilder,
    private router: Router,
    private service: AuthService,
    private alert: AlertsService,
    private validator: ValidatorService
  ) {
    this.formLogin = this.builder.group({
      email: new FormControl("", [Validators.required, this.validator.emailValidator, Validators.maxLength(255)]),
      password: new FormControl("", [Validators.required, Validators.minLength(8), Validators.maxLength(32)])
    })
   }

  ngOnInit(): void {

  }

  public login():void{

    if(this.formLogin.invalid){

      this.formLogin.markAllAsTouched();
      return;
    }

    this.service.login(this.formLogin.value).subscribe((result) => {

      this.alert.success("Inicio Exitoso", "Se inicio sesion correctamente");
      this.router.navigate(['home']);
    }, (error) => this.alert.error("Error", "No se inicio sesion correctamente"))

  }

  get email(){
    return this.formLogin.controls["email"];
  }

  get password(){
    return this.formLogin.controls["password"];
  }
}
