import re

class Validator:
    """Класс для валидации данных."""
    
    @staticmethod
    def validate_email(email):
        """Проверка, что email в правильном формате."""
        # Более точное регулярное выражение для email
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(email_regex, email):
            raise ValueError(f"Некорректный формат email: {email}")
    
    @staticmethod
    def validate_required(value, field_name):
        """Проверка на обязательность поля."""
        if not value:
            raise ValueError(f"Поле '{field_name}' не может быть пустым.")
    
    @staticmethod
    def validate_min_length(value, min_length, field_name):
        """Проверка минимальной длины строки."""
        if len(value) < min_length:
            raise ValueError(f"Поле '{field_name}' должно содержать хотя бы {min_length} символов.")