# generate/urls.py
#C:\Users\Developer\PycharmProjects\devrange\generate\urls.py
from django.urls import path
from .views import generate_lesson_view

urlpatterns = [
    path("lesson/", generate_lesson_view),
]