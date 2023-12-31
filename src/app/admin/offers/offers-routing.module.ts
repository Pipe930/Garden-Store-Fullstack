import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ListOffersComponent } from './list-offers/list-offers.component';
import { CreateOfferComponent } from './create-offer/create-offer.component';

const routes: Routes = [
  {
    path: "list",
    component: ListOffersComponent
  },
  {
    path: "create",
    component: CreateOfferComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class OffersRoutingModule { }
