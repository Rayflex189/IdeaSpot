from django.db import models
from django.conf import settings

class Idea(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        GENERATING = 'generating', 'Generating PRD'
        COMPLETED = 'completed', 'PRD Generated'
        ARCHIVED = 'archived', 'Archived'

    title = models.CharField(max_length=200)
    scanty_note = models.TextField()
    raw_description = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ideas')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ideas'

    def __str__(self):
        return self.title
