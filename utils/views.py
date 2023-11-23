from django.http import JsonResponse

def error_404(request, exception):

    response = JsonResponse(data={"message": "Recurso no encontrado", "status_code": 404})
    response.status_code = 404
    return response

def error_500(request):

    response = JsonResponse(data={"message": "Error interno del servidor", "status_code": 500})
    response.status_code = 500
    return response
