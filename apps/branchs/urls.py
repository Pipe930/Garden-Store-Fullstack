from django.urls import path
from . import views

urlsBranchs = [
    path("", views.ListCreateBranchView.as_view(), name="listcreatebranch"),
    path("branch/<int:id>", views.UpdateDetailBranchView.as_view(), name="updatedetailbranch"),
    path("product/add", views.CreateProductBranchView.as_view(), name="productaddbranch")
]
