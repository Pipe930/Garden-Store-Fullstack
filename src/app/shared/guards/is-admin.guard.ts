import { inject } from '@angular/core';
import { CanActivateFn } from '@angular/router';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/auth/services/auth.service';

export const isAdminGuard: CanActivateFn = (route, state) => {

  const _router = inject(Router);
  const _authService = inject(AuthService);

  if(_authService.getToken() == null){

    _router.navigate(["/auth/login"]);
    return false;
  }

  if(!_authService.getInfoUser().is_superuser){

    _router.navigate(["/auth/login"]);
    return false;
  }

  return true;
};
