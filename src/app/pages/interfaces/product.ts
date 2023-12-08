export interface Product {

  id_product: number;
  name_product: string;
  price: number;
  discount_price: number;
  stock: number;
  image: string;
  slug: string;
  aviable: boolean;
  created: string;
  description: string;
  category: string;
  offer?: string;
}

export interface ResponseProducts {
  count: number;
  next?: string;
  previous?: string;
  results: Array<Product>;
}

export interface SearchProduct {
  id_category: number;
  name_product: string;
}
