from setuptools import setup, find_packages

setup(
    name="igorskis-framework",
    version="1.0.0",
    packages=find_packages(),
    install_requires=["jinja2", "watchdog"],
    entry_points={
        "console_scripts": [
            "igorskis-admin=igorskis_framework.cli:main",
        ],
    },
    license="MIT",  # Добавляем лицензию
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="igorskis",
    author_email="usikowigor@gmail.com",
    classifiers=[
        "License :: OSI Approved :: MIT License",  # Категория лицензии
        "Programming Language :: Python :: 3",
    ],
)
