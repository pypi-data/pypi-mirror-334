import json
import os
from igorskis_framework.validator import Validator
from igorskis_framework.base_model import BaseModel


class Model(BaseModel):
    """Представление модели, которая будет взаимодействовать с данными."""

    def __init__(self, **fields):
        self.fields = fields
        self.id = None

    def validate(self):
        """Валидация данных перед сохранением."""
        for field_name, value in self.fields.items():
            # Пример валидации:
            if field_name == 'email':
                Validator.validate_email(value)  # Важно: вызываем валидацию email
            Validator.validate_required(value, field_name)

    def save(self):
        """Сохранение объекта модели в файл."""
        # Выполняем валидацию данных
        self.validate()

        # Создаем папку db, если её нет
        if not os.path.exists('db'):
            os.makedirs('db')

        # Для простоты мы будем сохранять в файл с использованием JSON
        data = self.fields
        if self.id:
            # Если объект уже был сохранен, обновим его
            file_name = f"{self.__class__.__name__}_{self.id}.json"
        else:
            # Если объект новый, генерируем новый ID
            self.id = self.__class__.generate_id()
            file_name = f"{self.__class__.__name__}_{self.id}.json"

        file_path = os.path.join('db', file_name)

        with open(file_path, 'w') as file:
            json.dump(data, file)
