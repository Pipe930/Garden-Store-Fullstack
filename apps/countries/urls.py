from django.urls import path
from . import views

urls_regions = [
    path("", views.ListRegionsView.as_view(), name="listregions")
]

urls_provincies = [
    path("region/<int:id>", views.ListProvincesRegionView.as_view(), name="listprovincies")
]

urls_communes = [
    path("province/<int:id>", views.ListCommuneProvinceView.as_view(), name="listcommunes")
]
