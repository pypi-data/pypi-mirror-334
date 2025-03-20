import fnmatch
import re
from functools import (
    partial,
)
from typing import (
    Dict,
    List,
    Optional,
    Tuple,
)

from django.conf import (
    settings,
)

from .helpers import (
    memoize,
)


def parse_trusted_host_paths_setting() -> Dict[str, Tuple[str]]:
    """Парсит настройку SECURE_MEDIA_TRUSTED_HOST_PATHS.

    Returns:
        Возвращает словарь с настройками Доверенный хост: кортеж доступных ему путей media.

    """
    settings_ = {}
    for host_path in settings.SECURE_MEDIA_TRUSTED_HOST_PATHS.split(';'):
        host_path = host_path.split(':')

        if not host_path[0]:
            break

        settings_[host_path[0]] = tuple(host_path[1].split(','))

    return settings_


@partial(memoize, cache={}, num_args=0)
def get_handlers_config() -> List[Tuple[Optional[str], str, dict]]:
    """Получает конфигурацию хендлеров из настройки SECURE_MEDIA_HANDLERS.

    Returns:
        Список handler'ов

    """
    from .utils import (
        import_object,
    )

    handlers = []
    for item in SECURE_MEDIA_HANDLERS:
        pattern = item[0]
        regex = None

        if pattern is not None:
            regex = re.compile(fnmatch.translate(pattern))
        handler = item[1]

        if isinstance(handler, str):
            handler = import_object(*handler.rsplit('.', 1))
        options = item[2] if len(item) == 3 else {}
        handlers.append((regex, handler, options))

    return handlers


SECRET_KEY = settings.SECURE_MEDIA_SECRET_KEY

HASHING_ALG = getattr(settings, 'SECURE_MEDIA_HASHING_ALG', 'sha1')

DESCRIPTOR_PARAM_NAME = getattr(settings, 'SECURE_MEDIA_DESCRIPTOR_PARAM_NAME', 'desc')

INSTANCE_DESCRIPTOR_PREFIX = '#/'

PUBLIC_DESCRIPTOR_NAME = getattr(settings, 'SECURE_MEDIA_PUBLIC_DESCRIPTOR_NAME', 'Public')

TRUSTED_HOST_PATHS = parse_trusted_host_paths_setting()

SECURE_MEDIA_HANDLERS = getattr(settings, 'SECURE_MEDIA_HANDLERS', [])
