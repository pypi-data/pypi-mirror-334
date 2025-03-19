import re

class Router:
    def __init__(self):
        self.urlpaths = []

    def add_route(self, path, view):
        # Заменяем {param} на группирующие regex-выражения
        path_regex = re.sub(r"{(\w+)}", r"(?P<\1>[^/]+)", path)
        self.urlpaths.append((re.compile(f"^{path_regex}$"), view))

    def resolve(self, path):
        for pattern, view in self.urlpaths:
            match = pattern.match(path)
            if match:
                return view, match.groupdict()  # Передаем параметры
        return None, {}

router = Router()
