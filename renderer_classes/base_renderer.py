from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView
from renderer_classes.response_api_renderer import ApiRenderer
from utils.permissions import IsStudentPermission


class BaseListView(ListAPIView):
    renderer_classes = [ApiRenderer]
    # permission_classes = (IsStudentPermission,)

class BaseRetrieveView(RetrieveAPIView):
    renderer_classes = [ApiRenderer]
    # permission_classes = (IsStudentPermission,)

class BasePostView(CreateAPIView):
    renderer_classes = [ApiRenderer]
    # permission_classes = (IsStudentPermission,)