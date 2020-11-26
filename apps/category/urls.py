from django.urls import path
from . import views

urlpatterns = [
    path('', views.CategoryApiView.as_view()),
]

