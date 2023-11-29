from django.http import Http404
from rest_framework.response import Response
from .serializer import (
    ListCategorySerializer,
    CreateUpdateCategorySerializer,
    ListProductsSerializer,
    CreateUpdateProductSerializer,
    ListOfferSerializer,
    CreateUpdateOfferSerializer)
from .models import Category, Product, Offer
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import FormParser, MultiPartParser
from core.messages import (
    message_response_list,
    message_response_created,
    message_response_bad_request,
    message_response_no_content,
    message_response_update,
    message_response_detail)

# ----------------------------- CATEGORY VIEWS --------------------------------

# Create and List Category View
class ListCreateCategoryView(generics.ListCreateAPIView):

    queryset = Category.objects.all().order_by("name_category")

    def get(self, request, format=None):

        categories = self.get_queryset()
        serializer = ListCategorySerializer(categories, many=True)

        if not categories.exists():
            return Response(
                message_response_no_content("categorias registradas"),
                status.HTTP_204_NO_CONTENT)

        return Response(
            message_response_list(serializer.data, categories.count()),
            status.HTTP_200_OK)

    def post(self, request, format=None):

        serializer = CreateUpdateCategorySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                message_response_bad_request("la categoria", serializer.errors, "POST"),
                status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(
            message_response_created("la categoria", serializer.data),
            status.HTTP_201_CREATED)

# Update a obtain category View
class UpdateDetailCategoryView(generics.RetrieveUpdateAPIView):

    # permission_classes = (IsAuthenticated, IsAdminUser)

    def get_object(self, id:int):

        try:
            category = Category.objects.get(id_category=id)
        except Category.DoesNotExist:
            raise Http404

        return category

    def update(self, request, id:int, format=None):

        category = self.get_object(id)
        serializer = CreateUpdateCategorySerializer(category, data=request.data)

        if not serializer.is_valid():
            return Response(
                message_response_bad_request("la categoria", serializer.errors, "PUT"),
                status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(
            message_response_update("la categoria", serializer.data),
            status.HTTP_205_RESET_CONTENT)

    def get(self, request, id:int, format=None):

        category = self.get_object(id)
        serializer = ListCategorySerializer(category)

        return Response(
            message_response_detail(serializer.data),
            status.HTTP_200_OK)

# ----------------------------- PRODUCT VIEWS --------------------------------

# Create and List Product View
class ListCreateProductView(generics.ListCreateAPIView):

    queryset = Product.objects.all().order_by("created")
    permission_classes = (IsAuthenticated, IsAdminUser)
    parser_classes = (FormParser, MultiPartParser)

    def get(self, request, format=None):

        products = self.get_queryset()
        serializer = ListProductsSerializer(products, many=True)

        if not products.exists():
            return Response(
                message_response_no_content("productos registrados"),
                status.HTTP_204_NO_CONTENT)

        return Response(
            message_response_list(serializer.data, products.count()),
            status.HTTP_200_OK)

    def post(self, request, format=None):

        serializer = CreateUpdateProductSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                message_response_bad_request("el producto", serializer.errors, "POST"),
                status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(
            message_response_created("el producto", serializer.data),
            status.HTTP_201_CREATED)

# Update a obtain product View
class UpdateDetailProductView(generics.RetrieveUpdateAPIView):

    parser_classes = (FormParser, MultiPartParser)
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get_object(self, id:int):

        try:
            product = Product.objects.get(id_product=id)
        except Product.DoesNotExist:
            raise Http404

        return product

    def update(self, request, id:int, format=None):

        product = self.get_object(id)
        serializer = CreateUpdateProductSerializer(product, data=request.data)

        if not serializer.is_valid():
            return Response(
                message_response_bad_request("el producto", serializer.errors, "PUT"),
                status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(
            message_response_update("el producto", serializer.data),
            status.HTTP_205_RESET_CONTENT)

    def get(self, request, id:int, format=None):

        product = self.get_object(id)
        serializer = ListProductsSerializer(product)

        return Response(
            message_response_detail(serializer.data),
            status.HTTP_200_OK)

# List Product a Clients View
class ListProductClientView(generics.ListAPIView):

    queryset = Product.objects.filter(aviable=True).order_by("name_product")

    def get(self, request, format=None):

        products = self.get_queryset()
        serializer = ListProductsSerializer(products, many=True)

        if not products.exists():
            return Response(
                message_response_no_content("productos registrados"),
                status.HTTP_204_NO_CONTENT)

        return Response(
            message_response_list(serializer.data, products.count()),
            status.HTTP_200_OK)

# ----------------------------- OFFER VIEWS --------------------------------

# Create and List Offers View
class ListCreateOfferView(generics.ListCreateAPIView):

    queryset = Offer.objects.all().order_by("start_date")
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, format=None):

        offers = self.get_queryset()
        serializer = ListOfferSerializer(offers, many=True)

        if not offers.exists():
            return Response(
                message_response_no_content("ofertas registradas"),
                status.HTTP_204_NO_CONTENT)

        return Response(
            message_response_list(serializer.data, offers.count()),
            status.HTTP_200_OK)

    def post(self, request, format=None):

        serializer = CreateUpdateOfferSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                message_response_bad_request("la oferta", serializer.errors, "POST"),
                status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(
            message_response_created("la oferta", serializer.data),
            status.HTTP_201_CREATED)

# Update a obtain offer View
class UpdateDetailOfferView(generics.RetrieveUpdateAPIView):

    permission_classes = (IsAuthenticated, IsAdminUser)

    def get_object(self, id:int):

        try:
            offer = Offer.objects.get(id_offer=id)
        except Offer.DoesNotExist:
            raise Http404

        return offer

    def update(self, request, id:int, format=None):

        offer = self.get_object(id)
        serializer = CreateUpdateOfferSerializer(offer, data=request.data)

        if not serializer.is_valid():
            return Response(
                message_response_bad_request("la oferta", serializer.errors, "PUT"),
                status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(
            message_response_update("la oferta", serializer.data),
            status.HTTP_205_RESET_CONTENT)

    def get(self, request, id:int, format=None):

        offer = self.get_object(id)
        serializer = ListOfferSerializer(offer)

        return Response(
            message_response_detail(serializer.data),
            status.HTTP_200_OK)
