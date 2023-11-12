from django.urls import path
from . import views

urlsCategories = [
    path("", views.ListCreateCategoryView.as_view(), name="listcreatecategory"),
    path("category/<int:id>", views.UpdateRetrieveCategoryView.as_view(), name="updateobtaincategory")
]
