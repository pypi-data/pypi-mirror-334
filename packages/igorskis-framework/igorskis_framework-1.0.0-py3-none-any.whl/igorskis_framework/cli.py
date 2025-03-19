import os
import argparse

TEMPLATE_FILES = {
    "manage.py": '''import time
from watchdog.observers import Observer
from igorskis_framework.restart_handler import RestartHandler

if __name__ == "__main__":
    print("[INFO] Автоперезапуск сервера активирован...")
    event_handler = RestartHandler()
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\\n[INFO] Остановка сервера.")
        event_handler.server_process.terminate()
        observer.stop()

    observer.join()
''',

    "server.py": '''import os
from wsgiref.simple_server import make_server
from igorskis_framework.router import router
import urls  # Загружаем маршруты

def serve_static_file(path):
    """Функция для обработки статических файлов."""
    # Убираем префикс "/static" из пути
    static_path = os.path.join(os.getcwd(), "static", path[len("/static/"):])
    print(f"Trying to serve static file: {static_path}")  # Выведем путь для отладки
    if os.path.exists(static_path) and os.path.isfile(static_path):
        with open(static_path, "rb") as f:
            return f.read()
    return None

def application(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    
    # Если путь начинается с /static/, обслуживаем статический файл
    if path.startswith("/static/"):
        file_data = serve_static_file(path)
        if file_data:
            status = "200 OK"
            # Определяем тип контента в зависимости от расширения
            if path.endswith(".css"):
                content_type = "text/css"
            elif path.endswith(".js"):
                content_type = "application/javascript"
            else:
                content_type = "application/octet-stream"
            
            headers = [("Content-Type", content_type), ("Content-Length", str(len(file_data)))]
            start_response(status, headers)
            return [file_data]
        else:
            status = "404 Not Found"
            response_body = b"<h1>File not found</h1>"
            headers = [("Content-Type", "text/html"), ("Content-Length", str(len(response_body)))]
            start_response(status, headers)
            return [response_body]
    
    # Для обычных маршрутов
    view, params = router.resolve(path)
    
    if view:
        response_body = view(**params).encode("utf-8")
        status = "200 OK"
        headers = [("Content-Type", "text/html"), ("Content-Length", str(len(response_body)))]
    else:
        response_body = b"<h1>404 Not Found</h1>"
        status = "404 Not Found"
        headers = [("Content-Type", "text/html"), ("Content-Length", str(len(response_body)))]

    start_response(status, headers)
    return [response_body]

if __name__ == "__main__":
    with make_server("", 8000, application) as server:
        print("Serving on port 8000...")
        server.serve_forever()
''',

    "urls.py": '''from igorskis_framework.router import router
from views import *''',

    "views.py": '''from igorskis_framework.templates import html''',
    "models.py": '''from igorskis_framework.models import Model''',
    "__init__.py": ''''''
}


def create_project(project_name):
    """Создаёт новый проект с базовой структурой."""
    if os.path.exists(project_name):
        print(f"Ошибка: Папка '{project_name}' уже существует.")
        return

    os.makedirs(project_name)  # Создаём папку проекта
    os.makedirs(os.path.join(project_name, "static"))  # Создаём папку для статических файлов
    os.makedirs(os.path.join(project_name, "db"))  # Создаём папку для базы данных
    os.makedirs(os.path.join(project_name, "html"))  # Создаём папку для шаблонов

    for filename, content in TEMPLATE_FILES.items():
        file_path = os.path.join(project_name, filename)
        with open(file_path, "w") as f:
            f.write(content)

    print(f"Проект '{project_name}' успешно создан!")


def main():
    parser = argparse.ArgumentParser(description="Igorskis Framework CLI")
    parser.add_argument("command", help="Команда (например, 'startproject')")
    parser.add_argument("project_name", help="Название проекта")

    args = parser.parse_args()

    if args.command == "startproject":
        create_project(args.project_name)
    else:
        print("Неизвестная команда. Используйте: igorskis-admin startproject project-name")


if __name__ == "__main__":
    main()
