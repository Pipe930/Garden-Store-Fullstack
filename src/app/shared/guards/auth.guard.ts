import { inject } from '@angular/core';
import { CanActivateFn } from '@angular/router';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/auth/services/auth.service';

export const authGuard: CanActivateFn = (route, state) => {

  const _router = inject(Router);
  const _authService = inject(AuthService);

  if(_authService.getToken()){
    return true
  }

  _router.navigate(["/auth/login"]);
  return false;
};
