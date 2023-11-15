from django.urls import path
from . import views

urlsRegions = [
    path("", views.ListRegionsView.as_view(), name="listregions")
]

urlsProvincies = [
    path("region/<int:id>", views.ListProvincesRegionView.as_view(), name="listprovincies")
]

urlsCommunes = [
    path("province/<int:id>", views.ListCommuneProvinceView.as_view(), name="listcommunes")
]
