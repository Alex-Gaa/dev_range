# C:\Users\Developer\PycharmProjects\devrange\generate\views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from children.models import Child

from generate.services.ai_lesson_service import (
    generate_lesson,
    AIClient
)


@api_view(["POST"])
def generate_lesson_view(request):

    child_id = request.data.get("child_id")
    subject = request.data.get("subject")
    topic = request.data.get("topic")

    # VALIDATION

    if not all([child_id, subject, topic]):
        return Response(
            {
                "detail":
                    "child_id, subject and topic are required"
            },
            status=400
        )

    # CHILD

    child = Child.objects.filter(
        id=child_id
    ).first()

    if not child:
        return Response(
            {
                "detail": "Child not found"
            },
            status=404
        )

    # GENERATION

    try:

        lesson = generate_lesson(
            child=child,
            subject=subject,
            topic=topic,
            ai_client=AIClient()
        )

        return Response({
            "id": lesson.id,
            "title": lesson.title,
            "content": lesson.content,
            "status": lesson.status,
            "progress": lesson.progress,
        })

    except Exception as e:

        return Response(
            {
                "detail": str(e)
            },
            status=500
        )