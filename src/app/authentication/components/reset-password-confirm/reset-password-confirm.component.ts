import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { AuthenticationService } from '../../services/authentication.service';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { GlobalFuctionsService } from 'src/app/services/global-fuctions.service';

@Component({
  selector: 'app-reset-password-confirm',
  templateUrl: './reset-password-confirm.component.html',
  styleUrls: ['./reset-password-confirm.component.scss']
})
export class ResetPasswordConfirmComponent implements OnInit {

  private uid: string = "";
  private token: string = "";
  public formResetPassword: FormGroup | any;
  public password_validated: boolean = false;

  constructor(
    private service: AuthenticationService,
    private route: ActivatedRoute,
    private builder: FormBuilder,
    private globalService: GlobalFuctionsService
  ) {

    this.route.params.subscribe(params =>{
      this.uid = params["uid"];
      this.token = params["token"];
    });
    this.formResetPassword = this.builder.group({
      new_password: new FormControl("", [Validators.required, Validators.minLength(8), Validators.maxLength(32)]),
      re_new_password: new FormControl("", [Validators.required, Validators.minLength(8), Validators.maxLength(32)])
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

    if(this.formResetPassword.valid){

      if(formulario.new_password === formulario.re_new_password) {

        this.service.resetPasswordConfirm(json);
      } else {

        this.password_validated = true;
      }
    } else {

      this.formResetPassword.markAllAsTouched();
    }
  }

  get new_password(){
    return this.formResetPassword.get("new_password");
  }

  get re_new_password(){
    return this.formResetPassword.get("re_new_password");
  }

  get get_service(){
    return this.service;
  }
}
