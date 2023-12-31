from django.urls import path
from . import views

urls_carts = [
    path("cart/user", views.CartUserView.as_view(), name="usercart"),
    path("cart/add", views.AddItemCartView.as_view(), name="additemcart"),
    path("cart/delete/item/<int:id>", views.DeleteProductCartView.as_view(), name="cartdeleteproduct"),
    path("cart/subtract/item", views.SubtractItemCartView.as_view(), name="subtractitem"),
    path("cart/clear", views.ClearItemsCartView.as_view(), name="cartclear")
]

urls_vouchers = [
    path("", views.ListCreateVoucherView.as_view(), name="listcreatedorder"),
    path("cancel/<int:id>", views.CancelVoucherView.as_view(), name="cancelvoucher"),
    path("voucher/<int:id>", views.UpdateVoucherView.as_view(), name="updatevoucher")
]
