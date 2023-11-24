import { Injectable } from '@angular/core';
import { AbstractControl } from '@angular/forms';
import Swal from 'sweetalert2';

@Injectable({
  providedIn: 'root'
})
export class GlobalFuctionsService {

  constructor() { }

  public emailValidator(control: AbstractControl): { [key: string]: any } | null {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    const valid = emailRegex.test(control.value);
    return valid ? null : { invalidEmail: { valid: false } };
  }

  public alertLoader():void{
    Swal.fire({
      title: "Mohon Funggu !",
      text: "Procesando...",
      allowOutsideClick: false,
      showConfirmButton: false,
      willOpen: () => {
        Swal.showLoading();
      }
    })
  }
}
