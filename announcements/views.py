from rest_framework import viewsets, permissions
from .models import Announcement
from .serializers import AnnouncementSerializer


class IsLibrarianOrSuperAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.role in ['LIBRARIAN', 'SUPERADMIN']


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsLibrarianOrSuperAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)