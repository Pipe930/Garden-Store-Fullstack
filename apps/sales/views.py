from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework.response import Response
from .models import Cart, Items, Order
from apps.products.models import Product
from django.http import Http404
from .serializer import (
    CartSerializer,
    AddCartItemSerializer,
    SubtractCartItemSerializer,
    CreateOrderSerializer,
    ListOrderSerializer)
from rest_framework.permissions import IsAuthenticated
from .cart_total import CalculateCart
from apps.users.authentication_mixins import Authentication
from core.messages import (
    message_response_list,
    message_response_created,
    message_response_bad_request,
    message_response_no_content)

instance_cart = CalculateCart()

class CartUserView(RetrieveAPIView):

    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, id:int):

        try:
            cart = Cart.objects.get(user=id)
        except Cart.DoesNotExist:
            raise Http404

        return cart

    def get(self, request, format=None):

        cart = self.get_object(request.user.id)
        serializer = self.get_serializer(cart)

        return Response(
            message_response_list(serializer.data),
            status.HTTP_200_OK)

class AddCartItemView(CreateAPIView):

    serializer_class = AddCartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, id:int):

        try:
            product = Product.objects.get(id_product=id)
        except Product.DoesNotExist:
            raise Http404

        return product

    def post(self, request):

        request.data["user"] = request.user.id
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():

            return Response({"status": "Bad Request", "errors": serializer.errors, "message": "Error, no se agrego el producto al carrito"}, status.HTTP_400_BAD_REQUEST)

        data = serializer.data
        product = self.get_object(data["product"])

        if product.stock >= data["quantity"]:

            serializer.save()
            return Response({"status": "OK", "data": serializer.data, "message": "Agregado al carrito con exito"}, status.HTTP_201_CREATED)

        return Response({"status": "Bad Request", "message": "La cantidad supera el stock disponible"}, status.HTTP_400_BAD_REQUEST)

class DeleteProductCartView(DestroyAPIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, id_user:int, id_product:int):

        try:
            cart = Cart.objects.get(user=id_user)
        except Cart.DoesNotExist:
            raise Http404

        try:
            product = Items.objects.get(cart=cart, product=id_product)
        except Items.DoesNotExist:
            raise Http404

        return product, cart

    def delete(self, request, id:int):

        product, cart = self.get_object(request.user.id, id)
        product.delete()

        return Response({"status": "OK", "message": "Producto Eliminado"}, status.HTTP_200_OK)

class SubtractCartItemView(CreateAPIView):

    serializer_class = SubtractCartItemSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        request.data["user"] = request.user.id

        if not serializer.is_valid():
            return Response({"status": "Bad Request", "errors": serializer.errors}, status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response({"status": "OK", "message": "Se resto el producto"}, status.HTTP_200_OK)

class ClearCartItemsView(DestroyAPIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, id:int):

        try:
            cart = Cart.objects.get(user=id)
        except Cart.DoesNotExist:
            raise Http404

        return cart

    def delete(self, request, format=None):

        cart = self.get_object(request.user.id)

        items = Items.objects.filter(cart = cart.id_cart)

        if len(items):

            for item in items:
                item.delete()

            instance_cart.cart_total(cart)
            instance_cart.calculate_total_products(cart.id_cart)
            instance_cart.calculate_total_quality(cart.id_cart)

            return Response({"status":"No Content", "message": "El carrito se a limpiado con exito"}, status.HTTP_204_NO_CONTENT)

        return Response({"status":"No Content", "message": "Tu carrito esta vacio"}, status.HTTP_204_NO_CONTENT)

class CreateOrderView(ListCreateAPIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        ordens = Order.objects.filter(user=request.user.id)
        serializer = ListOrderSerializer(ordens, many=True)

        if not ordens.exists():
            return Response({"status": "No Content", "message": "No tienes ordenes registradas"}, status.HTTP_204_NO_CONTENT)

        return Response(
            message_response_list(serializer.data),
            status.HTTP_200_OK)

    def post(self, request, format=None):

        request.data["user"] = request.user.id
        serializer = CreateOrderSerializer(data=request.data)

        if not serializer.is_valid():

            return Response(
                message_response_bad_request("La orden", serializer.errors, "POST"),
                status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(
            message_response_created("La orden", serializer.data),
            status.HTTP_201_CREATED)

# class CancelPurchaseView(generics.UpdateAPIView):

#     serializer_class = CancelVoucherSerializer
#     parser_classes = [JSONParser]
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [TokenAuthentication]

#     def get_object(self, id:int):

#         try:
#             voucher = Voucher.objects.get(id_voucher=id)
#         except Voucher.DoesNotExist:
#             raise Http404

#         return voucher

#     def put(self, request, id:int):

#         voucher = self.get_object(id)
#         serializer = self.get_serializer(voucher, data=request.data)

#         if serializer.is_valid():

#             if not token_validated(request, request.user.id):
#                 return Response({"status": "Unauthorized", "message": "Este token no le pertenece a este usuario"}, status.HTTP_401_UNAUTHORIZED)

#             data = serializer.validated_data

#             if data["state"]:
#                 data["state"] = False

#             if not voucher.state:
#                 return Response({"status": "Not Acceptable", "message": "Esta compra esta cancelada"}, status.HTTP_406_NOT_ACCEPTABLE)

#             products = voucher.products
#             items = products["items"]

#             for item in items:

#                 id = item["id"]
#                 quantity = item["quantity"]
#                 product = Product.objects.get(id=id)

#                 new_stock = product.stock + quantity

#                 product.stock = new_stock
#                 product.save()

#             serializer.save()
#             return Response({"status": "OK", "message": "Se a cancelado la compra con exito"}, status.HTTP_200_OK)

#         return Response({"status": "Bad Request", "errors": serializer.errors}, status.HTTP_400_BAD_REQUEST)
