# Igorskis Framework
Igorskis Framework это веб-фреймворк для создания веб-приложений.
Чтобы создать веб-приложение, ты можешь использовать команду igorskis-admin startproject project_name.
Ты можешь создовать URL-адреса в urls.py командой router.add_route(path, view). В views.py ты можешь создавать функции для рендеринга страниц. Пример: def index(): return html("index.html"). Создай файл html/index.html и добавь в него HTML-код.
Также в models.py ты можешь создавать модели. Пример: class User(Model): def __init__(self, name, email): super().__init__(name=name, email=email). В моделях ты можешь использовать методы get_all(), update(), delete(). Также ты можешь создавать экземпляры моделей. Чтобы создать экземпляр модели, выполни команду: user = User(name="John Doe", email="9K9bM@example.com"). Чтобы добавить экземпляр модели в базу данных, вызови метод save().
Картинки, CSS-стили и JavaScript-скрипты добавляются в папку static/
В разработке используй эту команду для запуска сервера: python3 manage.py. Для продакшена используй эту команду: python3 server.py.