
from rest_framework import serializers
from .models import Idea

class IdeaSerializer(serializers.ModelSerializer):
    created_by_username = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Idea
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at', 'status']
