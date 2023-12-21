import { Component, inject } from '@angular/core';
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
export class LoginComponent {

  private readonly _router = inject(Router);
  private readonly _builder = inject(FormBuilder);
  private readonly _authService = inject(AuthService);
  private readonly _alertService = inject(AlertsService);
  private readonly _validatorService = inject(ValidatorService);

  public formLogin: FormGroup = this._builder.group({
    email: new FormControl("", [Validators.required, this._validatorService.emailValidator, Validators.maxLength(255)]),
    password: new FormControl("", [Validators.required, Validators.minLength(8), Validators.maxLength(32)])
  });

  public login():void{

    if(this.formLogin.invalid){

      this.formLogin.markAllAsTouched();
      return;
    }

    this._authService.login(this.formLogin.value).subscribe((result) => {

      this._alertService.success("Inicio Exitoso", "Se inicio sesion correctamente");
      let user = this._authService.getInfoUser();

      if(user.is_superuser){
        this._router.navigate(['administration/dashboard']);
      } else {
        this._router.navigate(['home']);
      }

    }, (error) => this._alertService.error("Error", "No se inicio sesion correctamente"))

  }

  get email(){
    return this.formLogin.controls["email"];
  }

  get password(){
    return this.formLogin.controls["password"];
  }
}
