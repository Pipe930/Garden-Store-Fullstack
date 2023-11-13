from django.urls import path
from . import views

urlsCategories = [
    path("", views.ListCreateCategoryView.as_view(), name="listcreatecategory"),
    path("category/<int:id>", views.UpdateRetrieveCategoryView.as_view(), name="updateobtaincategory")
]

urlsProducts = [
    path("", views.ListCreateProductView.as_view(), name="listcreateproduct"),
    path("client", views.ListProductClientView.as_view(), name="listclientproduct"),
    path("product/<int:id>", views.UpdateRetrieveProductView.as_view(), name="updateretrieveproduct")
]

urlsOffers = [
    path("", views.ListCreateOfferView.as_view(), name="listcreateoffer"),
    path("offer/<int:id>", views.UpdateRetrieveOfferView.as_view(), name="updateretrieveoffer")
]
