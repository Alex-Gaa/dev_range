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
                "error": "child_id, subject and topic are required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # CHILD

    child = Child.objects.filter(
        id=child_id
    ).first()

    if not child:

        return Response(
            {
                "error": "Child not found"
            },
            status=status.HTTP_404_NOT_FOUND
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
                "error": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )