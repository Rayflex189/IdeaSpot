from rest_framework import serializers
from .models import EditedBranch, BranchHistory

class EditedBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = EditedBranch
        fields = '__all__'
        read_only_fields = ['id', 'version', 'created_at', 'updated_at']

class BranchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchHistory
        fields = '__all__'
