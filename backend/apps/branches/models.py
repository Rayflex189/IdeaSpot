from django.db import models
from django.conf import settings
from apps.prds.models import PRD

class EditedBranch(models.Model):
    prd = models.OneToOneField(PRD, on_delete=models.CASCADE, related_name='edited_branch')
    content = models.JSONField(default=dict)
    editors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='editing_branches', blank=True)
    last_edited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='last_edited_branches')
    version = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'edited_branches'

class BranchHistory(models.Model):
    branch = models.ForeignKey(EditedBranch, on_delete=models.CASCADE, related_name='history')
    content_snapshot = models.JSONField(default=dict)
    edited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    version = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'branch_history'
        unique_together = ['branch', 'version']
