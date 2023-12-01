import { Component, OnInit } from '@angular/core';
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
export class RegisterComponent implements OnInit {

  public formRegister: FormGroup;

  constructor(
    private builder: FormBuilder,
    private route: Router,
    private validator: ValidatorService,
    private service: AuthService,
    private alert: AlertsService
  ) {
    this.formRegister = this.builder.group({
      first_name: new FormControl("", [Validators.required, Validators.maxLength(20), Validators.minLength(4)]),
      last_name: new FormControl("", [Validators.required, Validators.maxLength(20), Validators.minLength(4)]),
      username: new FormControl("", [Validators.required, Validators.maxLength(60), Validators.minLength(4)]),
      email: new FormControl("", [this.validator.emailValidator, Validators.maxLength(255)]),
      password: new FormControl("", [Validators.required, Validators.minLength(8), Validators.maxLength(32)]),
      re_password: new FormControl("", [Validators.required, Validators.minLength(8), Validators.maxLength(32)])
    }, {
      validators: this.validator.comparePasswords("password", "re_password")
    });
  }

  public register():void{

    if(this.formRegister.invalid){
      this.formRegister.markAllAsTouched();
      return;
    }

    this.service.register(this.formRegister.value).subscribe( result => {

      this.alert.success("Registro Exitoso", "Su cuenta se a registrado correctamente, le enviamos un correo para activar su cuenta");
      this.route.navigate(['auth/login']);

    }, (error) => this.alert.error("Error Registro", "La cuenta no se registro correctamente"))
  }

  ngOnInit(): void {

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
