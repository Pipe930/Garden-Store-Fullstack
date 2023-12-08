export interface Category {
  id_category: number;
  name_category: string;
}

export interface ResponseCategories {
  count: number;
  data: Array<Category>;
  status: string;
}
