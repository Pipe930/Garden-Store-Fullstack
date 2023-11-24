import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { AuthenticationService } from '../../services/authentication.service';
import { GlobalFuctionsService } from 'src/app/services/global-fuctions.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  public formLogin: FormGroup | any;

  constructor(
    private builder: FormBuilder,
    private service: AuthenticationService,
    private globalService: GlobalFuctionsService
  ) {
    this.formLogin = this.builder.group({
      email: new FormControl("", [Validators.required, globalService.emailValidator, Validators.maxLength(255)]),
      password: new FormControl("", [Validators.required, Validators.minLength(8), Validators.maxLength(32)])
    })
   }

  ngOnInit(): void {
  }

  public login():void{

    let formulario = this.formLogin.value;

    if(this.formLogin.valid){

      this.globalService.alertLoader();
      this.service.login(formulario);

    } else {
      this.formLogin.markAllAsTouched();
    }

  }

  get email(){
    return this.formLogin.get("email");
  }

  get password(){
    return this.formLogin.get("password");
  }
}
