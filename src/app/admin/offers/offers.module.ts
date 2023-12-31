import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { OffersRoutingModule } from './offers-routing.module';
import { ListOffersComponent } from './list-offers/list-offers.component';
import { SharedModule } from 'src/app/shared/shared.module';
import { CreateOfferComponent } from './create-offer/create-offer.component';
import { ReactiveFormsModule } from '@angular/forms';


@NgModule({
  declarations: [
    ListOffersComponent,
    CreateOfferComponent
  ],
  imports: [
    CommonModule,
    OffersRoutingModule,
    SharedModule,
    ReactiveFormsModule
  ]
})
export class OffersModule { }
