from django.contrib import admin
from .models import Idea

@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'status', 'created_at')
