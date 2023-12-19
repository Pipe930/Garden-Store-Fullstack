import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PageNotFoundComponent } from './shared/components/page-not-found/page-not-found.component';
import { isAdminGuard } from './shared/guards/is-admin.guard';

const routes: Routes = [
  {
    path: "",
    redirectTo: "home",
    pathMatch: "full"
  },
  {
    path: "",
    loadChildren: () => import('./auth/auth.module').then(module => module.AuthModule)
  },
  {
    path: "",
    loadChildren: () => import('./pages/pages.module').then(module => module.PagesModule)
  },
  {
    path: "",
    loadChildren: () => import('./admin/admin.module').then(module => module.AdminModule),
    canActivate: [isAdminGuard]
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
