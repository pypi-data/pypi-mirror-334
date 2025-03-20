import urllib.parse
from typing import (
    TYPE_CHECKING,
    Optional,
    Tuple,
)

from django.conf import (
    settings,
)
from m3_users import (
    ADMIN,
    SUPER_ADMIN,
)
from m3_users.api import (
    user_has_metarole,
)

from ..utils import (
    get_real_request_path,
)


if TYPE_CHECKING:
    from django.http import (
        HttpRequest,
    )


def allow_admin_only_handler(  # noqa D417
    request: 'HttpRequest',
    prefixes: Tuple = (None,),
    join_media_url: bool = False,
    **kwargs,
) -> Optional[bool]:
    """Доступ разрешен только администраторам.

    Args:
        request:
            Объект запроса.
        prefixes:
            Префиксы для ссылки.
        join_media_url:
            Объединение MEDIA_URL с prefix в булевом выражении.

    Returns:
        Идентификатор разрешения доступа в булевом выражении.

    """
    is_allowed = None

    real_request_path = get_real_request_path(request.path)

    for prefix in prefixes:
        if join_media_url:
            prefix = urllib.parse.urljoin(settings.MEDIA_URL, prefix)

        if real_request_path.startswith(prefix):
            if request.user.is_authenticated and (
                user_has_metarole(request.user, ADMIN) or user_has_metarole(request.user, SUPER_ADMIN)
            ):
                is_allowed = True
            else:
                is_allowed = False

            break

    return is_allowed
