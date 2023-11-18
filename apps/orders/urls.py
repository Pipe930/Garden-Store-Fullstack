from django.urls import path
from . import views

urlsDispatchGuides = [
    path("", views.ListCreateDispatchGuideView.as_view()),
    path("dispatch-guide/<int:id>", views.UpdateDispatchGuideView.as_view())
]

urlsBills = [
    path("", views.ListCreateBillView.as_view()),
]
