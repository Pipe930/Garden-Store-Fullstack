import { Component, inject } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { AlertsService } from 'src/app/shared/services/alerts.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-reset-password',
  templateUrl: './reset-password.component.html',
  styleUrls: ['./reset-password.component.scss']
})
export class ResetPasswordComponent {

  private readonly _router = inject(Router);
  private readonly _builder = inject(FormBuilder);
  private readonly _authService = inject(AuthService);
  private readonly _alertService = inject(AlertsService);

  public formSendEmail: FormGroup = this._builder.group({
    email: new FormControl("", [Validators.required, Validators.email, Validators.maxLength(255)])
  });

  public sendEmail():void{

    if(this.formSendEmail.invalid){

      this.formSendEmail.markAllAsTouched();
      return;
    }

    this._authService.resetPassword(this.formSendEmail.value).subscribe( (result) => {

      this._alertService.success("Correo Enviado", "Le enviamos un correo con un link para resetear la contraseña");
      this._router.navigate(['auth/login']);
    }, (error) => this._alertService.error("Error", "Error, no se pudo resetear la contraseña"))

  }

  get email(){
    return this.formSendEmail.controls["email"];
  }
}
