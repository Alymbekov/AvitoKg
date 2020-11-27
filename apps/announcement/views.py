from datetime import timedelta

from django.utils import timezone
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


from apps.announcement.models import AnnouncementModel
from apps.announcement.permissions import IsOwner
from apps.announcement.serializers import (
    AnnouncementAPISerializer,
)


class MyPaginationClass(PageNumberPagination):
    page_size = 4

    def get_paginated_response(self, data):
        for i in range(self.page_size):
            description = data[i]['description']
            if len(description) > 10:
                data[i]['description'] = description[:10] + '...'
        data[0]['extra'] = 'This is the first object on page'
        return super().get_paginated_response(data=data)


class ReaderAnnouncementsAPIView(ListAPIView):
    queryset = AnnouncementModel.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = AnnouncementAPISerializer
    pagination_class = MyPaginationClass

    def get_queryset(self):
        price = self.request.query_params.get('price')
        queryset = super().get_queryset()
        if price:
            price_from, price_to = price.split('-')
            queryset = queryset.filter(price__gte=price_from,
                                       price__lte=price_to)
        return queryset


class OwnerAnnouncementsViewSet(viewsets.ModelViewSet):
    serializer_class = AnnouncementAPISerializer
    queryset = AnnouncementModel.objects.all()
    permission_classes = (IsAuthenticated, IsOwner, )

    def get_queryset(self):
        return AnnouncementModel.objects.filter(
            author=self.request.user
        )

    @action(detail=False, methods=['get'])   # /new?t=hour
    def new(self, request, pk=None):
        t = request.query_params.get('t')
        queryset = self.get_queryset()
        if t:
            if t == 'hour':
                start_time = timezone.now() - timedelta(hours=1)
            elif t == 'week':
                start_time = timezone.now() - timedelta(weeks=1)
            elif t == 'minutes':
                start_time = timezone.now() - timedelta(minutes=1)
        else:
            start_time = timezone.now() - timedelta(days=1)
        queryset = queryset.filter(created_at__gte=start_time)
        serializer = AnnouncementAPISerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])           # /search/?q=hello
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q) |
                                   Q(description__icontains=q))
        serializer = AnnouncementAPISerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




