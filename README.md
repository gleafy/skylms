# LMS Project

Проект системы управления обучением с Celery и Django REST framework.

## Запуск через Docker Compose

### 1. Настройка окружения
```bash
# Скопируйте файл с переменными окружения
cp .env.example .env

# Отредактируйте .env файл при необходимости
vim .env
```

### 2. Запуск проекта
```bash
# Запуск всех сервисов
docker-compose up -d

# Просмотр логов
docker-compose logs -f
```

### 3. Инициализация базы данных

Выполнение миграций
```bash
docker-compose exec web python manage.py migrate
```

Создание суперпользователя (опционально)
```bash
docker-compose exec web python manage.py createsuperuser
```

### 4. Доступ к сервисам

- **Админка**: http://localhost:8000/admin
- **API**: http://localhost:8000/api/
- **Swagger**: http://localhost:8000/swagger
- **Redoc**: http://localhost:8000/redoc
- **База данных**: localhost:5432
- **Redis**: localhost:6379

### 5. Остановка проекта
```bash
docker-compose down
```
