from rest_framework import status
from rest_framework.response import Response
from apps.account.serializers.account_serializers import WidgetSerializer
from renderer_classes.base_renderer import BaseRetrieveView

class statusApi(BaseRetrieveView):
    """
    API endpoint that retrieves expired points for the logged-in user.
    """
    serializer_class = WidgetSerializer

    def get_object(self):
        user = self.request.user
        
        if user.is_anonymous:
            raise ValueError("Debe registrarse para realizar esta accion.")   
            
        return user
    
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)