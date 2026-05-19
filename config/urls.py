from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.static import serve
from django.conf import settings
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/auth/", include("users.urls")),
    path("api/children/", include("children.urls")),
    path("api/lessons/", include("lessons.urls")),
    path("api/generate/", include("generate.urls")),
]

# ПРЯМАЯ ОТДАЧА ФАЙЛОВ ИЗ ПАПКИ assets (с правильными MIME-типами)
assets_path = os.path.join(settings.BASE_DIR, 'frontend', 'dist', 'assets')
urlpatterns += [
    re_path(r'^assets/(?P<path>.*)$', serve, {'document_root': assets_path}),
]

# Отдаём index.html для всех остальных маршрутов
urlpatterns += [
    path('', TemplateView.as_view(template_name='index.html')),
    re_path(r'^(?!api|admin|assets|media).*$', TemplateView.as_view(template_name='index.html')),
]