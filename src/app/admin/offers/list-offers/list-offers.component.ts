import { Component, OnInit, inject } from '@angular/core';
import { OfferService } from '../../services/offer.service';
import { Offer, offerColumns } from '../../interfaces/offer';
import { Router } from '@angular/router';

@Component({
  selector: 'app-list-offers',
  templateUrl: './list-offers.component.html',
  styleUrls: ['./list-offers.component.scss']
})
export class ListOffersComponent implements OnInit {

  private readonly _router = inject(Router);
  private readonly _offerService = inject(OfferService);

  public listOffer: Array<Offer> = [];
  public columns = offerColumns;

  public listOffers: Array<Offer> = [];

  ngOnInit(): void {

    this._offerService.getAllOffers().subscribe(result => {

      if(result){
        this.listOffer = result.data;
      }
    });
  }

  public editOffer(offer: Offer):void{
    this._router.navigate(['/administration/offers/update/', offer.id_offer]);
  }
}
