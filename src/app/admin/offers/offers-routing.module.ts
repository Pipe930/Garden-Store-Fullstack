import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ListOffersComponent } from './list-offers/list-offers.component';
import { CreateOfferComponent } from './create-offer/create-offer.component';
import { UpdateOfferComponent } from './update-offer/update-offer.component';

const routes: Routes = [
  {
    path: "list",
    component: ListOffersComponent
  },
  {
    path: "create",
    component: CreateOfferComponent
  },
  {
    path: "update/:id",
    component: UpdateOfferComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class OffersRoutingModule { }
