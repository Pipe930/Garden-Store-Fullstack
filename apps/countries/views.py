from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .models import Commune, Province, Region
from .serializer import (
    RegionSerializer,
    ProvinceSerializer,
    CommuneSerializer)
from core.messages import (
    message_response_list,
    message_response_no_content)

# ----------------------------- REGION VIEWS --------------------------------

# List Regions View
class ListRegionsView(ListAPIView):

    serializer_class = RegionSerializer
    queryset = Region.objects.all()

    # Method GET
    def get(self, request, format=None):

        regions = self.get_queryset()
        serializer = self.get_serializer(regions, many=True)

        if not regions.exists():

            return Response(
                message_response_no_content("regiones"),
                status.HTTP_204_NO_CONTENT)

        return Response(
            message_response_list(serializer.data, regions.count()),
            status.HTTP_200_OK)

# ----------------------------- PROVINCE VIEWS --------------------------------

# List Provincies View
class ListProvincesRegionView(ListAPIView):

    serializer_class = ProvinceSerializer

    # Method GET
    def get(self, request, id:int, format=None):

        provinces = Province.objects.filter(region=id)
        serializer = self.get_serializer(provinces, many=True)

        if not provinces.exists():

            return Response(
                message_response_no_content("provincias"),
                status.HTTP_204_NO_CONTENT)

        return Response(
            message_response_list(serializer.data, provinces.count()),
            status.HTTP_200_OK)

# ----------------------------- COMMUNE VIEWS --------------------------------

# List Communes View
class ListCommuneProvinceView(ListAPIView):

    serializer_class = CommuneSerializer

    # Method GET
    def get(self, request, id:int, format=None):

        communes = Commune.objects.filter(province=id)
        serializer = self.get_serializer(communes, many=True)

        if not communes.exists():

            return Response(
                message_response_no_content("categorias"),
                status.HTTP_204_NO_CONTENT)

        return Response(
            message_response_list(serializer.data, communes.count()),
            status.HTTP_200_OK)
