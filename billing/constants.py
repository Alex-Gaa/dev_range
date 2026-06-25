#C:\Users\Developer\PycharmProjects\devrange\billing\constants.py
PLANS = {

    "free": {
        "name": "Бесплатный",
        "price": 0,
        "children_limit": 1,
        "subjects_limit": 1,
        "lessons_limit": 5,
    },

    "basic": {
        "name": "Базовый",
        "price": 499,
        "children_limit": 1,
        "subjects_limit": 3,
        "lessons_limit": 50,
    },

    "family": {
        "name": "Семейный",
        "price": 999,
        "children_limit": 3,
        "subjects_limit": 999,
        "lessons_limit": 200,
    }
}