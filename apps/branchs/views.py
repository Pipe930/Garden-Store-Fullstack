from django.http import Http404
from rest_framework.response import Response
from .serializer import (
    ListBranchSerializer,
    CreateUpdateSerializer,
    CreateProductBranchSerializer,
    ListProductBranchSerializer)
from .models import Branch, ProductBranch
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from core.messages import (
    message_response_list,
    message_response_created,
    message_response_bad_request,
    message_response_no_content,
    message_response_update)


# ----------------------------- BRANCH VIEWS --------------------------------

# Create and List Branch View
class ListCreateBranchView(ListCreateAPIView):

    queryset = Branch.objects.all().order_by("name_branch")
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, format=None):

        branchs = self.get_queryset()
        serializer = ListBranchSerializer(branchs, many=True)

        if not branchs.exists():
            return Response(
                message_response_no_content("sucursales"),
                status.HTTP_204_NO_CONTENT)

        return Response(
            message_response_list(serializer.data),
            status.HTTP_200_OK)

    def post(self, request, format=None):

        serializer = CreateUpdateSerializer(data=request.data)

        if not serializer.is_valid():

            return Response(
                message_response_bad_request("la sucursal", serializer.errors, "POST"),
                status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(
            message_response_created("la sucursal", serializer.data),
            status.HTTP_201_CREATED)

# Detail and Update Branch View
class UpdateDetailBranchView(RetrieveUpdateAPIView):

    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = CreateUpdateSerializer

    def get_object(self, id:int):

        try:
            branch = Branch.objects.get(id_branch=id)
        except Branch.DoesNotExist:
            raise Http404

        return branch

    def update(self, request, id:int, format=None):

        branch = self.get_object(id)
        serializer = self.get_serializer(branch, data=request.data)

        if not serializer.is_valid():

            return Response(
                message_response_bad_request("la sucursal", serializer.errors, "PUT"),
                status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(
            message_response_update("la sucursal", serializer.data),
            status.HTTP_205_RESET_CONTENT)

    def get(self, request, id:int, format=None):

        branch = self.get_object(id)
        branch_products = ProductBranch.objects.filter(branch = branch)
        serializer = ListProductBranchSerializer(branch_products, many=True)

        return Response(
            {"status": "OK", "data": {
                "name_branch": branch.name_branch,
                "capacity": branch.capacity,
                "capacity_ocuped": branch.capacity_ocuped,
                "phone": branch.phone,
                "direction": branch.direction,
                "business_name": branch.business_name,
                "commune": branch.commune.name_commune,
                "products": serializer.data
            }},
            status.HTTP_200_OK)

# ----------------------------- PRODUCTS BRANCH VIEWS --------------------------------

# Create and List Branch View
class CreateProductBranchView(CreateAPIView):

    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = CreateProductBranchSerializer

    def post(self, request, format=None):

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"status": "Bad Request", "errors": serializer.errors, "message": "Error, No se agrago el producto a la sucursal"},
                status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(
            {"status": "created", "data": serializer.data, "message": "Se agrego el producto a la sucursal con exito"},
            status.HTTP_201_CREATED)
