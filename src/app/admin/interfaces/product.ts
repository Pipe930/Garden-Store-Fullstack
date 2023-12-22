import { TableColumns } from "src/app/shared/interfaces/table";

export interface Product {

  id_product: number;
  title: string;
  price: number;
  discount_price: number;
  stock: number;
  brand: string;
  image: string;
  slug: string;
  aviable: boolean;
  created: string;
  description: string;
  category: string;
  offer?: string;
}


export interface ResponseListProduct {

  status: string;
  count: number;
  data: Array<Product>;
}

export interface createProduct{

  title: string;
  brand: string;
  price: number;
  category: number;
  image: string;
  description: string;

}

export const productColumns: Array<TableColumns> = [

  {
    header: "Nombre",
    fieldName: "title",
    dataType: "string"
  },
  {
    header: "Precio",
    fieldName: "price",
    dataType: "number"
  },
  {
    header: "Cantidad",
    fieldName: "stock",
    dataType: "number"
  },
  {
    header: "Disponible",
    fieldName: "aviable",
    dataType: "boolean"
  },
  {
    header: "Acciones",
    fieldName: "action",
    dataType: "action"
  }
]
