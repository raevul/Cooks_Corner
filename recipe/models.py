from django.db import models

from user.models import AuthorProfile


class Category(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Recipe(models.Model):
    difficulties = (
        ('easy', 'easy'),
        ('medium', 'medium'),
        ('hard', 'hard'),
    )
    title = models.CharField(max_length=70)
    image = models.FileField("Image", upload_to="recipe image")
    description = models.TextField(max_length=300, null=True)
    ingredient = models.CharField(max_length=60)
    unit = models.PositiveIntegerField("Unit", default=0)
    time = models.CharField(max_length=10, null=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name='recipe')
    author = models.ForeignKey(AuthorProfile, on_delete=models.CASCADE)
    difficulty = models.CharField(choices=difficulties, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
