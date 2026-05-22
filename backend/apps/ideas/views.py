from rest_framework import generics, permissions
from .models import Idea
from .serializers import IdeaSerializer

class IdeaListCreateView(generics.ListCreateAPIView):
    serializer_class = IdeaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Idea.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class IdeaDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IdeaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Idea.objects.filter(created_by=self.request.user)
