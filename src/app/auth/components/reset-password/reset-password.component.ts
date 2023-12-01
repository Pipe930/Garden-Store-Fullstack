import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { AlertsService } from 'src/app/shared/services/alerts.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-reset-password',
  templateUrl: './reset-password.component.html',
  styleUrls: ['./reset-password.component.scss']
})
export class ResetPasswordComponent implements OnInit {

  public formSendEmail: FormGroup;

  constructor(
    private builder: FormBuilder,
    private service: AuthService,
    private alert: AlertsService,
    private router: Router
  ) {
    this.formSendEmail = this.builder.group({
      email: new FormControl("", [Validators.required, Validators.email, Validators.maxLength(255)])
    })
  }

  ngOnInit(): void {

  }

  public sendEmail():void{

    if(this.formSendEmail.invalid){

      this.formSendEmail.markAllAsTouched();
      return;
    }

    this.service.resetPassword(this.formSendEmail.value).subscribe( (result) => {

      this.alert.success("Correo Enviado", "Le enviamos un correo con un link para resetear la contraseña");
      this.router.navigate(['auth/login']);
    }, (error) => this.alert.error("Error", "Error, no se pudo resetear la contraseña"))

  }

  get email(){
    return this.formSendEmail.controls["email"];
  }
}
