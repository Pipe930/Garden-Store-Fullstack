from django.http import Http404
from rest_framework.response import Response
from .serializer import (
    ListCategorySerializer,
    CreateUpdateCategorySerializer)
from .models import Category, Product, Offer
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authentication import TokenAuthentication

# ----------------------------- CATEGORY VIEWS --------------------------------

# Create and List Category View
class ListCreateCategoryView(ListCreateAPIView):

    queryset = Category.objects.all().order_by("name_category")

    def get_permissions(self):

        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdminUser()]

        return super().get_permissions()

    def get(self, request, format=None):

        categories = self.get_queryset()
        serializer = ListCategorySerializer(categories, many=True)

        if not categories.exists():
            return Response({"status": "No Content", "message": "No tenemos categorias registradas"})

        return Response({"status": "OK", "data": serializer.data})

    def post(self, request, format=None):

        serializer = CreateUpdateCategorySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"status": "Bad Request", "errors": serializer.errors, "message": "Error, la categoria no se creo"},
                status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(
            {"status": "Created", "data": serializer.data, "message": "La categoria se creo con exito"},
            status.HTTP_201_CREATED)

# Update a obtain category View
class UpdateRetrieveCategoryView(RetrieveUpdateAPIView):

    def get_permissions(self):

        if self.request.method == 'PUT':
            return [IsAuthenticated(), IsAdminUser()]

        return super().get_permissions()

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
                {"status": "Bad Request", "errors": serializer.errors, "message": "Error, la categoria no se actualizo"},
                status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(
            {"status": "Reset Content", "data": serializer.data, "message": "Se actualizo la categoria con exito"},
            status.HTTP_205_RESET_CONTENT)

    def get(self, request, id:int, format=None):

        category = self.get_object(id)
        serializer = ListCategorySerializer(category)

        return Response({"status": "OK", "data": serializer.data}, status.HTTP_200_OK)

# ----------------------------- PRODUCT VIEWS --------------------------------
