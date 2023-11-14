from django.urls import path
from . import views

urlsUsers = [
    path("register", views.RegisterUserView.as_view(), name="registeruser"),
    path("auth/login", views.LoginView.as_view(), name="login"),
    path("auth/logout", views.LogoutView.as_view(), name="logout"),
    path("refresh-token/", views.RefreshTokenView.as_view(), name="refreshtoken")
]

urlsSubcriptions = [
    path("created", views.CreateSubscriptionView.as_view(), name="createdsubscription"),
    path("subscription/<int:id>", views.RetrieveDeleteSubscriptionView.as_view(), name="retrievedeletesubscription")
]
