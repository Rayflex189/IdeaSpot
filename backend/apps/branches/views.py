from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from apps.prds.models import PRD, PRDPermission
from .models import EditedBranch, BranchHistory
from .serializers import EditedBranchSerializer
from .locking import check_version_conflict

class BranchRetrieveUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def _has_edit_permission(self, prd, user):
        return prd.idea.created_by == user or PRDPermission.objects.filter(prd=prd, user=user, can_edit=True).exists()

    def get(self, request, prd_id):
        prd = get_object_or_404(PRD, id=prd_id)
        if not self._has_edit_permission(prd, request.user):
            return Response({'error': 'No permission'}, status=403)
        branch, _ = EditedBranch.objects.get_or_create(
            prd=prd,
            defaults={'content': prd.content, 'last_edited_by': request.user}
        )
        if request.user not in branch.editors.all():
            branch.editors.add(request.user)
        serializer = EditedBranchSerializer(branch)
        return Response(serializer.data)

    def put(self, request, prd_id):
        prd = get_object_or_404(PRD, id=prd_id)
        if not self._has_edit_permission(prd, request.user):
            return Response({'error': 'No permission'}, status=403)

        branch = get_object_or_404(EditedBranch, prd=prd)
        client_version = request.data.get('version')
        if not check_version_conflict(branch.version, client_version):
            return Response({
                'error': 'Conflict',
                'current_version': branch.version,
                'server_content': branch.content
            }, status=409)

        # Save history
        BranchHistory.objects.create(
            branch=branch,
            content_snapshot=branch.content,
            edited_by=request.user,
            version=branch.version
        )

        branch.content = request.data.get('content', branch.content)
        branch.last_edited_by = request.user
        branch.version += 1
        branch.save()
        return Response(EditedBranchSerializer(branch).data)

class MergeBranchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, prd_id):
        prd = get_object_or_404(PRD, id=prd_id)
        if prd.idea.created_by != request.user:
            return Response({'error': 'Only owner can merge'}, status=403)
        branch = get_object_or_404(EditedBranch, prd=prd)
        prd.content = branch.content
        prd.save()
        return Response({'message': 'Merged successfully'})

class DiscardBranchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, prd_id):
        prd = get_object_or_404(PRD, id=prd_id)
        if prd.idea.created_by != request.user:
            return Response({'error': 'Only owner can discard'}, status=403)
        EditedBranch.objects.filter(prd=prd).delete()
        return Response(status=204)
