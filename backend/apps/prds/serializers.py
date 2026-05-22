from rest_framework import serializers
from .models import PRD, PRDPermission

class PRDSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    has_edit_permission = serializers.SerializerMethodField()

    class Meta:
        model = PRD
        fields = '__all__'
        read_only_fields = ['id', 'fingerprint', 'is_protected']

    def get_owner(self, obj):
        return {
            'id': obj.idea.created_by.id,
            'username': obj.idea.created_by.username
        }

    def get_has_edit_permission(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        if obj.idea.created_by == request.user:
            return True
        return PRDPermission.objects.filter(prd=obj, user=request.user, can_edit=True).exists()

class PRDPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PRDPermission
        fields = '__all__'
        read_only_fields = ['id', 'granted_by', 'created_at']
