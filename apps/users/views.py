from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveDestroyAPIView
from django.http import Http404
from rest_framework.permissions import IsAuthenticated, AllowAny
from .utils import Util
from .models import Subscription
from .serializer import (
    CreateSubscriptionSerializer,
    ListSubscriptionSerializer,
    MessageSerializer)
from core.messages import (
    message_response_created,
    message_response_bad_request,
    message_response_detail)

# ----------------------------- SUBCRIPTION VIEWS --------------------------------

# Create Substription View
class CreateSubscriptionView(CreateAPIView):

    serializer_class = CreateSubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    # Petition POST
    def post(self, request, format=None):

        request.data["user"] = request.user.id
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                message_response_bad_request("la subscripción", serializer.errors, "POST"),
                status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(
            message_response_created("La subscripción", serializer.data),
            status.HTTP_201_CREATED)


# View that gets a subscription by id
class DeleteDetailSubscriptionView(RetrieveDestroyAPIView):

    serializer_class = ListSubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, id:int):

        try:
            subscription = Subscription.objects.get(user=id)
        except Subscription.DoesNotExist:
            raise Http404

        return subscription

    # Petition GET
    def get(self, request, id:int, format=None):

        subcription = self.get_object(request.user.id)
        serializer = self.get_serializer(subcription)

        return Response(
            message_response_detail(serializer.data),
            status.HTTP_200_OK)

    # Petition DELETE
    def delete(self, request, id:int, format=None):

        subscription = self.get_object(request.user.id)
        subscription.delete()

        return Response({"status": "No Content", "message": "La subscripcion se elimino correctamente"},status.HTTP_204_NO_CONTENT)

# View for mailing
class SendEmailView(CreateAPIView):

    serializer_class = MessageSerializer
    permission_classes = (AllowAny,)

    # Petition POST
    def post(self, request, format=None):

        serializer = self.get_serializer(data=request.data) # The data is serialized

        if not serializer.is_valid(): # The information is validated
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        Util.send_email(data=serializer.data) # The method of the util send email class is used
        return Response({"status": "OK","data": serializer.data, "message": "El correo se a enviado con exito"}, status.HTTP_200_OK)

