from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from apps.account.services.account_service import AccountService

def login_request(request):
    """
    Authenticates a user based on username and password.

    Parameters:
    - request (HttpRequest): The HTTP request with username and password.

    Returns:
    JsonResponse: A JSON response indicating success or failure.
    """
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        AccountService.validate_create_password(username)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"success": True, "message": "Credenciales correctas"})
        else:
            return JsonResponse({"success": False, "message": "Credenciales inválidas"})
    return JsonResponse({"success": False, "message": "Invalid request"})
