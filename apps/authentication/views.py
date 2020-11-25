from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.authentication.serializers import (
    RegisterApiSerializer, LoginSerializer)
from apps.authentication.tasks import send_notification_task

User = get_user_model()


class RegisterApiView(APIView):
    def post(self, request):
        serializer = RegisterApiSerializer(
            data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                #TODO add send message with celery
                send_notification_task.delay(user=user.id, seconds=30)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )


class ActivationView(View):

    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True

            user.activation_code = ''
            user.save()
            return render(request, 'account/index.html', {})

        except User.DoesNotExist:
            return render(request, 'account/link_exp.html', {})


class LoginApiView(TokenObtainPairView):
    serializer_class = LoginSerializer


