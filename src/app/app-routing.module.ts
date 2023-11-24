import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ActivateComponent } from './authentication/components/activate/activate.component';
import { ResetPasswordConfirmComponent } from './authentication/components/reset-password-confirm/reset-password-confirm.component';
import { PageNotFoundComponent } from './components/page-not-found/page-not-found.component';


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
    loadChildren: () => import('./authentication/authentication.module').then(module => module.AuthenticationModule)
  },
  {
    path: "**",
    pathMatch: "full",
    component: PageNotFoundComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
