from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Lesson
from .serializers import LessonSerializer


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