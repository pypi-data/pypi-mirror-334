from django.urls import (
    re_path,
)

from edu_secure_media.utils import (
    get_media_url_path,
)

from .views import (
    check_media_permission_view,
)


urlpatterns = (re_path(r'^%s' % get_media_url_path().lstrip('/'), check_media_permission_view),)
