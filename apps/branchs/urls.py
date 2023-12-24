from django.urls import path
from . import views

urls_branchs = [
    path("", views.ListCreateBranchView.as_view(), name="listcreatebranch"),
    path("branch/<int:id>", views.UpdateDetailBranchView.as_view(), name="updatedetailbranch"),
    path("product/add", views.CreateProductBranchView.as_view(), name="productaddbranch")
]
