from django.urls import path
from . import views

urls_categories = [
    path("", views.ListCategoriesView.as_view(), name="listcreatecategory")
]

urls_products = [
    path("", views.ListProductView.as_view(), name="listclientproduct"),
    path("search", views.SearchProductView.as_view(), name="searchproduct"),
    path("detail/product/<str:slug>", views.DetailProductSlugView.as_view(), name="detailproductslug")
]
