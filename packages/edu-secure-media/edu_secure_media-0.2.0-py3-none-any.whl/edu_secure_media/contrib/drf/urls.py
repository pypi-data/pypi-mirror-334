from django.urls import (
    re_path,
)

from edu_secure_media.utils import (
    get_media_url_path,
)

from .views import (
    SecureMediaView,
)


urlpatterns = (re_path(r'^%s' % get_media_url_path().lstrip('/'), SecureMediaView.as_view()),)
