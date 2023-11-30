from django.urls import path
from . import views

urlsCategories = [
    path("", views.ListCreateCategoryView.as_view(), name="listcreatecategory"),
    path("category/<int:id>", views.UpdateDetailCategoryView.as_view(), name="updatedetailcategory")
]

urlsProducts = [
    path("", views.ListCreateProductView.as_view(), name="listcreateproduct"),
    path("client", views.ListProductClientView.as_view(), name="listclientproduct"),
    path("product/<int:id>", views.UpdateDetailProductView.as_view(), name="updatedetailproduct"),
    path("search", views.SearchProductView.as_view(), name="searchproduct")
]

urlsOffers = [
    path("", views.ListCreateOfferView.as_view(), name="listcreateoffer"),
    path("offer/<int:id>", views.UpdateDetailOfferView.as_view(), name="updatedetailveoffer")
]
