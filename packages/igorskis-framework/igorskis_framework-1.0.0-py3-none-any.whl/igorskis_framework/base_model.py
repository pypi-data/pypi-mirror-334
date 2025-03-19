import os
import json

class BaseModel:
    """Базовый класс для всех моделей."""

    def save(self):
        """Сохраняет модель в файл."""
        raise NotImplementedError("Этот метод должен быть реализован в подклассах.")

    def delete(self):
        """Удаляет объект модели из базы данных (удаляет соответствующий файл)."""
        if self.id is not None:
            file_name = f"{self.__class__.__name__}_{self.id}.json"
            file_path = os.path.join('db', file_name)
            
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Объект {self.__class__.__name__} с ID {self.id} удален.")
            else:
                print(f"Объект {self.__class__.__name__} с ID {self.id} не найден.")
        else:
            print("Объект не имеет ID и не может быть удален.")

    def update(self, **fields):
        """Обновляет данные модели."""
        if self.id is not None:
            file_name = f"{self.__class__.__name__}_{self.id}.json"
            file_path = os.path.join('db', file_name)

            if os.path.exists(file_path):
                # Загружаем текущие данные объекта
                with open(file_path, 'r') as file:
                    data = json.load(file)

                # Обновляем данные
                data.update(fields)

                # Сохраняем обновленные данные обратно в файл
                with open(file_path, 'w') as file:
                    json.dump(data, file)

                # Обновляем атрибуты объекта
                self.fields.update(fields)
                print(f"Объект {self.__class__.__name__} с ID {self.id} обновлен.")
            else:
                print(f"Объект {self.__class__.__name__} с ID {self.id} не найден.")
        else:
            print("Объект не имеет ID и не может быть обновлен.")

    @classmethod
    def all(cls):
        """Возвращает все объекты из базы данных."""
        raise NotImplementedError("Этот метод должен быть реализован в подклассах.")