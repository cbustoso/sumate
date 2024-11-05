from rest_framework import status
from rest_framework.response import Response
from apps.account.services.initial_data_load_service import InitialDataLoadService
from rest_framework.parsers import MultiPartParser
from renderer_classes.base_renderer import BasePostView


class AccountFileLoadApi(BasePostView):
    """ 
    Get the current status profile that includes total points
    and the points that are going to expire
    """
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')

        if not file:
            return Response({"error": "Debe cargar un archivo."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            users_not_created = InitialDataLoadService.parse_and_load_data_from_excel(file)
            return Response({
                'message': 'Carga inicial cargada exitósamente.',
                'users_not_created': users_not_created
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)