import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { AuthenticationService } from '../../services/authentication.service';
import { GlobalFuctionsService } from 'src/app/services/global-fuctions.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {

  public formRegister: FormGroup | any;
  public password_validated: boolean = false;

  constructor(
    private builder: FormBuilder,
    private service: AuthenticationService,
    private globalService: GlobalFuctionsService
  ) {

    this.formRegister = this.builder.group({
      first_name: new FormControl("", [Validators.required, Validators.maxLength(20), Validators.minLength(4)]),
      last_name: new FormControl("", [Validators.required, Validators.maxLength(20), Validators.minLength(4)]),
      username: new FormControl("", [Validators.required, Validators.maxLength(60), Validators.minLength(4)]),
      email: new FormControl("", [Validators.required, globalService.emailValidator, Validators.maxLength(255)]),
      password: new FormControl("", [Validators.required, Validators.minLength(8), Validators.maxLength(32)]),
      re_password: new FormControl("", [Validators.required, Validators.minLength(8), Validators.maxLength(32)])
    })
  }

  ngOnInit(): void {

  }

  public register():void{

    let formulario = this.formRegister.value;

    if(this.formRegister.valid){
      if(formulario.password === formulario.re_password){

        this.globalService.alertLoader();
        this.service.register(formulario);

      } else {
        this.password_validated = true;
      }
    } else {
      this.formRegister.markAllAsTouched();
    }

  }

  get first_name(){
    return this.formRegister.get("first_name");
  }

  get last_name(){
    return this.formRegister.get("last_name");
  }

  get username(){
    return this.formRegister.get("username");
  }

  get email(){
    return this.formRegister.get("email");
  }

  get password(){
    return this.formRegister.get("password");
  }

  get re_password(){
    return this.formRegister.get("re_password");
  }

  get get_servive(){
    return this.service;
  }
}
