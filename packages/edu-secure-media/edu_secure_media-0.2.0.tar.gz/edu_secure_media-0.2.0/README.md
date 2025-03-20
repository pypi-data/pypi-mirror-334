# Пакет для проверки авторизации пользователя перед доступом к /media/

---
## Установка и настройка

1. Установить пакет в окружение:
    ```pip install edu-secure-media```
    Также можно установить `m3` расширения: 
    ```pip install edu-secure-media[m3]```
    и\или `drf` расширения:
    ```pip install edu-secure-media[drf]```
2. В основном `urls.py` расширить `urlpatterns`
    ```
    # Пример использования в ЭШ:
    from edu_secure_media.urls import (
        urlpatterns as secure_urls,
    )
    
    urlpatterns += secure_urls
    ```
    либо DRF версию
    ```python
    from edu_secure_media.contrib.drf.urls import  urlpatterns as secure_media_urls
    
    urlpatterns += secure_media_urls
    ```
3. Добавить в settings.py параметры:
- SECURE_MEDIA_SECRET_KEY
- SECURE_MEDIA_TRUSTED_HOST_PATHS
  ```
  # Пример использования:
  SECURE_MEDIA_TRUSTED_HOST_PATHS = conf.get('secure_media', 'trusted_host_paths').replace(' ', '') or ''
  ```
- SECURE_MEDIA_HASHING_ALG (по умолчанию 'sha1')
- SECURE_MEDIA_DESCRIPTOR_PARAM_NAME (по умолчанию 'desc')
- SECURE_MEDIA_PUBLIC_DESCRIPTOR_NAME (по умолчанию 'Public')
- SECURE_MEDIA_HANDLERS
  ```
  # Пример использования с разъяснением в разделе "Параметры SECURE_MEDIA_HANDLERS"
  ```
- Для django-sendfile:
   - SENDFILE_BACKEND  
  ```
   # Пример использования для машины разработчика:
   SENDFILE_BACKEND = conf.get('secure_media', 'backend') or 'django_sendfile.backends.development'
  
   # Пример использования для тестовых и production серверов:
   SENDFILE_BACKEND = conf.get('secure_media', 'backend') or 'django_sendfile.backends.nginx'
  ```
     - SENDFILE_URL   
  ```
  # Адрес, на который будет перенаправлен запрос в случае, если авторизация прошла успешна. 
  # Адрес не должен заканчиваться слешем. Пример использования:
  SENDFILE_URL = conf.get('secure_media', 'url') or '/protected'
  ```
   - SENDFILE_ROOT = MEDIA_ROOT
  ```
  SENDFILE_ROOT всегда равен MEDIA_ROOT, 
  директория с файлами, для отдачи которых требуется авторизация.
  ```
4. Для тестовых и production серверов в конфигурационном файле проекта задать
параметры
```
    [secure_media]
    backend = django_sendfile.backends.nginx
    # URL на который будет перенаправляться запрос
    url = /protected
```
5. Для тестовых и production серверов сконфигурировать **NGINX**.  
Для url из параметров необходимо задать секцию ``location`` в конфигурационном файле **NGINX**.  

---
## Алгоритм обработки запроса на тестовых и production серверах:

Поступает запрос от клиента на URL ``/media/*``. **NGINX** принимает запрос
и передает проксируемому серверу (**django**, **gunicorn**). Этот запрос не
кэшируется.   
Пример конфигурации:

    location / {
        proxy_pass http://localhost:8000;
        include proxy_params;
        charset utf-8;
        chunked_transfer_encoding off;
    }
    location /media/ {
        proxy_pass http://localhost:8000/media/;
        # Не кэшируем запрос на клиенте
        expires -1;
    }

Запрос обрабатывается в **Django view**. Если запрашиваются файлы в
/media/public, то они отдаются без каких-либо проверок.
Если пользователь не авторизован, то на клиент возвращается ``json`` с
сообщением. Если пользователь авторизован, то запрос перенаправляется
на **URL** заданный параметром ``SENDFILE_URL``. **location** для него
должен быть задан в конфигурационном файле **NGINX**

    location /protected/ {
        # Обрабатываются внутренние запросы
        internal;
        # Если для nginx используется докер, путь к media должен соответствовать пути, 
        # в который смонтирована директория с медиафайлами.
        alias /home/ivahotin/dev/kinder_conf/media/;
        # Отключаем кеширование в браузере
        expires -1;
    }

---
## Параметры SECURE_MEDIA_HANDLERS
```
# Пример использования в ЭШ:
SECURE_MEDIA_HANDLERS = [
    [
        None,
        'edu_secure_media.handlers.common.check_path_traversal_attack',
    ],
    [
        None,
        'edu_secure_media.handlers.common.allow_host_handler',
    ],
    [
        None,
        'edu_secure_media.handlers.common.allow_prefixes_handler',
        {
            'prefixes': [
                'public/',
            ]
        },
    ],
    [
        None,
        'edu_secure_media.handlers.m3.allow_admin_only_handler',
        {
            'prefixes': [
                'downloads/admin/',
                'uploads/edu_rdm_integration/',
                f'{RDM_COLLECT_LOG_DIR}/'
                f'{RDM_EXPORT_LOG_DIR}/',
            ],
            'join_media_url': True,
        }
    ],
    [
        None,
        'edu_secure_media.handlers.common.allow_authenticated_handler',
    ],
    [
        'Public',
        'edu_secure_media.handlers.common.always_allow_handler',
    ],
    [
        '#/emie_school/*',
        'edu_secure_media.handlers.common.delegate_to_model_handler',
    ],
    [
        '*',
        'edu_secure_media.handlers.common.always_allow_handler',
    ]
]
```

Список handler'ов определяющих доступность файла по его ссылке.

Каждый элемент списка это список из 3х элементов:

 * pattern для сопоставления или None. Если None, то хендлер функция будет вызываться для всех ссылок,
   иначе только для тех у которых pattern совпадает с дескриптором ссылки. Паттерны сопоставляются модулем fnmatch.
 * Путь к хендлер функции, которая будет вызвана
 * Словарь именнованных аргуметов для хендлер функции

Хендлеры вызываются по порядку.
Каждый handler должен вернуть одно из 4-х значений:

* True - Если доступ разрешается
* False - Если доступ запрещается
* HttpResponse - Если нужно вернуть ответ "как есть"
* None - Если хендлер не смог однозначно нужно дать доступ или нет

Если один из handler'ов возвращает True, False или HttpResponse, обработка
прерывается, если же None, то обрабатываются следующие handler'ы.
