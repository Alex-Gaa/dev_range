#C:\Users\Developer\PycharmProjects\devrange\generate\services\ai_lesson_service.py
import hashlib
import json

from django.template import Template, Context
from django.conf import settings

from openai import OpenAI

from billing.services import reserve_lesson


from generate.models import (
    AIPromptTemplate,
    GeneratedLessonMemory
)

from lessons.models import Lesson



def generate_lesson(child, subject, topic, ai_client):

    # 1. SAFE HASH
    raw_hash = f"{child.id}-{subject}-{topic}"
    lesson_hash = hashlib.sha256(
        raw_hash.encode()
    ).hexdigest()

    # 2. MEMORY CHECK
    memory = GeneratedLessonMemory.objects.filter(
        lesson_hash=lesson_hash
    ).first()

    if memory:

        existing = Lesson.objects.filter(
            child=child
        ).order_by("-created_at").first()

        if existing:
            return existing

    # 3. GET PROMPT
    prompt_template = AIPromptTemplate.objects.filter(
        subject=subject,
        is_active=True
    ).first()

    if not prompt_template:
        raise Exception(
            f"No active prompt found for subject: {subject}"
        )

    # 4. RENDER PROMPT
    try:

        template = Template(
            prompt_template.template
        )

        prompt = template.render(Context({
            "subject": subject,
            "topic": topic,
            "age": child.age,
            "grade": child.grade,
            "interests": child.interests,
        }))

    except Exception as e:

        raise Exception(
            f"Prompt rendering error: {str(e)}"
        )

    # CHECK + RESERVE LESSON SLOT

    if not reserve_lesson(child.parent):
        raise Exception(
            "Monthly lessons limit reached"
        )

    # 5. AI CALL
    ai_response_raw = ai_client.generate(prompt)


    # 6. SAFE JSON PARSING
    if isinstance(ai_response_raw, dict):

        ai_response = ai_response_raw

    else:

        try:
            ai_response = json.loads(
                ai_response_raw
            )

        except Exception:

            ai_response = {
                "title": "Generated Lesson",
                "introduction": str(ai_response_raw)
            }

    # 7. SAFE TITLE
    title = ai_response.get(
        "title",
        f"{subject.title()} Lesson"
    )

    # 8. SAVE LESSON
    lesson = Lesson.objects.create(
        child=child,
        title=title,
        content=ai_response,
        status="draft",
        progress=0
    )


    # 9. SAVE MEMORY
    GeneratedLessonMemory.objects.create(
        subject=subject,
        topic=topic,
        child=child,
        lesson_hash=lesson_hash
    )

    return lesson


class AIClient:

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    def generate(self, prompt: str):

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={
                "type": "json_object"
            },
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert AI teacher "
                        "for children. "
                        "Return ONLY valid JSON."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7
        )

        content = response.choices[0].message.content

        try:

            return json.loads(content)

        except Exception:

            return {
                "title": "Generated Lesson",
                "introduction": content
            }