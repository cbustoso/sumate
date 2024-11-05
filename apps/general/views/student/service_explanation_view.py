from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from utils.decorators.permissions import is_student

def service_explanation_view(request):
    return render(request, 'student/service_explanation.html')
