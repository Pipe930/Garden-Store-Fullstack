import base64
from django.http import Http404
from django.db.models import Q
from rest_framework.response import Response
from django.core.files.base import ContentFile
from .serializer import (
    ListCategorySerializer,
    CreateUpdateCategorySerializer,
    ListProductsSerializer,
    CreateUpdateProductSerializer,
    ListOfferSerializer,
    CreateUpdateOfferSerializer,
    SearchProductSerialzer)
from .models import Category, Product, Offer
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.pagination import PageNumberPagination
from core.messages import (
    message_response_list,
    message_response_created,
    message_response_bad_request,
    message_response_no_content,
    message_response_update,
    message_response_detail)

# ----------------------------- CATEGORY VIEWS --------------------------------

# Create and List Category View
class ListCreateCategoryView(ListCreateAPIView):

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
class UpdateDetailCategoryView(RetrieveUpdateAPIView):

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
class ListCreateProductView(ListCreateAPIView):

    queryset = Product.objects.all().order_by("created")
    permission_classes = (IsAuthenticated, IsAdminUser)

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

        try:
            imagen_base64 = request.data["image"]
            if imagen_base64 != "":
                format, img = imagen_base64.split(';base64,')
                ext = format.split('/')[-1]
                request.data['image'] = ContentFile(base64.b64decode(img), name=f'image_product.{ext}')
        except KeyError:
            return Response({"status": "Bad Request", "message": "Tiene que ingresar una imagen"})

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
class UpdateDetailProductView(RetrieveUpdateAPIView):

    permission_classes = (IsAuthenticated, IsAdminUser)

    def get_object(self, id:int):

        try:
            product = Product.objects.get(id_product=id)
        except Product.DoesNotExist:
            raise Http404

        return product

    def update(self, request, id:int, format=None):

        try:
            imagen_base64 = request.data["image"]
            if imagen_base64 != "":
                format, img = imagen_base64.split(';base64,')
                ext = format.split('/')[-1]
                request.data['image'] = ContentFile(base64.b64decode(img), name=f'image_product.{ext}')
        except KeyError:
            return Response({"status": "Bad Request", "message": "Tiene que ingresar una imagen"})

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
class ListProductClientView(ListAPIView):

    pagination_class = PageNumberPagination

    def get(self, request, format=None):

        products = Product.objects.all().order_by("title")
        page = self.paginate_queryset(products)
        serializer = ListProductsSerializer(page, many=True)

        if not products.exists():
            return Response(
                message_response_no_content("productos registrados"),
                status.HTTP_204_NO_CONTENT)

        return self.get_paginated_response(serializer.data)

# Search Product a Clients View
class SearchProductView(CreateAPIView):

    serializer_class = ListProductsSerializer
    pagination_class = PageNumberPagination
    permission_classes = (AllowAny,)

    def post(self, request, format=None):

        serializer_search = SearchProductSerialzer(data=request.data)

        if not serializer_search.is_valid():
            return Response(
                {"status": "Bad Request", "errors": serializer_search.errors},
                status.HTTP_400_BAD_REQUEST)

        name_product = serializer_search.validated_data["name_product"]
        category_id = serializer_search.validated_data["id_category"]

        search_products = Product.objects.filter(Q(title__icontains=name_product)).order_by("title")

        if category_id == 0:

            page = self.paginate_queryset(search_products)
            serializer = self.get_serializer(page, many=True)

            return self.get_paginated_response(serializer.data)

        if not Category.objects.filter(id_category=category_id).exists():
            return Response({"status": "Not Found", "message": "Esta categoria no existe"}, status.HTTP_404_NOT_FOUND)

        category = Category.objects.get(id_category= category_id)

        search_results = search_products.filter(category=category).order_by("title")
        page = self.paginate_queryset(search_results)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(serializer.data)

# Product Detail by Slug
class DetailProductSlugView(RetrieveAPIView):

    serializer_class = ListProductsSerializer

    def get_object(self, slug:str):

        try:
            product = Product.objects.get(slug= slug)
        except Product.DoesNotExist:
            raise Http404

        return product

    def get(self, request, slug:str, format=None):

        product = self.get_object(slug)
        serializer = self.get_serializer(product)

        return Response(
            message_response_detail(serializer.data),
            status.HTTP_200_OK)

# ----------------------------- OFFER VIEWS --------------------------------

# Create and List Offers View
class ListCreateOfferView(ListCreateAPIView):

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
class UpdateDetailOfferView(RetrieveUpdateAPIView):

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
