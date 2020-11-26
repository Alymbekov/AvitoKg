from django.shortcuts import render
from rest_framework.generics import(
    ListAPIView,
)
from .serializers import CategoryAPISerializer
from apps.category.models import Category


class CategoryApiView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryAPISerializer
