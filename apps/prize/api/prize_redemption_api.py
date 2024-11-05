from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from renderer_classes.base_renderer import BasePostView
from apps.account.models import User
from apps.prize.services.prize_redemption_service import PrizRedemptionService
from apps.prize.models import Prize


class PrizeRedemptionAPi(BasePostView):
    """
    Handles prize redemption requests, validating eligibility and executing redemption.
    """
    def post(self, request, *args, **kwargs):
        prize_id = request.data.get('prize_id')
        request.user = request.user

        prize = self.fetch_prize(prize_id)
        if not prize:
            return Response({"error": "El premio seleccionado es inválido."}, status=status.HTTP_400_BAD_REQUEST)
        
        student = self.fetch_student(request.user.id)

        if not student:
            return Response({"error": "El estudiante no puede canjear el premio."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            PrizRedemptionService.redeem_prize(student, prize)
            return Response({"success": "Premio canjeado exitosamente."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def fetch_prize(prize_id: int) -> Prize:
        """
        Fetches the prize object based on the provided ID.
        """
        try:
            return Prize.objects.get(pk=prize_id, is_active=True)
        except Prize.DoesNotExist:
            return None

    @staticmethod
    def fetch_student(student_id: int) -> User:
        """
        Fetches the student object based on the provided ID.
        """
        try:
            student_group = Group.objects.get(name='student')
            return User.objects.get(pk=student_id, is_active=True, groups=student_group)
        except User.DoesNotExist:
            return None
