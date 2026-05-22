from django.contrib import admin
from .models import EditedBranch, BranchHistory

@admin.register(EditedBranch)
class EditedBranchAdmin(admin.ModelAdmin):
    list_display = ('prd', 'last_edited_by', 'version', 'updated_at')

@admin.register(BranchHistory)
class BranchHistoryAdmin(admin.ModelAdmin):
    list_display = ('branch', 'edited_by', 'version', 'created_at')
