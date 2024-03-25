from django.db import models

from user.models import AuthorProfile


class Recipe(models.Model):
    DIFFICULTIES = (
        ('easy', 'easy'),
        ('medium', 'medium'),
        ('hard', 'hard'),
    )
    CATEGORIES = (
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner')
    )
    title = models.CharField(max_length=70)
    image = models.FileField("Image", upload_to='Recipe image')
    description = models.TextField(max_length=800, null=True, blank=True)
    time = models.CharField(max_length=10, null=True)
    category = models.CharField(choices=CATEGORIES, max_length=30)
    ingredients = models.TextField(max_length=500)
    author = models.ForeignKey(AuthorProfile, on_delete=models.CASCADE, related_name='recipes')
    difficulty = models.CharField(choices=DIFFICULTIES, max_length=30)

    def __str__(self):
        return self.title
