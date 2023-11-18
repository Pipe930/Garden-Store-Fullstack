from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    RetrieveAPIView,
    ListCreateAPIView,
    UpdateAPIView)
from rest_framework.response import Response
from .models import Cart, Items, Voucher, VoucherItem
from apps.products.models import Product
from django.http import Http404
from .serializer import (
    CartSerializer,
    AddCartItemSerializer,
    SubtractCartItemSerializer,
    CreateVoucherSerializer,
    ListVouchersSerializer,
    CancelVoucherSerializer)
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

class ListCreateVoucherView(ListCreateAPIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        ordens = Voucher.objects.filter(user=request.user.id)
        serializer = ListVouchersSerializer(ordens, many=True)

        if not ordens.exists():
            return Response({"status": "No Content", "message": "No tienes ordenes registradas"}, status.HTTP_204_NO_CONTENT)

        return Response(
            message_response_list(serializer.data),
            status.HTTP_200_OK)

    def post(self, request, format=None):

        request.data["user"] = request.user.id
        serializer = CreateVoucherSerializer(data=request.data)

        if not serializer.is_valid():

            return Response(
                message_response_bad_request("La orden", serializer.errors, "POST"),
                status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(
            message_response_created("La orden", serializer.data),
            status.HTTP_201_CREATED)

class CancelVoucherView(UpdateAPIView):

    serializer_class = CancelVoucherSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, id_voucher:int, id_user:int):

        try:
            voucher = Voucher.objects.filter(user=id_user, id_voucher=id_voucher).first()
        except Voucher.DoesNotExist:
            raise Http404

        return voucher

    def put(self, request, id:int):

        request.data["state"] = False
        voucher = self.get_object(id, request.user.id)
        serializer = self.get_serializer(voucher, data=request.data)

        if not serializer.is_valid():
            return Response({"status": "Bad Request", "errors": serializer.errors}, status.HTTP_400_BAD_REQUEST)

        if not voucher.state:
            return Response({"status": "Not Acceptable", "message": "Esta compra esta cancelada"}, status.HTTP_406_NOT_ACCEPTABLE)

        products = VoucherItem.objects.filter(voucher=voucher)

        for product in products:

            product_query = Product.objects.get(id_product=product.product.id_product)

            new_stock = product_query.stock + product.quantity

            product_query.stock = new_stock
            product_query.save()

        serializer.save()
        return Response({"status": "OK", "message": "Se a cancelado la compra con exito"}, status.HTTP_200_OK)

