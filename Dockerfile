FROM python:3.14-alpine

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем только файлы зависимостей
COPY pyproject.toml poetry.lock* ./

# Устанавливаем зависимости системы
RUN pip install poetry==2.2.1 && poetry config virtualenvs.create false && poetry update

# Копируем исходный код приложения в контейнер
COPY . .

# Пробрасываем порт, который будет использовать Django
EXPOSE 8000

# Команда для запуска приложения
CMD ["", "", "python", "manage.py", "runserver", "0.0.0.0:8000"]