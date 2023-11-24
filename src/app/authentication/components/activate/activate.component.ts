import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { AuthenticationService } from '../../services/authentication.service';

@Component({
  selector: 'app-activate',
  templateUrl: './activate.component.html',
  styleUrls: ['./activate.component.scss']
})
export class ActivateComponent implements OnInit {

  private uid: string = "";
  private token: string = "";

  constructor(
    private route: ActivatedRoute,
    private service: AuthenticationService
  ) {
    this.route.params.subscribe(params =>{
      this.uid = params["uid"];
      this.token = params["token"];
    })
  }

  ngOnInit(): void {

  }

  public activateAcount():void{

    let info = {
      uid: this.uid,
      token: this.token
    }

    this.service.activateAcount(info);

  }
}
