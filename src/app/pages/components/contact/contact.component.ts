import { Component, OnInit, inject } from '@angular/core';
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
export class ContactComponent implements OnInit {

  private _builder = inject(FormBuilder);
  private _pagesService = inject(PagesService);
  private _alertService = inject(AlertsService);
  private _validatorService = inject(ValidatorService);
  private _router = inject(Router);

  public formContact: FormGroup = this._builder.group({
    full_name: new FormControl("", [Validators.required, Validators.maxLength(40), Validators.minLength(4)]),
    email: new FormControl("", [Validators.required, this._validatorService.emailValidator, Validators.maxLength(255)]),
    message: new FormControl("", Validators.maxLength(255))
  });

  ngOnInit(): void {
    window.scrollTo({
      top: 0,
      behavior: 'smooth',
      left: 0
    });
  }

  public sendEmail():void{

    if(this.formContact.invalid){

      this.formContact.markAllAsTouched();
      return;
    }

    this._pagesService.sendEmail(this.formContact.value).subscribe( (result) => {

      this._alertService.success("Correo Enviado", "El correo se a enviado correctamente, te atendermos tu problema");
      this._router.navigate(['/home']);
    }, (error) => this._alertService.error("Error Envio", "El correo no se a enviado correctamente"))
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
