#C:\Users\Developer\PycharmProjects\devrange\posts\models.py
from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from uuid import uuid4

class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts"
    )

    title = models.CharField(max_length=255)

    slug = models.SlugField(unique=True)

    content = models.TextField()

    excerpt = models.TextField(blank=True)

    cover = models.ImageField(
        upload_to="posts/covers/",
        blank=True,
        null=True
    )

    github_url = models.URLField(blank=True, null=True)

    tech_stack = models.CharField(max_length=255, blank=True)

    is_published = models.BooleanField(default=True)

    views = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_id = str(uuid4())[:8]
            self.slug = f"{slugify(self.title)}-{unique_id}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title