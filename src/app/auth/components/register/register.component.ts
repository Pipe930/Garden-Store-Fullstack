import { Component, inject } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { ValidatorService } from 'src/app/shared/services/validator.service';
import { AuthService } from '../../services/auth.service';
import { AlertsService } from 'src/app/shared/services/alerts.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent {

  private _router = inject(Router);
  private _builder = inject(FormBuilder);
  private _authService = inject(AuthService);
  private _alertService = inject(AlertsService);
  private _validatorService = inject(ValidatorService);

  public messagePassword: Array<string> = [];
  public formRegister: FormGroup = this._builder.group({
    first_name: new FormControl("", [Validators.required, Validators.maxLength(20), Validators.minLength(4)]),
    last_name: new FormControl("", [Validators.required, Validators.maxLength(20), Validators.minLength(4)]),
    username: new FormControl("", [Validators.required, Validators.maxLength(60), Validators.minLength(4)]),
    email: new FormControl("", [this._validatorService.emailValidator, Validators.maxLength(255)]),
    password: new FormControl("", [Validators.required, Validators.minLength(8), Validators.maxLength(32)]),
    re_password: new FormControl("", [Validators.required, Validators.minLength(8), Validators.maxLength(32)])
  }, {
    validators: this._validatorService.comparePasswords("password", "re_password")
  });

  public register():void{

    if(this.formRegister.invalid){
      this.formRegister.markAllAsTouched();
      return;
    }

    this._authService.register(this.formRegister.value).subscribe( result => {

      this._alertService.success("Registro Exitoso", "Su cuenta se a registrado correctamente, le enviamos un correo para activar su cuenta");
      this._router.navigate(['auth/login']);

    }, (error) => {

      if(error.error["password"]){

        this.messagePassword = error.error["password"];
      }

      this._alertService.error("Error Registro", "La cuenta no se registro correctamente")
    })
  }

  get first_name(){
    return this.formRegister.controls["first_name"];
  }

  get last_name(){
    return this.formRegister.controls["last_name"];
  }

  get username(){
    return this.formRegister.controls["username"];
  }

  get email(){
    return this.formRegister.controls["email"];
  }

  get password(){
    return this.formRegister.controls["password"];
  }

  get re_password(){
    return this.formRegister.controls["re_password"];
  }

}
