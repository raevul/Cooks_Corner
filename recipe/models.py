from django.db import models

from user.models import AuthorProfile


class Category(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    title = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Recipe(models.Model):
    difficulties = (
        ('easy', 'easy'),
        ('medium', 'medium'),
        ('hard', 'hard'),
    )
    title = models.CharField(max_length=70)
    image = models.FileField("Image", upload_to="Recipe image")
    description = models.TextField(max_length=300, null=True, blank=True)
    time = models.CharField(max_length=10, null=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name='recipe')
    ingredient = models.CharField()
    author = models.ForeignKey(AuthorProfile, on_delete=models.CASCADE)
    difficulty = models.CharField(choices=difficulties, max_length=50)

    def __str__(self):
        return self.title
