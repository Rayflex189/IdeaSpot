from django.db import models
from django.conf import settings
from apps.ideas.models import Idea

class PRD(models.Model):
    idea = models.OneToOneField(Idea, on_delete=models.CASCADE, related_name='prd')
    content = models.JSONField(default=dict)
    fingerprint = models.CharField(max_length=64, unique=True)
    is_protected = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'prds'

    def __str__(self):
        return f"PRD for {self.idea.title}"

class PRDPermission(models.Model):
    prd = models.ForeignKey(PRD, on_delete=models.CASCADE, related_name='permissions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    granted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='granted_permissions')
    can_edit = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'prd_permissions'
        unique_together = ['prd', 'user']
