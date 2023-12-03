import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { AlertsService } from 'src/app/shared/services/alerts.service';

@Component({
  selector: 'app-activate',
  templateUrl: './activate.component.html',
  styleUrls: ['./activate.component.scss']
})
export class ActivateComponent {

  private uid: string = "";
  private token: string = "";

  constructor(
    private activate: ActivatedRoute,
    private service: AuthService,
    private router: Router,
    private alert: AlertsService
  ) {
    this.activate.params.subscribe(params =>{
      this.uid = params["uid"];
      this.token = params["token"];
    })
   }

  public activateAcount():void{

    let info = {
      uid: this.uid,
      token: this.token
    }

    this.service.activateAcount(info).subscribe( (result) => {

      this.alert.success("Cuenta Activada", "La cuenta a sido activada con exito");
      this.router.navigate(['auth/login']);
    }, (error) => this.alert.error("Error", "La cuenta no a sido activada correctamente"));

  }
}
