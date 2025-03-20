from typing import (
    Union,
)

from django.http import (
    HttpResponse,
)
from rest_framework.permissions import (
    AllowAny,
)
from rest_framework.request import (
    Request,
)
from rest_framework.response import (
    Response,
)
from rest_framework.views import (
    APIView,
)

from edu_secure_media.views import (
    check_media_permission_view,
)


class SecureMediaView(APIView):
    """Проверяет наличие разрешений для доступа к media, DRF обёртка.

    Предназначен для интеграции в системы, использующие RestFramework аутентификацию.
    """

    permission_classes = (AllowAny,)  # проверка доступа будет выполнена с помощью обработчиков

    def get(self, request: Request) -> Union[Response, HttpResponse]:
        """Проверяет наличие разрешений для доступа к media."""
        return check_media_permission_view(request)
