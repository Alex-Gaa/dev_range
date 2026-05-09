#C:\Users\Developer\PycharmProjects\devrange\lessons\views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Lesson
from .serializers import LessonSerializer


class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Lesson.objects.filter(child__parent=user)

        child_id = self.request.query_params.get("child")

        if child_id and child_id.isdigit():
            queryset = queryset.filter(child_id=child_id)

        return queryset