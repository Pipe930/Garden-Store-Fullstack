import { Injectable } from '@angular/core';
import { AbstractControl, FormGroup } from '@angular/forms';

@Injectable({
  providedIn: 'root'
})
export class ValidatorService {

  constructor() { }

  public emailValidator(control: AbstractControl): { [key: string]: any } | null {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,3}$/;
    const valid = emailRegex.test(control.value);
    return valid ? null : { invalidEmail: { valid: false } };
  }

  public comparePasswords(passwordKey: string, re_password: string) {

    return (group: FormGroup): {[key: string]: any} => {
      const password = group.controls[passwordKey];
      const confirmPassword = group.controls[re_password];

      if (password.value !== confirmPassword.value) {
        return { passordsDontMatch: true };
      }

      return {};
    }
  }
}
