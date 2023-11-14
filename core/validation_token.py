from rest_framework.authtoken.models import Token
from rest_framework.authentication import get_authorization_header

def validation_token(request, idUser:int) -> bool:

    token = get_authorization_header(request).split()[1].decode()

    tokenDB = Token.objects.get(key = token)

    if tokenDB.user.id == idUser:
        return True

    return False
