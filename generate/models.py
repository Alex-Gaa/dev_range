# C:\Users\Developer\PycharmProjects\devrange\generate\models.py

from django.db import models


class AIPromptTemplate(models.Model):

    subject = models.CharField(
        max_length=100,
        db_index=True
    )

    name = models.CharField(max_length=255)

    template = models.TextField(
        help_text="""
Use variables:
{{subject}},
{{topic}},
{{age}},
{{grade}},
{{interests}}
"""
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["subject", "name"]
        verbose_name = "AI Prompt Template"
        verbose_name_plural = "AI Prompt Templates"

    def save(self, *args, **kwargs):
        self.subject = self.subject.lower().strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.subject} - {self.name}"


class GeneratedLessonMemory(models.Model):

    subject = models.CharField(
        max_length=100,
        db_index=True
    )

    topic = models.CharField(max_length=255)

    child = models.ForeignKey(
        "children.Child",
        on_delete=models.CASCADE,
        related_name="generated_memories"
    )

    lesson_hash = models.CharField(
        max_length=64,
        unique=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["subject", "topic", "child"]),
        ]

        verbose_name = "Generated Lesson Memory"
        verbose_name_plural = "Generated Lesson Memories"

    def save(self, *args, **kwargs):
        self.subject = self.subject.lower().strip()
        self.topic = self.topic.lower().strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.child.first_name} | {self.subject} | {self.topic}"