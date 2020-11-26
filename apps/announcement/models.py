from django.db import models
from django.contrib.auth import get_user_model
from apps.category.models import Category

User = get_user_model()


class AnnouncementModel(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,  decimal_places=2
    )
    category = models.ForeignKey(
        Category, related_name='announcements',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User, related_name='announcements', on_delete=models.CASCADE, null=True
    )

    def __str__(self):
        return self.title






