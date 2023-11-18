from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveDestroyAPIView
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from .models import Subscription
from .serializer import (
    CreateSubscriptionSerializer,
    ListSubscriptionSerializer)
from core.messages import (
    message_response_list,
    message_response_created,
    message_response_bad_request)

# ----------------------------- SUBCRIPTION VIEWS --------------------------------

# Create Substription View
class CreateSubscriptionView(CreateAPIView):

    serializer_class = CreateSubscriptionSerializer

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
class RetrieveDeleteSubscriptionView(RetrieveDestroyAPIView):

    serializer_class = ListSubscriptionSerializer
    permission_classes = [IsAuthenticated]

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
            message_response_list(serializer.data),
            status.HTTP_200_OK)

    # Petition DELETE
    def delete(self, request, id:int, format=None):

        subscription = self.get_object(request.user.id)
        subscription.delete()

        return Response({"status": "No Content", "message": "La subscripcion se elimino correctamente"},status.HTTP_204_NO_CONTENT)
