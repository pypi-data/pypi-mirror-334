import urllib.parse
from typing import (
    TYPE_CHECKING,
    Optional,
    Tuple,
    Union,
)

from django.conf import (
    settings,
)
from django.http import (
    HttpResponseNotFound,
)

from ..config import (
    TRUSTED_HOST_PATHS,
)
from ..utils import (
    get_model_instance_by_descriptor,
    get_real_request_path,
    parse_model_instance_descriptor,
)


if TYPE_CHECKING:
    from django.http import (
        HttpRequest,
    )


def check_path_traversal_attack(request: 'HttpRequest', **kwargs) -> Optional[bool]:  # noqa D417
    """Проверка на атаку Path Traversal.

    Args:
        request:
            Объект запроса.

    Returns:
        Идентификатор разрешения доступа в булевом выражении.

    """
    real_request_path = get_real_request_path(request.path)

    return False if real_request_path != request.path else None


def always_allow_handler(**kwargs) -> bool:  # noqa D417
    """Доступ разрешен всем.

    Returns:
        Идентификатор разрешения доступа в булевом выражении.

    """
    return True


def always_deny_handler(deny_message: str = None, **kwargs) -> Union[bool, HttpResponseNotFound]:  # noqa D417
    """Доступ запрещен.

    Args:
        deny_message:
            Сообщение с запретом на доступ.

    Returns:
        Идентификатор разрешения доступа в булевом выражении либо 'HttpResponseNotFound'.

    """
    return HttpResponseNotFound(deny_message) if deny_message is not None else False


def delegate_to_model_handler(descriptor: str, method_name: str = None, **kwargs) -> bool:  # noqa D417
    """Проверка доступности файлов осуществляется на уровне модели.

    Args:
        descriptor:
            Дескриптор.
        method_name:
            Название метода.

    Returns:
        Идентификатор разрешения доступа в булевом выражении.

    """
    result = False
    method_name = method_name or 'is_public_media'
    instance = get_model_instance_by_descriptor(descriptor)

    if instance is not None:
        method = getattr(instance, method_name)
        field_attname = parse_model_instance_descriptor(descriptor)[2]
        result = method(field_attname)

    return result


def allow_authenticated_handler(request: 'HttpRequest', **kwargs) -> Optional[bool]:  # noqa D417
    """Доступ разрешен авторизованным пользователям.

    Args:
        request:
            Объект запроса.

    Returns:
        Идентификатор разрешения доступа в булевом выражении.

    """
    if request.user.is_authenticated:
        return True


def allow_authenticated_only_handler(  # noqa D417
    request: 'HttpRequest', **kwargs
) -> Union[bool, HttpResponseNotFound]:
    """Доступ разрешен только авторизованным пользователям.

    Args:
        request:
            Объект запроса.

    Returns:
        Идентификатор разрешения доступа в булевом выражении либо 'HttpResponseNotFound'.

    """
    if not request.user.is_authenticated:
        return HttpResponseNotFound(
            'Вы не авторизованы. Возможно, закончилось время '
            'пользовательской сессии. Для повторной '
            'аутентификации обновите страницу.'
        )

    return True


def allow_prefixes_handler(  # noqa D417
    request: 'HttpRequest',
    prefixes: Tuple = (None,),
    join_media_url: bool = True,
    **kwargs,
) -> Optional[bool]:
    """Доступ разрешен всем с префиксом в url файла.

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
    real_request_path = get_real_request_path(request.path)

    for prefix in prefixes:
        if join_media_url:
            prefix = urllib.parse.urljoin(settings.MEDIA_URL, prefix)

        if real_request_path.startswith(prefix):
            return True


def allow_host_handler(request: 'HttpRequest', **kwargs) -> Optional[bool]:  # noqa D417
    """Разрешает доступ доверенным хостам без авторизации.

    Если хост является доверенным для запрашиваемого пути, возвращает True.
    Иначе передает выполнение дальше.
    Если TRUSTED_HOST_PATHS пустой словарь - проверка не производится.

    Args:
        request:
            Объект запроса.

    Returns:
        Идентификатор разрешения доступа в булевом выражении.

    """
    if not TRUSTED_HOST_PATHS:
        return
    remote_addr = request.META.get('REMOTE_ADDR')

    if remote_addr not in TRUSTED_HOST_PATHS:
        # Если хост не указан в настройках - передается для дальнейших проверок:

        return
    else:
        allowed_paths = TRUSTED_HOST_PATHS[remote_addr]
        real_request_path = get_real_request_path(request.path)
        for path in allowed_paths:
            media_path = urllib.parse.urljoin(settings.MEDIA_URL, path)

            if real_request_path.startswith(media_path):
                # Если запрашиваемый путь хостом есть в разрешениях,
                # то доступ разрешается. Дальнейшие проверки не производятся:

                return True
