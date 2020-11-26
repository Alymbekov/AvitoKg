from django.urls import path, include
from rest_framework import routers
from apps.announcement.views import (
    OwnerAnnouncementsViewSet, ReaderAnnouncementsAPIView
)

router = routers.DefaultRouter()
router.register('owner_announcements', OwnerAnnouncementsViewSet, basename='owner_announcements')

urlpatterns = [
    path('reader-announcements/', ReaderAnnouncementsAPIView.as_view()),
]
urlpatterns += router.urls


