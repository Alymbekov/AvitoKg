from rest_framework import serializers

from apps.announcement.models import AnnouncementModel
from apps.category.serializers import CategoryAPISerializer


class AnnouncementAPISerializer(serializers.ModelSerializer):
    category = CategoryAPISerializer(many=False, read_only=True)
    some = serializers.SerializerMethodField()

    class Meta:
        model = AnnouncementModel
        fields = (
            'id', 'title', 'description', 'price', 'author', 'category', 'some'
        )

    def get_some(self, obj):
        print(obj)
        return "Hello world"

