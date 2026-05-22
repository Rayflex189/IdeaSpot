from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from apps.ideas.models import Idea
from apps.accounts.models import User
from .models import PRD, PRDPermission
from .serializers import PRDSerializer, PRDPermissionSerializer
from .generators import generate_prd_content
from utils.fingerprint import generate_fingerprint

class PRDListCreateView(generics.ListCreateAPIView):
    serializer_class = PRDSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return only PRDs where user is owner or has permission
        user = self.request.user
        owned = PRD.objects.filter(idea__created_by=user)
        permitted = PRD.objects.filter(permissions__user=user)
        return (owned | permitted).distinct()

    def perform_create(self, serializer):
        # Not used directly; PRD is created via generate endpoint
        pass

class PRDDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PRD.objects.all()
    serializer_class = PRDSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return PRD.objects.filter(
            models.Q(idea__created_by=user) | models.Q(permissions__user=user)
        ).distinct()

class GeneratePRDView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, idea_id):
        idea = get_object_or_404(Idea, id=idea_id, created_by=request.user)
        if hasattr(idea, 'prd'):
            return Response({'error': 'PRD already exists'}, status=status.HTTP_400_BAD_REQUEST)

        fingerprint = generate_fingerprint(idea, request.user.id)
        content = generate_prd_content(idea)
        prd = PRD.objects.create(idea=idea, content=content, fingerprint=fingerprint)
        idea.status = Idea.Status.COMPLETED
        idea.save()
        serializer = PRDSerializer(prd, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class GrantPermissionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, prd_id):
        prd = get_object_or_404(PRD, id=prd_id)
        if prd.idea.created_by != request.user:
            return Response({'error': 'Only owner can grant permissions'}, status=403)

        user_id = request.data.get('user_id')
        user = get_object_or_404(User, id=user_id)
        permission, _ = PRDPermission.objects.get_or_create(
            prd=prd, user=user,
            defaults={'granted_by': request.user, 'can_edit': True}
        )
        return Response(PRDPermissionSerializer(permission).data)

class RevokePermissionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, prd_id, user_id):
        prd = get_object_or_404(PRD, id=prd_id)
        if prd.idea.created_by != request.user:
            return Response({'error': 'Only owner can revoke permissions'}, status=403)
        PRDPermission.objects.filter(prd=prd, user_id=user_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
