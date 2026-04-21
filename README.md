# DevRange API - Users Service

Микросервис аутентификации и управления пользователями для платформы DevRange.
Поддерживает ролевую модель (Developer, HR, Admin), JWT-авторизацию и управление профилями.

---

## 🚀 Технологии

* Python 3.10+
* Django 5.x
* Django REST Framework (DRF)
* Simple JWT
* Django CORS Headers
* PostgreSQL / SQLite

---

## 📦 Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/Alex-Gaa/dev_range
cd devrange
```

### 2. Создание виртуального окружения

```bash
python -m venv venv

# Linux / Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

Создайте файл `.env`:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/devrange
# или
# DATABASE_URL=sqlite:///db.sqlite3
```

### 5. Миграции и суперпользователь

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Запуск сервера

```bash
python manage.py runserver
```

API будет доступно по адресу:
http://localhost:8000/api/users/

---

## 📚 API Эндпоинты

| Метод | URL        | Описание             | JWT | Body            | Response       |
| ----- | ---------- | -------------------- | --- | --------------- | -------------- |
| POST  | /register/ | Регистрация          | ❌   | email, password | user           |
| POST  | /login/    | Логин                | ❌   | email, password | tokens         |
| POST  | /refresh/  | Обновление токена    | ❌   | refresh         | access         |
| GET   | /me/       | Текущий пользователь | ✅   | -               | user + profile |
| PATCH | /profile/  | Обновление профиля   | ✅   | profile fields  | updated        |
| POST  | /logout/   | Logout               | ✅   | refresh         | message        |

---

## 👥 Роли пользователей

| Роль      | Значение    | Доступ                |
| --------- | ----------- | --------------------- |
| developer | Разработчик | Базовый доступ        |
| hr        | HR          | Управление вакансиями |
| admin     | Админ       | Полный доступ         |

---

## 🔐 Авторизация

Тип: JWT (access + refresh)

### Пример запроса

```bash
POST /api/users/login/
Content-Type: application/json
```

```json
{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

### Ответ

```json
{
  "refresh": "token",
  "access": "token",
  "user": {
    "id": 1,
    "email": "john@example.com",
    "role": "developer"
  }
}
```

### Использование

```http
Authorization: Bearer <access_token>
```

---

## 📋 Модели данных

### User

| Поле        | Тип        | Описание    |
| ----------- | ---------- | ----------- |
| id          | AutoField  | ID          |
| email       | EmailField | Логин       |
| first_name  | CharField  | Имя         |
| last_name   | CharField  | Фамилия     |
| role        | CharField  | Роль        |
| is_verified | Boolean    | Верификация |

### Profile

| Поле         | Тип        |
| ------------ | ---------- |
| avatar       | ImageField |
| bio          | TextField  |
| location     | CharField  |
| github_url   | URLField   |
| linkedin_url | URLField   |
| telegram_url | URLField   |

---

## 🔧 Примеры запросов

### Регистрация

```bash
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
```

---

## 🗂️ Структура проекта

```text
devrange/
├── users/
├── config/
├── media/
├── requirements.txt
└── manage.py
```

---

## 📦 Зависимости

```txt
Django==5.0.3
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
django-cors-headers==4.3.1
Pillow==10.2.0
python-dotenv==1.0.1
psycopg2-binary==2.9.9
```

---

## 🧪 Тестирование

```bash
python manage.py test users
```

---

## 🐛 TODO

* Email verification
* Reset password
* Permissions
* Swagger docs
* Avatar validation

---

## 🔒 CORS

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
```

---

## 🤝 Contributing

```bash
git checkout -b feature/new-feature
git commit -m "add feature"
git push origin feature/new-feature
```

---

## 📄 License

MIT

---

## 📞 Контакты

DevRange Platform
API: 