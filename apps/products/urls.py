from django.urls import path
from . import views

urlsCategories = [
    path("", views.ListCreateCategoryView.as_view(), name="listcreatecategory"),
    path("category/<int:id>", views.UpdateRetrieveCategoryView.as_view(), name="updateobtaincategory")
]

urlsProducts = [
    path("", views.ListCreateProductView.as_view(), name="listcreateproduct"),
    path("admin", views.ListProductAdminView.as_view(), name="listadminproduct"),
    path("product/<int:id>", views.UpdateRetrieveProductView.as_view(), name="updateretrieveproduct")
]
