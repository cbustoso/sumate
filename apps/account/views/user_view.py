from django.shortcuts import render
from apps.account.decorators.permissions import group_required
from apps.account.services.initial_score_load_service import InitialScoreLoadService
from apps.account.services.initial_data_load_service import InitialDataLoadService

@group_required('administrator')
def upload_file_initial_view(request):
    """
    View for uploading an initial file 
    """
    if request.method == "POST":
        file = request.FILES.get('file')
        if file:
            InitialDataLoadService.parse_and_load_data_from_excel(file)
    return render(request, 'apps/account/upload_file_initial.html')

@group_required('administrator')
def upload_file_score_view(request):
    """
    View for uploading a score initial file
    """
    if request.method == "POST":
        file = request.FILES.get('file')
        if file:
            InitialScoreLoadService.parse_and_load_data_from_excel(file)
    return render(request, 'apps/account/upload_file_score.html')


