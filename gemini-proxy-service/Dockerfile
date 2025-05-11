# Используем официальный образ Python на базе Alpine для минимального размера
FROM python:3.9-alpine

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл с зависимостями и устанавливаем их
# Используем --no-cache-dir и --upgrade pip для оптимизации размера
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код приложения
COPY . .

# Команда для запуска приложения
CMD ["python", "main.py"]