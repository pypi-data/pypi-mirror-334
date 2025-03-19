from jinja2 import Environment, FileSystemLoader

# Настройка Jinja2 для загрузки шаблонов из папки "templates"
env = Environment(loader=FileSystemLoader("html"))

def html(template_name, **context):
    """Функция для рендеринга HTML-шаблонов с переданными параметрами."""
    template = env.get_template(template_name)
    return template.render(**context)
