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

## Настройка CI/CD с GitHub Actions

### Предварительные требования

1. Удаленный сервер на Linux
2. Доступ по SSH с приватным ключом
3. Установленные пакеты на сервере: python3.13, poetry redis, postgresql, gunicorn

### Настройка сервера

1. Создайте директорию для проекта:
   ```bash
   sudo mkdir -p /opt/lms
   sudo chown $USER:$USER /opt/lms
   ```

2. Создать .env по примеру (.env.example) и заполнить переменные своими значениями.

3. Настройте PostgreSQL:
   ```bash
   sudo -u postgres psql
   CREATE DATABASE lms;
   CREATE USER lms_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE lms TO lms_user;
   \q
   ```

4. Настройте Gunicorn (создайте `/etc/systemd/system/gunicorn.service`):
   ```
   [Unit]
   Description=gunicorn daemon for LMS
   After=network.target

   [Service]
   WorkingDirectory=/opt/lms
   ExecStart=/usr/local/bin/poetry run gunicorn --bind unix:/opt/lms/lms.sock config.wsgi:application
   ExecReload=/bin/kill -s HUP $MAINPID

   [Install]
   WantedBy=multi-user.target
   ```

5. Настройте Celery (создайте `/etc/systemd/system/celery_worker.service` и `/etc/systemd/system/celery_beat.service`) 
   ```
   [Unit]
   Description=Celery Worker for LMS
   After=network.target redis.target
   
   [Service]
   Type=simple
   WorkingDirectory=/opt/lms
   ExecStart=/usr/local/bin/poetry run celery -A config worker --loglevel=info
   
   [Install]
   WantedBy=multi-user.target
   ```
   ```
   [Unit]
   Description=Celery Beat for LMS
   After=network.target redis.target     
   [Service]
   Type=simple
   WorkingDirectory=/opt/lms
   ExecStart=/usr/local/bin/poetry run celery -A config beat --loglevel=info     
   [Install]
   WantedBy=multi-user.target
   ```
6. Настройте Nginx (создайте `/etc/nginx/sites-available/lms`):
   ```
   server {
       listen 80;
       server_name your_server_ip;

       location / {
           include proxy_params;
           proxy_pass http://unix:/opt/lms/lms.sock;
       }
   }
   ```

### Настройка GitHub Secrets

В настройках репозитория GitHub добавьте:

- `SSH_KEY` - приватный SSH ключ для доступа к серверу
- `SERVER_IP` - IP адрес вашего сервера
- `SSH_USER` - пользователь для SSH
- `DEPLOY_DIR` - `/opt/lms`

### Workflow процесс

При каждом push в репозиторий автоматически:

1. **Запускаются тесты** Django приложения
2. **При успешном прохождении тестов** происходит деплой на сервер
3. **Этапы деплоя:**
   - Копирование файлов проекта
   - Установка зависимостей через Poetry
   - Сбор статических файлов
   - Применение миграций базы данных
   - Перезапуск сервисов    