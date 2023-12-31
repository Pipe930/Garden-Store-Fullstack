import { Component, OnInit, inject } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { OfferService } from '../../services/offer.service';
import { AlertsService } from 'src/app/shared/services/alerts.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-create-offer',
  templateUrl: './create-offer.component.html',
  styleUrls: ['./create-offer.component.scss']
})
export class CreateOfferComponent implements OnInit {

  private readonly _offerService = inject(OfferService);
  private readonly _alertService = inject(AlertsService);
  private readonly _router = inject(Router);
  private readonly _builder = inject(FormBuilder);

  public dateTomorrow: string = "";
  public formCreateOffer: FormGroup = this._builder.group({
    name_offer: new FormControl("", [Validators.required, Validators.maxLength(255)]),
    end_date: new FormControl("", Validators.required),
    percentage_discount: new FormControl(1, [Validators.required, Validators.min(1), Validators.max(100)])
  });

  ngOnInit(): void {

    const today = new Date().getDate();
    const tomorrow = new Date();
    tomorrow.setDate(today + 1);

    let tomorrowFormatted = tomorrow.toISOString().split('T')[0];
    this.dateTomorrow = tomorrowFormatted;
  }

  public createOffer():void {

    if(this.formCreateOffer.invalid){

      this.formCreateOffer.markAllAsTouched();
      return;
    }

    const formulario = {
      ...this.formCreateOffer.value
    }

    this._offerService.createOffer(formulario).subscribe(result => {

      this._alertService.success("Creado Existoso", "La oferta se a creado con exito");
      this._router.navigate(["/administration/offers/list"]);
    }, error => this._alertService.error("Error", "Error, la oferta no se creo correctamente"))

  }

  get name_offer(){
    return this.formCreateOffer.controls["name_offer"];
  }

  get end_date(){
    return this.formCreateOffer.controls["end_date"];
  }

  get percentage_discount(){
    return this.formCreateOffer.controls["percentage_discount"];
  }

}
