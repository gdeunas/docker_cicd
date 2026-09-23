# Django docker_cicd HW_35.2 
 
## Описание:

Проект Django - это приложение на Python.

## Задание 1
Настройте удаленный сервер для работы с веб-приложением, которое вы разрабатывали в рамках домашних работ на курсе DRF.

## Задание 2
Создайте и настройте файл GitHub Actions workflow, который будет:

Запускать тесты проекта автоматически при каждом push в репозиторий.
Автоматически деплоить проект на удаленный сервер после успешного прохождения тестов.

## Запуск веб-сервера в терминале

````
python manage.py runserver
````

## Главный адрес

````
http://127.0.0.1:8000/
````

## Адрес админки

````
http://127.0.0.1:8000/admin/
````

## Production Deployment & CI/CD

### Адрес приложения
Приложение развернуто и доступно по адресу: `http://your_domain_or_IP`

---

### Настройка сервера (Gunicorn + Nginx + Systemd)

#### 1. Установка и запуск Gunicorn
Gunicorn устанавливается автоматически из зависимостей проекта. Для ручной проверки или установки внутри виртуального окружения:
```bash
pip install gunicorn
```

#### 2. Настройка автоматического перезапуска (Systemd)
1. Создайте файл службы:
   ```bash
   sudo nano /etc/systemd/system/my_app.service
   ```
2. Вставьте конфигурацию:
   ```ini
   [Unit]
   Description=Gunicorn instance to serve my_app
   After=network.target

   [Service]
   User=user
   Group=www-data
   WorkingDirectory=/home/user/my_app
   ExecStart=/home/user/my_app/.venv/bin/gunicorn --workers 3 --bind unix:my_app.sock config.wsgi:application
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```
3. Активируйте и запустите сервис:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable my_app
   sudo systemctl start my_app
   ```

#### 3. Настройка проксирования Nginx
1. Создайте конфигурационный файл сайта:
   ```bash
   sudo nano /etc/nginx/sites-available/my_app
   ```
2. Добавьте настройки проксирования:
   ```nginx
   server {
       listen 80;
       server_name your_domain_or_IP;

       location / {
           include proxy_params;
           proxy_pass http://unix:/home/user/my_app/my_app.sock;
       }

       location /static/ {
           root /home/user/my_app;
       }
   }
   ```
3. Включите конфигурацию и перезапустите Nginx:
   ```bash
   sudo ln -s /etc/nginx/sites-available/my_app /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

---

### Команды проверки статуса сервисов

Для проверки работы компонентов на сервере используйте следующие команды:

```bash
# Проверить статус службы Gunicorn (вашего приложения)
sudo systemctl status my_app

# Проверить статус веб-сервера Nginx
sudo systemctl status nginx

# Посмотреть логи приложения в реальном времени
sudo journalctl -u my_app -f
```

---

### GitHub Secrets

Для работы GitHub Actions и автоматического деплоя в репозитории должны быть настроены следующие Secrets (`Settings -> Secrets and variables -> Actions`):

* **`SSH_HOST`** — IP-адрес или домен вашего production-сервера.
* **`SSH_USER`** — Имя пользователя для подключения по SSH (например, `ubuntu` или `root`).
* **`SSH_KEY`** — Ваш приватный SSH-ключ (содержимое файла `id_rsa`).
* **`ENV_FILE_CONTENT`** — Полное содержимое файла `.env` со всеми боевыми секретами и ключами.

---

### 🚀 Порядок автоматического деплоя (CI/CD)

Деплой происходит автоматически при каждом пуше в ветку `main` (или `master`) по следующему алгоритму:

1. **Checkout & Test:** GitHub Actions забирает свежий код и запускает тесты (если они настроены).
2. **Copy Files:** Код копируется на удаленный сервер через SSH/Rsync.
3. **Install Dependencies:** На сервере обновляются зависимости (`pip install` или `poetry install`).
4. **Environment Setup:** Содержимое из GitHub Secret `ENV_FILE_CONTENT` записывается в файл `.env` на сервере.
5. **Database & Statics:** Выполняются миграции базы данных и сборка статики (например, `collectstatic` для Django).
6. **Application Reload:** Сервис Gunicorn безопасно перезапускается командой `sudo systemctl restart my_app`.


## Документация:

Для получения дополнительной информации обратитесь к [документации] (docs/README.md).

## Лицензия:

Этот проект лицензирован по [лицензии MIT] (LICENSE).