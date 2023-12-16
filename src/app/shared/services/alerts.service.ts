import { Injectable } from '@angular/core';
import Swal from 'sweetalert2';

@Injectable({
  providedIn: 'root'
})
export class AlertsService {

  public success(title: string, text: string):void{

    Swal.fire({
      title: title,
      text: text,
      icon: "success",
      timer: 5000
    })
  }

  public error(title: string, text: string):void{

    Swal.fire({
      title: title,
      text: text,
      icon: "error",
      timer: 5000
    })
  }
}
