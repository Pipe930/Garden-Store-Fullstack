import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { RouterModule } from '@angular/router';
import { ReactiveFormsModule } from '@angular/forms';

import { AuthRoutingModule } from './auth-routing.module';
import { AuthComponent } from './auth.component';
import { LoginComponent } from './components/login/login.component';
import { RegisterComponent } from './components/register/register.component';
import { ResetPasswordComponent } from './components/reset-password/reset-password.component';
import { ActivateComponent } from './components/activate/activate.component';
import { ResetPasswordConfirmComponent } from './components/reset-password-confirm/reset-password-confirm.component';

import { AuthService } from './services/auth.service';


@NgModule({
  declarations: [
    AuthComponent,
    LoginComponent,
    RegisterComponent,
    ResetPasswordComponent,
    ActivateComponent,
    ResetPasswordConfirmComponent
  ],
  imports: [
    CommonModule,
    AuthRoutingModule,
    HttpClientModule,
    RouterModule,
    ReactiveFormsModule
  ],
  providers: [
    AuthService
  ]
})
export class AuthModule { }
