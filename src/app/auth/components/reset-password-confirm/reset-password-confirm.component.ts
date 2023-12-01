import { Component, OnInit } from '@angular/core';
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

  public formResetPassword: FormGroup;
  private uid: string = "";
  private token: string = "";

  constructor(
    private activate: ActivatedRoute,
    private builder: FormBuilder,
    private service: AuthService,
    private alert: AlertsService,
    private validator: ValidatorService,
    private router: Router
  ) {
    this.activate.params.subscribe(params =>{
      this.uid = params["uid"];
      this.token = params["token"];
    });
    this.formResetPassword = this.builder.group({
      new_password: new FormControl("", [Validators.required, Validators.minLength(8), Validators.maxLength(32)]),
      re_new_password: new FormControl("", [Validators.required, Validators.minLength(8), Validators.maxLength(32)])
    }, {
      validators: this.validator.comparePasswords("password", "re_password")
    })
   }

  ngOnInit(): void {

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

    this.service.resetPasswordConfirm(json).subscribe( (result) => {

      this.alert.success("Contraseña Cambiada", "La contraseña a sido cambiada con exito");
      this.router.navigate(['auth/login']);
    }, (error) => this.alert.error("Error", "No se pudo cambiar la contraseña correctamente"))

  }

  get new_password(){
    return this.formResetPassword.controls["new_password"];
  }

  get re_new_password(){
    return this.formResetPassword.controls["re_new_password"];
  }

}
