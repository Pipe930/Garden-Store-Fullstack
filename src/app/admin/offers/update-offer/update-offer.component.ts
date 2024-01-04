import { Component, OnInit, inject } from '@angular/core';
import { FormBuilder, FormGroup, FormControl, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { OfferService } from '../../services/offer.service';
import { Offer } from '../../interfaces/offer';
import { AlertsService } from 'src/app/shared/services/alerts.service';

@Component({
  selector: 'app-update-offer',
  templateUrl: './update-offer.component.html',
  styleUrls: ['./update-offer.component.scss']
})
export class UpdateOfferComponent implements OnInit {

  private readonly _builder = inject(FormBuilder);
  private readonly _router = inject(Router);
  private readonly _activeRouter = inject(ActivatedRoute);
  private readonly _offerService = inject(OfferService);
  private readonly _alertService = inject(AlertsService);

  public dateTomorrow: string = "";

  public id_offer: number = 0;

  public formUpdateOffer: FormGroup = this._builder.group({
    name_offer: new FormControl("", [Validators.required, Validators.maxLength(255)]),
    end_date: new FormControl("", Validators.required),
    percentage_discount: new FormControl(1, [Validators.required, Validators.min(1), Validators.max(100)])
  });

  public offer: Offer = {
    id_offer: 0,
    name_offer: "",
    start_date: "",
    end_date: "",
    percentage_discount: 0,
    state: false
  }

  ngOnInit(): void {

    this.id_offer = Number(this._activeRouter.snapshot.paramMap.get("id"));
    this._offerService.getOffer(this.id_offer).subscribe(result => {

      if(result){
        this.offer = result.data;

        this.formUpdateOffer.get("name_offer")?.setValue(result.data.name_offer);
        this.formUpdateOffer.get("end_date")?.setValue(result.data.end_date);
        this.formUpdateOffer.get("percentage_discount")?.setValue(result.data.percentage_discount);
        this.formUpdateOffer.updateValueAndValidity();
      }
    })

    const today = new Date().getDate();
    const tomorrow = new Date();
    tomorrow.setDate(today + 1);

    let tomorrowFormatted = tomorrow.toISOString().split('T')[0];
    this.dateTomorrow = tomorrowFormatted;
  }

  public updateOffer():void {

    this._offerService.updateOffer(this.formUpdateOffer.value, this.id_offer).subscribe(resutl => {
      this._router.navigate(["/administration/offers/list"]);
      this._alertService.success("Oferta Actualizada", "Se ha actualizado la oferta correctamente");
    }, (error) => {
      this._alertService.error("Error", "Error, no se actualizo la oferta correctamente");
    })
  }

  get name_offer(){
    return this.formUpdateOffer.controls["name_offer"];
  }

  get end_date(){
    return this.formUpdateOffer.controls["end_date"];
  }

  get percentage_discount(){
    return this.formUpdateOffer.controls["percentage_discount"];
  }

}
