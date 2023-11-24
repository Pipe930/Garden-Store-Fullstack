import { Component, OnInit } from '@angular/core';
import { AuthenticationService } from '../../services/authentication.service';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { GlobalFuctionsService } from 'src/app/services/global-fuctions.service';

@Component({
  selector: 'app-reset-password',
  templateUrl: './reset-password.component.html',
  styleUrls: ['./reset-password.component.scss']
})
export class ResetPasswordComponent implements OnInit {

  public formSendEmail: FormGroup | any;

  constructor(
    private builder: FormBuilder,
    private service: AuthenticationService,
    private globalService: GlobalFuctionsService
  ) {
    this.formSendEmail = this.builder.group({
      email: new FormControl("", [Validators.required, globalService.emailValidator, Validators.maxLength(255)])
    })
   }

  ngOnInit(): void {

  }

  public sendEmail():void{

    let formulario = this.formSendEmail.value;

    if(this.formSendEmail.valid){

      this.service.resetPassword(formulario);

    } else {
      this.formSendEmail.markAllAsTouched();
    }

  }

  get email(){
    return this.formSendEmail.get("email");
  }

}
