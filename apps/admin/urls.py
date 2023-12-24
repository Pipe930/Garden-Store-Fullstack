from django.urls import path
from . import views

urls_administration = [
    path("categories/", views.ListCreateCategoryView.as_view(), name="listcreatecategories"),
    path("category/<int:id>", views.UpdateDetailCategoryView.as_view(), name="updatedetailcategory"),
    path("products/", views.ListCreateProductView.as_view(), name="listcreateproducts"),
    path("product/<int:id>", views.UpdateDetailProductView.as_view(), name="updatedetailproduct"),
    path("offers/", views.ListCreateOfferView.as_view(), name="listcreateoffer"),
    path("offer/<int:id>", views.UpdateDetailOfferView.as_view(), name="updatedetailoffer")
]
