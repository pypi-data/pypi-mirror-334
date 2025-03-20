from typing import (
    TYPE_CHECKING,
    Union,
)

from django.http import (
    HttpResponse,
    HttpResponseNotFound,
)
from django_sendfile import (
    sendfile,
)

from . import (
    config,
)
from .utils import (
    get_absolute_file_path,
    validate_descriptor,
)


if TYPE_CHECKING:
    from django.http import (
        HttpRequest,
    )
    from django.http.response import (
        FileResponse,
    )


def check_media_permission_view(request: 'HttpRequest') -> Union[HttpResponse, 'FileResponse']:
    """Проверяет наличие разрешений для доступа к media.

    Args:
        request:
            Объект запроса.

    Returns:
        объект 'HttpResponse' либо 'FileResponse'.

    """
    ret = None
    descriptor = None

    if config.DESCRIPTOR_PARAM_NAME in request.GET:
        descriptor = validate_descriptor(request.get_full_path())

    for regex, handler, options in config.get_handlers_config():
        if regex is None or (descriptor and regex.search(descriptor)):
            ret = handler(request=request, descriptor=descriptor, **options)
            if ret is not None:
                break

    if isinstance(ret, HttpResponse):
        return ret

    if ret:
        ret = sendfile(request, get_absolute_file_path(request))
    else:
        ret = HttpResponseNotFound('Media Not Found!')

    return ret
