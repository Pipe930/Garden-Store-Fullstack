from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveDestroyAPIView
from django.http import Http404
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import login, logout
from .utils import Util
from .models import Subscription, User
from .serializer import (
    CreateSubscriptionSerializer,
    ListSubscriptionSerializer,
    MessageSerializer,
    CustomTokenObtainPairSerializer,
    LogoutSerializer)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from core.messages import (
    message_response_created,
    message_response_bad_request,
    message_response_detail)

# ----------------------------- USER VIEWS --------------------------------

# Login User View
class LoginView(TokenObtainPairView):

    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not User.objects.filter(email=request.data.get("email")).exists():
            Response({"error": "Usuario invalido o contraseña invalida"}, status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=request.data.get("email")).first()

        login(request, user)

        return super().post(request, *args, **kwargs)

# Logout User View
class LogoutView(CreateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def post(self, request, format=None):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token_refresh = serializer.validated_data["refresh_token"]

        try:
            token = RefreshToken(token_refresh)
            token.blacklist()

            logout(request)
        except TokenError:
            return Response({"status": "Bad Request", "message": "Este token ya esta en la lista negra"}, status.HTTP_400_BAD_REQUEST)


        return Response({"status": "OK", "message": "Sesion Terminada con exito"}, status.HTTP_200_OK)

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

