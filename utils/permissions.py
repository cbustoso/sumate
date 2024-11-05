from django.db.models import Q
from rest_framework import permissions

from utils.constants.permissions_texts_responses import DONT_HAVE_ENOUGH_PERMISSIONS
from utils.constants.predeterminated_groups_user import GROUP_NAME_ADMINISTRATOR, GROUP_NAME_STUDENT

class IsStudentPermission(permissions.BasePermission):
    """ This permission allows only student """
    message = DONT_HAVE_ENOUGH_PERMISSIONS

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.groups.filter(name=GROUP_NAME_ADMINISTRATOR).exists()


class IsAdminUserPermission(permissions.BasePermission):
    """ This permission allows only the admin """
    message = DONT_HAVE_ENOUGH_PERMISSIONS

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.groups.filter(name=GROUP_NAME_STUDENT).exists()