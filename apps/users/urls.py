from django.urls import path
from . import views

urlsSubcriptions = [
    path("created", views.CreateSubscriptionView.as_view(), name="createdsubscription"),
    path("subscription/<int:id>", views.RetrieveDeleteSubscriptionView.as_view(), name="retrievedeletesubscription")
]
