from django.db.models.fields import (
    files,
)

from .utils import (
    inject_descriptor,
    make_model_instance_descriptor,
)


class FieldFile(files.FieldFile):
    """Класс для конфигурации свойства поля."""

    @property
    def url(self):
        """Конфигурация свойства поля.

        Добавляет параметр дескриптора к ссылке `original_url`.
        """
        url = super(FieldFile, self).url
        descriptor = make_model_instance_descriptor(self.instance, self.field.attname)

        return inject_descriptor(url, descriptor)


class DescFileField(files.FileField):
    """Класс поля со ссылкой на файл.

    Содержит измененный url метод,
    который добавляет параметр дескриптора к ссылке `original_url`.
    """

    attr_class = FieldFile
