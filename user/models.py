from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class AuthorProfile(models.Model):
    name = models.CharField(max_length=50)
    bio = models.TextField(max_length=250, null=True)
    email = models.EmailField(unique=True)
    image = models.FileField("Author image", upload_to="Author image", null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="author")

    def __str__(self):
        return f"This {self.name} profile"
