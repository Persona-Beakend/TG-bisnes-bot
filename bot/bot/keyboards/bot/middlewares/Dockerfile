FROM python:3.11-slim

# Запобігаємо запису .pyc файлів та буферизації виводу логів
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Встановлюємо системні залежності при потребі компіляції (gcc, libpq-dev)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Спочатку копіюємо лише requirements для кешування шарів Docker
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копіюємо вихідний код
COPY . .

# Створюємо непривілейованого користувача для безпеки
RUN useradd -m botuser && chown -R botuser:botuser /app
USER botuser

CMD ["python", "main.py"]
