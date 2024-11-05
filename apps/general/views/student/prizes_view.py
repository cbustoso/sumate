from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from apps.account.models.user import User
from apps.prize.models import Prize
from utils.decorators.permissions import is_student

@user_passes_test(is_student)
def prizes_view(request):
    user_id = request.user.id
    user_points = User.objects.filter(id=user_id).values('points').get()
    prizes = Prize.objects.filter(is_active=True).order_by('-points', '-stock')
    
    context = {
        'prizes': prizes,
        'user_points': user_points,
    }

    return render(request, 'student/prizes.html', context)
