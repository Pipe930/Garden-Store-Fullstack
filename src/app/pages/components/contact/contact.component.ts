import { Component } from '@angular/core';
import { AlertsService } from 'src/app/shared/services/alerts.service';
import { PagesService } from '../../services/pages.service';
import { ValidatorService } from 'src/app/shared/services/validator.service';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-contact',
  templateUrl: './contact.component.html',
  styleUrls: ['./contact.component.scss']
})
export class ContactComponent {

  public formContact: FormGroup;

  constructor(
    private builder: FormBuilder,
    private service: PagesService,
    private alert: AlertsService,
    private validator: ValidatorService,
    private router: Router
  ) {
    this.formContact = this.builder.group({
      full_name: new FormControl("", [Validators.required, Validators.maxLength(40), Validators.minLength(4)]),
      email: new FormControl("", [Validators.required, this.validator.emailValidator, Validators.maxLength(255)]),
      message: new FormControl("", Validators.maxLength(255))
    })
  }

  public sendEmail():void{

    if(this.formContact.invalid){

      this.formContact.markAllAsTouched();
      return;
    }

    this.service.sendEmail(this.formContact.value).subscribe( (result) => {

      this.alert.success("Correo Enviado", "El correo se a enviado correctamente, te atendermos tu problema");
      this.router.navigate(['/home']);
    }, (error) => this.alert.error("Error Envio", "El correo no se a enviado correctamente"))
  }

  get full_name(){
    return this.formContact.controls["full_name"];
  }

  get email(){
    return this.formContact.controls["email"];
  }

  get message(){
    return this.formContact.controls["message"];
  }
}
