import { Component, OnInit, inject } from '@angular/core';
import { UserService } from '../../services/user.service';
import { User } from '../../interfaces/user';
import { AuthService } from 'src/app/auth/services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-account',
  templateUrl: './account.component.html',
  styleUrls: ['./account.component.scss']
})
export class AccountComponent implements OnInit {

  private _userService = inject(UserService);
  private _authService = inject(AuthService);
  private _router = inject(Router);

  public user: User = {
    id: 0,
    first_name: "",
    last_name: "",
    username: "",
    email: "",
    is_active: false
  };

  ngOnInit(): void {

    this._userService.getUser().subscribe( result => {
      this.user = result;
    });
  }

}
