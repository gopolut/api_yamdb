# Проект Yamdb:
База данных лучших произведений мира и оценки экспертов

## Как запустить проект:

### 1. Клонировать репозиторий и перейти в него в командной строке:

git clone https://github.com/philaguy/api_yamdb.git

cd api_yamdb

### 2. Cоздать и активировать виртуальное окружение:

python3 -m venv env

source env/bin/activate

### 3. Установить зависимости из файла requirements.txt:

python3 -m pip install --upgrade pip

pip install -r requirements.txt

### 4. Выполнить миграции:

python3 manage.py migrate

### 5. Запустить проект:

python3 manage.py runserver

### OpenAPI схема:

http://localhost/redoc/