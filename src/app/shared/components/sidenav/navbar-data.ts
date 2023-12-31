import { Sidenav } from "../../interfaces/sidenav";

export const navbarData: Array<Sidenav> = [
  {
    routerLink: "dashboard",
    icon: "bx bxs-dashboard",
    label: "Dashboard"
  },
  {
    routerLink: "categories",
    icon: "bx bxs-category",
    label: "Categorias",
    items: [
      {
        routerLink: "categories/list",
        label: "Lista Categorias",
      },
      {
        routerLink: "categories/create",
        label: "Crear Categoria",
      }
    ]
  },
  {
    routerLink: "products",
    icon: "bx bxl-product-hunt",
    label: "Productos",
    items: [
      {
        routerLink: "products/list",
        label: "Lista Productos",
      },
      {
        routerLink: "products/create",
        label: "Crear Producto",
      }
    ]
  },
  {
    routerLink: "offers",
    icon: "bx bxs-offer",
    label: "Ofertas",
    items: [
      {
        routerLink: "offers/list",
        label: "Lista Ofertas",
      },
      {
        routerLink: "offers/create",
        label: "Crear Oferta",
      }
    ]
  }
]
