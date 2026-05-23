#C:\Users\Developer\PycharmProjects\devrange\lessons\urls.py
# lessons/urls.py

from rest_framework.routers import DefaultRouter
from .views import LessonViewSet, SubjectViewSet, TopicViewSet

router = DefaultRouter()

router.register(r"subjects", SubjectViewSet, basename="subjects")
router.register(r"topics", TopicViewSet, basename="topics")
router.register(r"", LessonViewSet, basename="lessons")

urlpatterns = router.urls