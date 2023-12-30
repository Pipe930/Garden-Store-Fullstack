export interface Product {

  id_product: number;
  title: string;
  price: number;
  discount_price: number;
  stock: number;
  sold: number;
  image: string;
  brand: string;
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

export interface ResponseProduct {
  status: string;
  data: Product;
}

export interface SearchProduct {
  id_category: number;
  name_product: string;
}
