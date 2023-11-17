from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, RetrieveDestroyAPIView, UpdateAPIView
from django.http import Http404
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from .models import User, Subscription
from .serializer import CreateUserSerializer, CreateSubscriptionSerializer, ListSubscriptionSerializer, MessageSerializer, ChangePasswordSerializer
from django.contrib.sessions.models import Session
from datetime import datetime
from .util import Util
from apps.sales.models import Cart
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import EmailMultiAlternatives
from rest_framework.authentication import get_authorization_header
from core.messages import (
    message_response_list,
    message_response_created,
    message_response_bad_request)

# Register User View
# Create User in DataBase or System
class RegisterUserView(CreateAPIView):

    serializer_class = CreateUserSerializer

    def post(self, request, format=None):

        # Serializer data
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():

            return Response(
                message_response_bad_request("el usuario", serializer.errors, "POST"),
                status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(
            message_response_created("El usuario", serializer.data),
            status.HTTP_201_CREATED)

# User Login View
class LoginView(ObtainAuthToken):

    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response({"status": "Bad Request", "errors": serializer.errors}, status.HTTP_400_BAD_REQUEST)

        # Authenticated User
        user_found = authenticate(
            username = request.data["username"],
            password = request.data["password"]
        )

        if user_found is not None: # user found?

            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data["user"] # User is obtained

            if user.is_active: # Is the user active?

                token, created = Token.objects.get_or_create(user=user) # A token is created for the user
                cart, createCart = Cart.objects.get_or_create(user=user) # A cart is created for the user

                if created: # If a token exists

                    login(request=request, user=user) # The user is authenticated

                    userJson = {
                        "token": token.key,
                        "username": user.username,
                        "user_id": user.id,
                        "activate": user.is_active,
                        "staff": user.is_staff
                    }

                    return Response(userJson, status.HTTP_200_OK) # Response

                all_sesion = Session.objects.filter(expire_date__gte = datetime.now())
                if all_sesion.exists(): # Is there an active session?

                    for session in all_sesion:
                        session_data = session.get_decoded() # Decode the session

                        if user.id == int(session_data.get("_auth_user_id")): # Is there an active session with this user?
                            session.delete() # delete session

                # If there is not token
                token.delete() # Remove Token
                token = Token.objects.create(user=user) # A new token is created

                # User information
                userJson = {
                    "token": token.key,
                    "username": user.username,
                    "user_id": user.id,
                    "activate": user.is_active,
                    "staff": user.is_staff
                }

                return Response(userJson, status.HTTP_200_OK) # Response

            return Response({"status": "Unauthorized","message": "El usuario no esta activo"},  status.HTTP_401_UNAUTHORIZED)

        return Response({"status": "Unauthorized", "message": "Credenciales Invalidas"}, status.HTTP_401_UNAUTHORIZED)

# View to logout the user
class LogoutView(RetrieveAPIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:
            # The token is obtained in the parameters of the url
            token_request = get_authorization_header(request).split()[1].decode()
            token = Token.objects.filter(key=token_request).first()

            if not token: # Is there a token?
                return Response({"status": "Bad Request","error": "Usuario no encontrado con esas credenciales"},
                status.HTTP_400_BAD_REQUEST)

            user = token.user # Obtain user
            all_sesion = Session.objects.filter(expire_date__gte = datetime.now()) # You get all sessions

            if all_sesion.exists(): # Is there an active session?

                for session in all_sesion:
                    session_data = session.get_decoded() # Decode the session

                    if user.id == int(session_data.get("_auth_user_id")): # Is there an active session with this user?
                        session.delete() # delete session

            token.delete()
            logout(request=request)

            # Messages
            session_message = "Session de usuario terminada"
            token_message = "Token Eliminado"

            # Message in json format
            message = {
                "sesion_message": session_message,
                "token_message": token_message
            }

            return Response(message, status.HTTP_200_OK)

        except:
            return Response({"status": "Conflict","errors": "El token no se a encontrado en la cabecera"}, status.HTTP_409_CONFLICT)

# Refresh Token a User View
class RefreshTokenView(RetrieveAPIView):

    def get(self, request, *args, **kwargs):

        username = request.GET.get("username")
        try:

            user_token = Token.objects.get(
                user = CreateUserSerializer().Meta.model.objects.filter(username = username).first()
            )

            return Response({
                'token': user_token.key
            }, status.HTTP_202_ACCEPTED)

        except:
            return Response({
                "status": "Bad Request",
                "error": "Credenciales enviadas incorrectas"
            }, status.HTTP_400_BAD_REQUEST)

class CreateSubscriptionView(CreateAPIView):

    permission_classes = [IsAuthenticated]
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

# View for mailing
class SendEmailView(CreateAPIView):

    serializer_class = MessageSerializer

    # Petition POST
    def post(self, request, format=None):

        serializer = self.get_serializer(data=request.data) # The data is serialized

        if serializer.is_valid(): # The information is validated

            print(serializer.data)
            Util.send_email(data=serializer.data) # The method of the util send email class is used

            return Response({"status": "OK", "data": serializer.data, "message": "Email enviado con exito"}, status.HTTP_200_OK)

        return Response({"status": "Bad Request", "data":serializer.errors}, status.HTTP_400_BAD_REQUEST)

# View that changes the user"s password
class ChangePasswordView(UpdateAPIView):
    """
    One end point to change the password
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]

    # Get the user object
    def get_object(self, queryset=None):

        object = self.request.user
        return object

    # Petition PUT
    def update(self, request, *args, **kwargs):

        self.object = self.get_object() # Is obtained a user
        serializer = self.get_serializer(data=request.data) # The data is serialized

        if serializer.is_valid(): # The date is validated

            # Check if the password is correct
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status.HTTP_400_BAD_REQUEST)

            # The password that the user will get is encrypted
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save() # The new password is saved

            response = {
                "status": "OK",
                "code": status.HTTP_200_OK,
                "message": "Contraseña cambiada con exito"
            }

            return Response(response)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Garden Store"),
        # message:
        "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key),
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
    msg.send()
