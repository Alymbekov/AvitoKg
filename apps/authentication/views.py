from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.authentication.send_mail import send_confirmation_email
from apps.authentication.serializers import RegisterApiSerializer

User = get_user_model()


class RegisterApiView(APIView):
    def post(self, request):
        serializer = RegisterApiSerializer(
            data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                #TODO add send message with celery
                send_confirmation_email(user)
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





