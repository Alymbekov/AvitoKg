from rest_framework import serializers

from django.contrib.auth import get_user_model

User = get_user_model()

USER_TYPE_CHOICES = (
    ('owner', 'Owner'),
    ('reader', 'Reader'),
)


class RegisterApiSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=6, required=True,
        write_only=True)
    password_confirmation = serializers.CharField(
        min_length=6, required=True,
        write_only=True)
    user_type = serializers.ChoiceField(choices=USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = (
            'email', 'password',
            'password_confirmation',
            'user_type'
        )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('User with given email already exists!!!')
        return value

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmation  = attrs.pop('password_confirmation')

        if password != password_confirmation:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user






