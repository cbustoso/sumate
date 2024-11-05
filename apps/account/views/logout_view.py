from django.shortcuts import redirect
from django.contrib.auth import logout

def logout_view(request):
    """
    Logs out the user and redirects to the home page.
    """
    logout(request)  # Esto borra la sesión actual
    return redirect('login') 