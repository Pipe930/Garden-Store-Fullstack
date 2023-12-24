from django.urls import path
from . import views

urls_subcriptions = [
    path("created", views.CreateSubscriptionView.as_view(), name="createdsubscription"),
    path("subscription/<int:id>", views.DeleteDetailSubscriptionView.as_view(), name="retrievedeletesubscription")
]

urls_users = [
    path("sendEmail/", views.SendEmailView.as_view(), name="sendEmail")
]
