from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import redirect

class CustomLoginView(LoginView):
    template_name = 'account/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        """
        Returns the success URL to redirect to after a successful login.
        """
        url = super().get_success_url()
        user = self.request.user
        if user.groups.filter(name='administrator').exists():           
             return '/admin/'
        return url