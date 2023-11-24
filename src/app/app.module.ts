import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AuthenticationModule } from './authentication/authentication.module';
import { GlobalFuctionsService } from './services/global-fuctions.service';
import { ResetPasswordConfirmComponent } from './authentication/components/reset-password-confirm/reset-password-confirm.component';
import { PageNotFoundComponent } from './components/page-not-found/page-not-found.component';

@NgModule({
  declarations: [
    AppComponent,
    ResetPasswordConfirmComponent,
    PageNotFoundComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    AuthenticationModule,
    ReactiveFormsModule,
    FormsModule
  ],
  providers: [
    GlobalFuctionsService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
