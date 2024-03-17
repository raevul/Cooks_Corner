from django.db import models
from django.contrib.auth.models import User


class AuthorProfile(models.Model):
    name = models.CharField(max_length=50)
    bio = models.TextField(max_length=250)
    image = models.FileField("Author image", upload_to="Author image")
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"This {self.name} profile"
