#C:\Users\Developer\PycharmProjects\devrange\lessons\views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from .models import Lesson, Topic, Subject
from .serializers import LessonSerializer, TopicSerializer, SubjectSerializer
from django.utils.text import slugify

class LessonViewSet(viewsets.ModelViewSet):

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user = self.request.user

        # PARENT
        if user.role == "parent":

            queryset = Lesson.objects.filter(
                child__parent=user
            )

        # CHILD ACCOUNT
        elif user.role == "child":

            queryset = Lesson.objects.filter(
                child__linked_user=user
            )

        else:
            queryset = Lesson.objects.none()

        child_id = self.request.query_params.get("child")

        if child_id:
            queryset = queryset.filter(child_id=child_id)

        return queryset

    # 🔥 CHILD CAN ONLY UPDATE PROGRESS/STATUS
    def update(self, request, *args, **kwargs):

        lesson = self.get_object()

        # CHILD RESTRICTIONS
        if request.user.role == "child":

            allowed_fields = {"status", "progress"}

            incoming_fields = set(request.data.keys())

            # trying to edit forbidden fields
            if not incoming_fields.issubset(allowed_fields):
                raise PermissionDenied(
                    "Children can only update progress/status"
                )

        return super().update(request, *args, **kwargs)

    # PATCH SUPPORT
    def partial_update(self, request, *args, **kwargs):

        lesson = self.get_object()

        if request.user.role == "child":

            allowed_fields = {"status", "progress"}

            incoming_fields = set(request.data.keys())

            if not incoming_fields.issubset(allowed_fields):
                raise PermissionDenied(
                    "Children can only update progress/status"
                )

        return super().partial_update(request, *args, **kwargs)

    # DELETE ONLY FOR PARENT
    def destroy(self, request, *args, **kwargs):

        if request.user.role != "parent":
            raise PermissionDenied(
                "Only parents can delete lessons"
            )

        return super().destroy(request, *args, **kwargs)

class SubjectViewSet(viewsets.ModelViewSet):
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return Subject.objects.filter(
            Q(is_global=True) |
            Q(parent=user)
        )

    def perform_create(self, serializer):
        name = serializer.validated_data["name"]
        base_slug = slugify(name)

        slug = base_slug
        counter = 1

        # делаем уникальный slug
        while Subject.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        serializer.save(
            parent=self.request.user,
            slug=slug
        )


class TopicViewSet(viewsets.ModelViewSet):

    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user = self.request.user

        queryset = Topic.objects.filter(
            Q(subject__is_global=True) |
            Q(subject__parent=user)
        )

        subject_id = self.request.query_params.get("subject")

        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)

        return queryset