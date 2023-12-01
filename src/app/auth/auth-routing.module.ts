import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthComponent } from './auth.component';
import { LoginComponent } from './components/login/login.component';
import { RegisterComponent } from './components/register/register.component';
import { ResetPasswordComponent } from './components/reset-password/reset-password.component';
import { ActivateComponent } from './components/activate/activate.component';
import { ResetPasswordConfirmComponent } from './components/reset-password-confirm/reset-password-confirm.component';

const routes: Routes = [
  {
    path: "activate/:uid/:token",
    component: ActivateComponent
  },
  {
    path: "password/reset/confirm/:uid/:token",
    component: ResetPasswordConfirmComponent
  },
  {
    path: "auth",
    component: AuthComponent,
    children: [
      {
        path: "login",
        component: LoginComponent
      },
      {
        path: "register",
        component: RegisterComponent
      },
      {
        path: "reset-password",
        component: ResetPasswordComponent
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AuthRoutingModule { }
