import { TableColumns } from "src/app/shared/interfaces/table";

export interface Offer {

  id_offer: number;
  name_offer: string;
  state: boolean;
  start_date: string;
  end_date: string;
  percentage_discount: number;
}

export interface CreateOffer {

  name_offer: string;
  end_date: string;
  percentage_discount: number;
}

export interface ResponseOffer {
  status: string;
  data: Offer;
}

export interface ResponseListOffer {

  status: string;
  count: number;
  data: Array<Offer>;
}

export const offerColumns: Array<TableColumns> = [

  {
    header: "Nombre",
    fieldName: "name_offer",
    dataType: "string"
  },
  {
    header: "Fecha Termino",
    fieldName: "end_date",
    dataType: "string"
  },
  {
    header: "Descuento",
    fieldName: "percentage_discount",
    dataType: "string"
  },
  {
    header: "Acciones",
    fieldName: "action",
    dataType: "action"
  }
]
