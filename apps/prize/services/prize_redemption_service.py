from django.db import transaction

from apps.account.models import User
from apps.semester.services.semester_service import SemesterService
from apps.prize.models import Prize, PrizeRedemption

class PrizRedemptionService:
    def redeem_prize(student: User, prize: Prize) -> None:
        """
        Redeems a prize for a student by deducting the required points from the student's total.
        Raises a ValueError if the student does not have sufficient points.

        Parameters:
        - student (User): The student redeeming the prize.
        - prize (Prize): The prize being redeemed.
        - provided_by (User): The user providing the prize.

        Returns:
        None: Indicates successful completion of the operation.
        """
        if student.points < prize.points:
            raise ValueError("El alumno no tiene suficientes puntos para este premio.")

        with transaction.atomic():
            student.points -= prize.points
            student.save(update_fields=['points'])

            prize.deduct_stock()
            prize.save(update_fields=['stock'])

            last_semester = SemesterService.get_active_semester()

            PrizeRedemption.objects.create(
                prize=prize,
                student=student,
                semester=last_semester,
                points=prize.points
            )
