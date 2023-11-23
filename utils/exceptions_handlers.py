# custom handler
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.

    handlers = {
        "ValidationError": _handle_generic_error,
        "MethodNotAllowed": _handle_generic_error,
        "NotFound": _handle_generic_error,
        "PermissionDenied": _handle_generic_error,
        "NotAuthenticated": _handle_authentication_error
    }

    response = exception_handler(exc, context)
    exception_class=exc.__class__.__name__

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)

    return response

def _handle_authentication_error(exc, contect, response):
    response.data = {
        "message": "Las credenciales de autenticación no se proveyeron",
        "status_code": response.status_code
    }

    return response

def _handle_generic_error(exc, contect, response):
    return response
