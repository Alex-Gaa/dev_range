#C:\Users\Developer\PycharmProjects\devrange\lessons\views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q

from billing.constants import PLANS
from .models import Lesson, Topic, Subject
from .serializers import LessonSerializer, TopicSerializer, SubjectSerializer
from django.utils.text import slugify
from rest_framework.exceptions import ValidationError

from billing.services import reserve_lesson, get_or_create_subscription


class LessonViewSet(viewsets.ModelViewSet):

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user = self.request.user

        # BASE QUERYSET
        queryset = Lesson.objects.select_related(
            "child",
            "subject",
            "topic"
        )

        if user.role == "parent":

            queryset = queryset.filter(
                child__parent=user
            )

        elif user.role == "child":

            queryset = queryset.filter(
                child__linked_user=user
            )

        else:

            return Lesson.objects.none()

        # SINGLE CHILD
        child_id = self.request.query_params.get("child")

        if child_id:
            queryset = queryset.filter(
                child_id=child_id
            )

        # MULTIPLE CHILDREN
        children = self.request.query_params.get("children")

        if children:
            ids = [
                child_id.strip()
                for child_id in children.split(",")
                if child_id.strip()
            ]

            queryset = queryset.filter(
                child_id__in=ids
            )

        # STATUS
        status = self.request.query_params.get("status")

        if status:
            queryset = queryset.filter(
                status=status
            )

        # SUBJECT
        subject = self.request.query_params.get("subject")

        if subject:
            queryset = queryset.filter(
                subject_id=subject
            )

        # TOPIC
        topic = self.request.query_params.get("topic")

        if topic:
            queryset = queryset.filter(
                topic_id=topic
            )

        # SEARCH
        search = self.request.query_params.get("search")

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(child__first_name__icontains=search) |
                Q(subject__name__icontains=search) |
                Q(topic__name__icontains=search)
            )

        # DATE RANGE
        date_from = self.request.query_params.get("date_from")

        if date_from:
            queryset = queryset.filter(
                created_at__date__gte=date_from
            )

        date_to = self.request.query_params.get("date_to")

        if date_to:
            queryset = queryset.filter(
                created_at__date__lte=date_to
            )

        # ORDERING
        ordering = self.request.query_params.get(
            "ordering",
            "-created_at"
        )

        allowed_ordering = [
            "created_at",
            "-created_at",
            "title",
            "-title",
            "status",
            "-status",
            "progress",
            "-progress",
        ]

        if ordering in allowed_ordering:
            queryset = queryset.order_by(
                ordering
            )

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

    def perform_create(self, serializer):

        user = self.request.user

        if user.role != "parent":
            raise PermissionDenied(
                "Only parents can create lessons."
            )

        serializer.save()



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

        user = self.request.user

        subscription = get_or_create_subscription(user)
        from billing.constants import PLANS

        limit = PLANS[subscription.plan]["subjects_limit"]

        current_count = Subject.objects.filter(parent=user).count()

        if current_count >= limit:
            raise ValidationError({
                "detail": f"Your {subscription.plan} plan allows only {limit} subjects."
            })

        name = serializer.validated_data["name"]

        base_slug = slugify(name)

        slug = base_slug
        counter = 1

        while Subject.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        serializer.save(
            parent=user,
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