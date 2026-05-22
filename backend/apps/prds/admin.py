from django.contrib import admin
from .models import PRD, PRDPermission

@admin.register(PRD)
class PRDAdmin(admin.ModelAdmin):
    list_display = ('id', 'idea', 'fingerprint', 'created_at')
    readonly_fields = ('fingerprint',)

@admin.register(PRDPermission)
class PRDPermissionAdmin(admin.ModelAdmin):
    list_display = ('prd', 'user', 'granted_by', 'can_edit')
