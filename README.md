# LMS Project

Проект системы управления обучением с Celery и Django REST framework.

## Запуск через Docker Compose

### 1. Настройка окружения

Скопируйте файл с переменными окружения:
```bash
cp .env.example .env
```

Отредактируйте .env файл:
```bash
vim .env
```

### 2. Запуск проекта

Запуск всех сервисов:
```bash
docker-compose up -d
```

Просмотр логов:
```bash
docker-compose logs -f
```

### 3. Инициализация базы данных

Выполнение миграций:
```bash
docker-compose exec web python manage.py migrate
```

Создание суперпользователя (опционально):
```bash
docker-compose exec web python manage.py createsuperuser
```

### 4. Доступ к сервисам

- **Приложение**: http://localhost
- **Админка**: http://localhost/admin
- **API**: http://localhost/api/
- **База данных**: доступна только внутри Docker сети
- **Redis**: доступен только внутри Docker сети

### 5. Остановка проекта
```bash
docker-compose down
```

## Настройка CI/CD с GitHub Actions

### Предварительные требования

1. Удаленный сервер на Linux с установленными Docker и Docker Compose
2. Доступ по SSH с приватным ключом

### Настройка сервера

1. Установите Docker и Docker Compose:

2. Создайте директорию для проекта:
```bash
sudo mkdir -p /opt/lms
sudo chown $USER:$USER /opt/lms
```

Создайте .env файл в директории проекта:
```bash
cd /opt/lms
cp .env.example .env
# Отредактируйте .env файл своими значениями
```

### Настройка GitHub Secrets

В настройках репозитория GitHub добавьте:

- `SSH_KEY` - приватный SSH ключ для доступа к серверу
- `SERVER_IP` - IP адрес вашего сервера
- `SERVER_IP6` - IPv6 адрес сервера (для маскировки в логах)
- `SSH_USER` - пользователь для SSH
- `DEPLOY_DIR` - `/opt/lms`
- `TEST_POSTGRES_DB` - имя тестовой БД
- `TEST_POSTGRES_USER` - пользователь тестовой БД  
- `TEST_POSTGRES_PASSWORD` - пароль тестовой БД
- `TEST_SECRET_KEY` - секретный ключ для тестов

### Workflow процесс

При каждом push в репозиторий автоматически:

1. **Запускаются тесты** Django приложения
2. **Собираются Docker образы** и проверяется их работоспособность
3. **При успешном прохождении тестов** происходит деплой на сервер
4. **Этапы деплоя:**
   - Копирование файлов проекта на сервер
   - Остановка текущих контейнеров
   - Запуск обновленных контейнеров
   - Применение миграций базы данных
   - Сбор статических файлов

## Структура проекта

```
.
├── config/                 # Настройки Django
├── materials/              # Приложение материалов курса
├── users/                  # Приложение пользователей
├── nginx/                  # Конфигурация Nginx
├── docker-compose.yaml     # Docker Compose конфигурация
├── Dockerfile              # Образ для Django приложения
├── .github/workflows/      # CI/CD конфигурация
└── README.md              # Документация
```

## Технологии

- **Backend**: Django, Django REST Framework
- **База данных**: PostgreSQL
- **Кеширование и брокер**: Redis
- **Асинхронные задачи**: Celery + Celery Beat
- **Контейнеризация**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **Веб-сервер**: Nginx
- **WSGI сервер**: Gunicorn