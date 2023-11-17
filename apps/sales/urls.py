from django.urls import path
from . import views

urlsCarts = [
    path("cart/user", views.CartUserView.as_view(), name="usercart"),
    path("cart/add", views.AddCartItemView.as_view(), name="additemcart"),
    path("cart/delete/item/<int:id>", views.DeleteProductCartView.as_view(), name="cartdeleteproduct"),
    path("cart/subtract/item", views.SubtractCartItemView.as_view(), name="subtractitem"),
    path("cart/clear", views.ClearCartItemsView.as_view(), name="cartclear")
]

urlsOrders = [
    path("", views.CreateOrderView.as_view(), name="createdorder")
]
