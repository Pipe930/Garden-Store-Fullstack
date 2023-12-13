import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AuthModule } from './auth/auth.module';
import { PageNotFoundComponent } from './shared/components/page-not-found/page-not-found.component';
import { PagesModule } from './pages/pages.module';
import { AdminModule } from './admin/admin.module';
import { CategoriesModule } from './admin/categories/categories.module';

@NgModule({
  declarations: [
    AppComponent,
    PageNotFoundComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    AuthModule,
    PagesModule,
    AdminModule,
    CategoriesModule,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
