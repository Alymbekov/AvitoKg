from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.RegisterApiView.as_view()),
    path('login/', views.LoginApiView.as_view()),
    path('activate/<uuid:activation_code>/', views.ActivationView.as_view(), name='activate_account'),
]