import { Component, ElementRef, EventEmitter, Input, OnInit, Output, ViewChild, Renderer2, inject } from '@angular/core';
import { Navbar } from '../../interfaces/navbar';
import { AuthService } from 'src/app/auth/services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent implements OnInit {

  private _renderer2 = inject(Renderer2);
  private _authService = inject(AuthService);
  private _router = inject(Router);

  @Input() public sessionActivate: boolean = false;
  @Input() public ObjectsNavbar: Array<Navbar> = [];
  @Output() public eventThemeNavbar = new EventEmitter<boolean>();
  @Output() public eventSession = new EventEmitter<boolean>();
  @ViewChild("openDivNavbar") public containerNavbar!: ElementRef;

  public themeNavbar: boolean = false;
  public modeOriginal:string = "Normal";
  public modeDark:string = "Oscuro";
  public mode:string = this.modeOriginal;
  public showClass:boolean = false;
  public username: string = "";

  ngOnInit(): void {
    this.eventThemeNavbar.emit(this.themeNavbar);

    if(this.sessionActivate){
      this.username = this._authService.getInfoUser().username;
    }
  }

  public openNavbar():void{

    let containerNavbar = this.containerNavbar.nativeElement;
    this._renderer2.addClass(containerNavbar, "visible");

  }

  public closeNavbar():void{

    let containerNavbar = this.containerNavbar.nativeElement;
    this._renderer2.removeClass(containerNavbar, "visible");
  }

  public logout():void {

    this._authService.logout().subscribe(result => {

      sessionStorage.clear();
      this._router.navigate(['/home']);
    });

    this.eventSession.emit(false);
  }

  public themeChange():void{

    if(this.mode === this.modeOriginal){
      this.mode = this.modeDark;
    } else {
      this.mode = this.modeOriginal;
    }

    if(!this.themeNavbar){
      this.themeNavbar = true;
    } else {
      this.themeNavbar = false;
    }

    this.eventThemeNavbar.emit(this.themeNavbar);
  }

}
