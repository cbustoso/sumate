from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

def admin_superuser_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.request.user.is_authenticated:
            return Response({"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)    
        
        if not request.request.user.is_superuser or not request.request.user.groups.filter(name='administrator').exists():
            return Response({"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        return view_func(request, *args, **kwargs)
    return _wrapped_view