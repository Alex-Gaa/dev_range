# DevRange API - Users Service

Микросервис аутентификации и управления пользователями для платформы DevRange. Поддерживает ролевую модель (Developer, HR, Admin), JWT-авторизацию и управление профилями.

## 🚀 Технологии

- **Python** 3.10+
- **Django** 5.x
- **Django REST Framework** (DRF)
- **Simple JWT** (JWT аутентификация)
- **Django CORS Headers** (для фронта)
- **PostgreSQL** / SQLite (для разработки)

## 📦 Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/yourusername/devrange.git
cd devrange
2. Создание виртуального окружения
bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
3. Установка зависимостей
bash
pip install -r requirements.txt
4. Настройка переменных окружения
Создайте файл .env в корне проекта:

env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/devrange
# или для SQLite
# DATABASE_URL=sqlite:///db.sqlite3
5. Миграции и создание суперпользователя
bash
python manage.py migrate
python manage.py createsuperuser
6. Запуск сервера
bash
python manage.py runserver
API будет доступно по адресу: http://localhost:8000/api/users/

📚 API Эндпоинты
Метод	URL	Описание	Требуется JWT	Request Body	Response
POST	/api/users/register/	Регистрация нового пользователя	❌	{email, password, password2, first_name, last_name, role}	{id, email, ...}
POST	/api/users/login/	Вход (получение токенов)	❌	{email, password}	{access, refresh, user}
POST	/api/users/refresh/	Обновление access-токена	❌	{refresh}	{access}
GET	/api/users/me/	Получить текущего пользователя и профиль	✅	-	{id, email, role, profile: {...}}
PATCH	/api/users/profile/	Обновить профиль	✅	{avatar, bio, location, ...}	Обновленные поля профиля
POST	/api/users/logout/	Выход (blacklist refresh токена)	✅	{refresh}	{message: "logged out"}
👥 Роли пользователей
Роль	Значение	Доступ
developer	Разработчик	Базовый доступ, просмотр вакансий/проектов
hr	HR-менеджер	Управление вакансиями, просмотр разработчиков
admin	Администратор	Полный доступ (Django admin + API)
🔐 Авторизация
Тип: JWT (JSON Web Token) с refresh-механизмом

Получение токенов:
bash
POST /api/users/login/
Content-Type: application/json

{
    "email": "john@example.com",
    "password": "securepassword123"
}
Ответ:

json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbG...",
    "access": "eyJhbGciOiJIUzI1NiIs...",
    "user": {
        "id": 1,
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "role": "developer"
    }
}
Использование в запросах:
http
Authorization: Bearer <access_token>
📋 Модели данных
User (расширенный AbstractUser)
Поле	Тип	Описание
id	AutoField	Уникальный ID
username	CharField(150)	username = email (внутреннее поле)
email	EmailField	Уникальный email (логин)
first_name	CharField(150)	Имя
last_name	CharField(150)	Фамилия
role	CharField(20)	developer / hr / admin
is_verified	BooleanField	Верификация email (по умолчанию False)
Profile (связь 1:1 с User)
Поле	Тип	Описание
avatar	ImageField	Аватар (загружается в avatars/)
bio	TextField	Биография разработчика
location	CharField(255)	Город/страна
github_url	URLField	Ссылка на GitHub
linkedin_url	URLField	LinkedIn профиль
telegram_url	URLField	Telegram контакт
portfolio_url	URLField	Портфолио/сайт
created_at	DateTimeField	Дата создания профиля
updated_at	DateTimeField	Дата обновления
🔧 Примеры запросов
1. Регистрация нового разработчика
bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "ivan@example.com",
    "password": "secure123",
    "password2": "secure123",
    "first_name": "Иван",
    "last_name": "Петров",
    "role": "developer"
  }'
2. Логин и получение токена
bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "ivan@example.com",
    "password": "secure123"
  }'
3. Получение своего профиля (с токеном)
bash
curl -X GET http://localhost:8000/api/users/me/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
4. Обновление профиля
bash
curl -X PATCH http://localhost:8000/api/users/profile/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "bio": "Senior Python Developer, 5+ years experience",
    "location": "Moscow, Russia",
    "github_url": "https://github.com/ivanpetrov"
  }'
🗂️ Структура проекта
text
devrange/
├── users/                      # Приложение пользователей
│   ├── models.py              # User + Profile модели
│   ├── serializers.py         # Register, JWT, Profile сериализаторы
│   ├── views.py               # Register, Login, Me, Profile, Logout
│   ├── urls.py                # Маршруты /register, /login, /me и т.д.
│   └── admin.py               # Админка (не показана, но должна быть)
├── config/                    # Основная конфигурация Django
│   ├── settings.py            # Настройки (INSTALLED_APPS, REST_FRAMEWORK)
│   ├── urls.py                # Главный urls.py (include users.urls)
│   └── wsgi.py
├── media/                     # Загруженные аватары
│   └── avatars/
├── requirements.txt           # Зависимости
└── manage.py
📦 Необходимые зависимости (requirements.txt)
txt
Django==5.0.3
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
django-cors-headers==4.3.1
Pillow==10.2.0              # Для работы с ImageField
python-dotenv==1.0.1        # Для .env файлов
psycopg2-binary==2.9.9      # Для PostgreSQL (опционально)
🧪 Тестирование
bash
# Запуск всех тестов
python manage.py test users

# С конкретным тестом
python manage.py test users.tests.UserRegistrationTest
Пример теста (добавить в users/tests.py):

python
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

class UserRegistrationTest(TestCase):
    def test_register_developer(self):
        client = APIClient()
        response = client.post(reverse('register'), {
            'email': 'test@example.com',
            'password': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'developer'
        })
        self.assertEqual(response.status_code, 201)
🐛 Известные проблемы и TODO
Добавить верификацию email (отправка письма с подтверждением)

Реализовать сброс пароля через email

Добавить пагинацию для списка пользователей (для HR и Admin)

Добавить эндпоинт GET /users/{id}/ для просмотра профиля другого пользователя

Настроить права доступа (permissions) на основе ролей

Добавить валидацию avatar (размер, формат)

Написать документацию Swagger/OpenAPI (drf-yasg или drf-spectacular)

🔒 Настройка CORS (для связи с фронтендом)
В settings.py:

python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",     # React/Vue/Next.js фронт
    "https://yourdomain.com",
]
🤝 Как внести вклад
Форкните репозиторий

Создайте ветку для фичи (git checkout -b feature/new-feature)

Сделайте коммит изменений

Запушьте ветку (git push origin feature/new-feature)

Откройте Pull Request

📄 Лицензия
MIT License

📞 Контакты
Проект: DevRange Platform

API Base URL: https://api.devrange.example.com/v1/

Документация: /api/docs/ (после добавления Swagger)

Автор: Ваше имя / команда DevRange

text

---

## **Что нужно добавить в ваш проект:**

1. **В `settings.py`** добавьте:
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# JWT настройки
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}
В devrange/urls.py подключите users:

python
from django.urls import path, include

urlpatterns = [
    path('api/users/', include('users.urls')),
    path('admin/', admin.site.urls),
]
Добавьте admin.py для удобного управления:

python
from django.contrib import admin
from .models import User, Profile

admin.site.register(User)
admin.site.register(Profile)