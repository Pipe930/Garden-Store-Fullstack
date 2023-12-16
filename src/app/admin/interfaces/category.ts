import { TableColumns } from "src/app/shared/interfaces/table";

export interface Category {

  id_category: number;
  name_category: string;
}

export interface ResponseCategory {

  status: string;
  count: number;
  data: Array<Category>;
}


export const categoryColumns: Array<TableColumns> = [

  {
    header: "Nombre",
    fieldName: "name_category",
    dataType: "string"
  },
  {
    header: "Acciones",
    fieldName: "action",
    dataType: "action"
  }
]
