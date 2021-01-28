from django.contrib.auth.models import User
from django.db import models


class Userpreference(models.Model):
    user = models.OneToOneField(
        to=User, on_delete=models.CASCADE, related_name="preferences")
    currency = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Userpreferenc"
        verbose_name_plural = "Userpreferencs"

    def __str__(self):
        return f"{self.user.username}'s preferences"
