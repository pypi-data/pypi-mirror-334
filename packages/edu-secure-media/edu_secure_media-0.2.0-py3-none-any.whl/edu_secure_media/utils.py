import base64
import binascii
import hashlib
import importlib
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from functools import (
    reduce,
)
from pathlib import (
    PurePosixPath,
)
from typing import (
    Optional,
    Tuple,
)
from urllib.parse import (
    urlparse,
)

from django.apps import (
    apps,
)
from django.conf import (
    settings,
)
from django.utils.encoding import (
    smart_bytes,
)

from . import (
    config,
)


def make_security_token(path, descriptor) -> str:
    """Формирует токен защищающий ссылку с дескриптором от фальсификации.

    Args:
        path:
            Путь ссылки.
        descriptor:
            Идентификатор ссылки.

    Returns:
        Токен защищающий ссылку с дескриптором от фальсификации.

    """
    hasher = hashlib.new(config.HASHING_ALG)
    hasher.update(smart_bytes(path))
    hasher.update(smart_bytes(descriptor))
    hasher.update(smart_bytes(config.SECRET_KEY))

    return hasher.hexdigest()


def make_model_instance_descriptor(instance, field_attname) -> str:
    """Формирует дескриптор для объекта модели.

    Args:
        instance:
            Экземпляр модели.
        field_attname:
            Название поля с файлом.

    Returns:
        Дескриптор для объекта модели.

    """
    model = instance.__class__
    descriptor = '/'.join(
        (
            model._meta.app_label,
            model.__name__,
            field_attname,
            str(instance.pk),
        )
    )

    return config.INSTANCE_DESCRIPTOR_PREFIX + descriptor


def parse_model_instance_descriptor(descriptor: str) -> Tuple[str, str, str, str]:
    """Получает кортеж из названий атрибутов дескриптора.

    Args:
        descriptor:
            Идентификатор ссылки.

    Returns:
        Кортеж из названий атрибутов дескриптора.

    """
    assert descriptor.startswith(config.INSTANCE_DESCRIPTOR_PREFIX)
    descriptor = descriptor[len(config.INSTANCE_DESCRIPTOR_PREFIX) :]
    app_label, model_name, field_name, pk = descriptor.split('/')

    return app_label, model_name, field_name, pk


def get_model_instance_by_descriptor(descriptor: str):
    """Получение объекта модели по дескриптору.

    Args:
        descriptor:
            Идентификатор ссылки.

    Returns:
        Объект модели.

    """
    app_label, model_name, field_name, pk = parse_model_instance_descriptor(descriptor)

    model = apps.get_model(app_label, model_name)
    try:
        obj = model.objects.get(pk=pk)
    except model.DoesNotExsist:
        obj = None

    return obj


def inject_descriptor(original_url: str, descriptor: str):
    """Добавление параметра дескриптора к ссылке `original_url`.

    Args:
        original_url:
            Строка ссылки.
        descriptor:
            Идентификатор ссылки.

    Returns:
        Новая ссылка.

    Example:
        >>>> inject_descriptor('/media/file.doc', 'mylink')
        '/media/file.doc?desc=WyJteWxpbmsiLCAi...xYWYwNjg3OTI5NiJd'

    """
    parsed_url = urllib.parse.urlparse(original_url)

    sec_token = make_security_token(parsed_url.path, descriptor)
    data = base64.urlsafe_b64encode(smart_bytes(json.dumps([descriptor, sec_token])))

    args_list = urllib.parse.parse_qsl(parsed_url.query)
    args_list.append((config.DESCRIPTOR_PARAM_NAME, data))

    parts = list(parsed_url)
    parts[4] = urllib.parse.urlencode(args_list)

    return urllib.parse.urlunparse(parts)


def public_link(original_url: str) -> str:
    """Делает ссылку публичной.

    Args:
        original_url:
            Строка ссылки.

    Returns:
        Публичная ссылка.

    """
    return inject_descriptor(original_url, config.PUBLIC_DESCRIPTOR_NAME)


def validate_descriptor(url: str) -> Optional[str]:
    """Проверка ссылки на наличие в ней валидного дескриптора.

    Args:
        url:
            Строка ссылки.

    Returns:
        Идентификатор ссылки.

    Example:
        >>>> validate_descriptor('/media/file.doc?desc=WyJteWxpbmsi')
        'mylink'

    """
    url = urllib.parse.unquote(url)
    parsed_url = urllib.parse.urlparse(url)
    data = urllib.parse.parse_qs(parsed_url.query).get(config.DESCRIPTOR_PARAM_NAME)
    if not data:
        return

    try:
        data = json.loads(base64.urlsafe_b64decode(smart_bytes(data[0])))
    except (ValueError, TypeError, binascii.Error):
        return

    descriptor, sec_token = data
    if make_security_token(parsed_url.path, descriptor) != sec_token:
        return

    return descriptor


def import_object(module_name: str, object_name: str = ''):
    """Импорт объекта представленного в виде строки.

    Args:
        module_name:
            Название модуля.
        object_name:
            Название объекта.

    Returns:
        Импортируемый объект.

    """
    obj = importlib.import_module(module_name)
    if object_name:
        obj = reduce(getattr, [obj] + object_name.split('.'))

    return obj


def get_real_request_path(request_path: str) -> str:
    """Возвращает реальный путь до файла.

    Args:
        request_path:
            Путь до файла.

    Returns:
        Реальный путь до файла.

    """
    return os.path.realpath(request_path)


def get_media_url_path():
    """Получает путь из URL-адреса медиафайлов.

    В Django настройка MEDIA_URL может быть полным URL (с хостом) или
    относительным путем (начинающимся с /).

    Returns:
        str: Путь из MEDIA_URL без домена.

    """
    return urlparse(settings.MEDIA_URL).path


def get_absolute_file_path(request) -> PurePosixPath:
    """Извлекает из запроса и возвращает абсолютный путь до файла в ФС.

    Args:
        request:
            Запрос.

    Returns:
        PurePosixPath: Абсолютный путь до файла в ФС.

    """
    # полный путь запроса (без домена)
    path = PurePosixPath(request.path)

    # префикс, если WSGI сервер установил SCRIPT_NAME или указан FORCE_SCRIPT_NAME в settings
    script_name = getattr(settings, 'FORCE_SCRIPT_NAME', '') or request.META.get('SCRIPT_NAME', '')

    # полный префикс: SCRIPT_NAME + MEDIA_URL
    full_prefix = PurePosixPath('/') / script_name.strip('/') / get_media_url_path().strip('/')

    return PurePosixPath(settings.MEDIA_ROOT) / path.relative_to(full_prefix)
