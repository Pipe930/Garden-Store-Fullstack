from apps.users.authentication import ExiringTokenAuthentication
from rest_framework.authentication import get_authorization_header
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status

class Authentication(object):

    user = None
    user_token_expired = False

    def get_user(self, request):

        token = get_authorization_header(request).split()

        if token:

            try:
                token = token[1].decode()
            except:
                return None

            token_expire = ExiringTokenAuthentication()
            user, token, message, self.user_token_expired = token_expire.authenticate_credentials(token)


            if user != None and token != None:
                self.user = user
                return user

            return message

        return None

    def dispatch(self, request, *args, **kwargs):

        user = self.get_user(request)

        if user is not None:
            if type(user) == str:
                response = Response({"error": user}, status.HTTP_401_UNAUTHORIZED)
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = 'application/json'
                response.renderer_context = {}
                return response

            if not self.user_token_expired:

                return super().dispatch(request, *args, **kwargs)

        response = Response({"message": "Las credenciales de autenticación no se proveyeron."}, status.HTTP_400_BAD_REQUEST)
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = 'application/json'
        response.renderer_context = {}

        return response
