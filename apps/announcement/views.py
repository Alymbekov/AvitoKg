from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.announcement.models import AnnouncementModel
from apps.announcement.permissions import IsOwner
from apps.announcement.serializers import (
    AnnouncementAPISerializer,
)


class ReaderAnnouncementsAPIView(ListAPIView):
    queryset = AnnouncementModel.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = AnnouncementAPISerializer


class OwnerAnnouncementsViewSet(viewsets.ModelViewSet):
    serializer_class = AnnouncementAPISerializer
    queryset = AnnouncementModel.objects.all()
    permission_classes = (IsAuthenticated, IsOwner, )

    def get_queryset(self):
        return AnnouncementModel.objects.filter(
            author=self.request.user
        )
