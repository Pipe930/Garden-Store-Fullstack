import { Component, OnInit, inject } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { AlertsService } from 'src/app/shared/services/alerts.service';
import { Router } from '@angular/router';
import { ValidatorService } from 'src/app/shared/services/validator.service';


@Component({
  selector: 'app-reset-password-confirm',
  templateUrl: './reset-password-confirm.component.html',
  styleUrls: ['./reset-password-confirm.component.scss']
})
export class ResetPasswordConfirmComponent implements OnInit {

  private uid: string = "";
  private token: string = "";

  private readonly _activate = inject(ActivatedRoute);
  private readonly _router = inject(Router);
  private readonly _builder = inject(FormBuilder);
  private readonly _authService = inject(AuthService);
  private readonly _alertService = inject(AlertsService);
  private readonly _validatorService = inject(ValidatorService);

  public messagePassword: Array<string> = [];
  public formResetPassword: FormGroup = this._builder.group({
    new_password: new FormControl("", [Validators.required, Validators.minLength(8), Validators.maxLength(32)]),
    re_new_password: new FormControl("", [Validators.required, Validators.minLength(8), Validators.maxLength(32)])
  }, {
    validators: this._validatorService.comparePasswords("password", "re_password")
  });

   ngOnInit(): void {
    this._activate.params.subscribe(params =>{
      this.uid = params["uid"];
      this.token = params["token"];
    });
   }

  public resetPassword():void{

    let formulario = this.formResetPassword.value;
    let json = {
      uid: this.uid,
      token: this.token,
      new_password: formulario.new_password,
      re_new_password: formulario.re_new_password
    }

    if(this.formResetPassword.invalid){

      this.formResetPassword.markAllAsTouched();
      return;
    }

    this._authService.resetPasswordConfirm(json).subscribe( (result) => {

      this._alertService.success("Contraseña Cambiada", "La contraseña a sido cambiada con exito");
      this._router.navigate(['auth/login']);
    }, (error) => {

      if(error.error["password"]){

        this.messagePassword = error.error["password"];
      }

      this._alertService.error("Error", "No se pudo cambiar la contraseña correctamente")
    })

  }

  get new_password(){
    return this.formResetPassword.controls["new_password"];
  }

  get re_new_password(){
    return this.formResetPassword.controls["re_new_password"];
  }

}
