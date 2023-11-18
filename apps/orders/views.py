from django.http import Http404
from rest_framework.response import Response
from .serializer import (
    ListDispatchGuideSerializer,
    CreateDispatchGuieSerializer,
    UpdateDispatchGuideSerializer,
    ListBillSerializer,
    CreateBillSerializer)
from .models import Bill, DispatchGuide
from rest_framework.generics import ListCreateAPIView
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from core.messages import (
    message_response_list,
    message_response_created,
    message_response_bad_request,
    message_response_no_content,
    message_response_update)

class ListCreateDispatchGuideView(ListCreateAPIView):

    queryset = DispatchGuide.objects.all().order_by("created")
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, format=None):

        dispatch_guides = self.get_queryset()
        serializer = ListDispatchGuideSerializer(dispatch_guides, many=True)

        if not dispatch_guides.exists():

            return Response(
                message_response_no_content("guias de despacho"),
                status.HTTP_204_NO_CONTENT)

        return Response(
            message_response_list(serializer.data),
            status.HTTP_200_OK)

    def post(self, request, format=None):

        serializer = CreateDispatchGuieSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                message_response_bad_request("La guia de despacho", serializer.errors, "POST"),
                status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(
            message_response_created("La guia de despacho"),
            status.HTTP_201_CREATED)

class UpdateDispatchGuideView(generics.UpdateAPIView):

    serializer_class = UpdateDispatchGuideSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self, id:int):

        try:
            dispatch_guide = DispatchGuide.objects.get(id_dispatch_guide = id)
        except DispatchGuide.DoesNotExist:
            raise Http404

        return dispatch_guide

    def put(self, request, id:int, format=None):

        dispatch_guide = self.get_object(id)
        serializer = self.get_serializer(dispatch_guide, data=request.data)

        if not serializer.is_valid():

            return Response(
                message_response_bad_request("La guia de despacho", serializer.errors, "PUT"),
                status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(
            message_response_update("La guia de despacho", serializer.data),
            status.HTTP_205_RESET_CONTENT)

class ListCreateBillView(ListCreateAPIView):

    queryset = Bill.objects.all().order_by("created")
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, format=None):

        queryset = self.get_queryset()
        serializer = ListBillSerializer(queryset, many=True)

        if not len(serializer.data):
            return Response(message_response_no_content("facturas"), status.HTTP_204_NO_CONTENT)

        return Response(
            message_response_list(serializer.data),
            status.HTTP_200_OK)

    def post(self, request, format=None):

        serializer = CreateBillSerializer(data=request.data)

        if not serializer.is_valid():

            return Response(
                message_response_bad_request("La factura", serializer.errors, "POST"),
                  status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(
            message_response_created("La factura", serializer.data),
            status.HTTP_201_CREATED)
