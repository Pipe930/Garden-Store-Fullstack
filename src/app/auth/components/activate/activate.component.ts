import { Component, inject, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { AlertsService } from 'src/app/shared/services/alerts.service';

@Component({
  selector: 'app-activate',
  templateUrl: './activate.component.html',
  styleUrls: ['./activate.component.scss']
})
export class ActivateComponent implements OnInit {

  private uid: string = "";
  private token: string = "";

  private readonly _activate = inject(ActivatedRoute);
  private readonly _authService = inject(AuthService);
  private readonly _router = inject(Router);
  private readonly _alertService = inject(AlertsService);

  ngOnInit(): void {

    this._activate.params.subscribe(params =>{
      this.uid = params["uid"];
      this.token = params["token"];
    })
  }

  public activateAcount():void{

    let info = {
      uid: this.uid,
      token: this.token
    }

    this._authService.activateAcount(info).subscribe( (result) => {

      this._alertService.success("Cuenta Activada", "La cuenta a sido activada con exito");
      this._router.navigate(['auth/login']);
    }, (error) => this._alertService.error("Error", "La cuenta no a sido activada correctamente"));

  }
}
