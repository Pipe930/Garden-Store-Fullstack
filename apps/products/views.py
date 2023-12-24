from django.http import Http404
from django.db.models import Q
from rest_framework.response import Response
from .serializer import (
    ListCategorySerializer,
    ListProductsSerializer,
    SearchProductSerialzer)
from .models import Category, Product
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from core.messages import (
    message_response_list,
    message_response_no_content,
    message_response_detail)

# ----------------------------- CATEGORY VIEWS --------------------------------

# Create and List Category View
class ListCategoriesView(ListAPIView):

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

# List Product a Clients View
class ListProductView(ListAPIView):

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
