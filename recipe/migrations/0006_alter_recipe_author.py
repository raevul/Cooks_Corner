# Generated by Django 5.0.3 on 2024-03-22 16:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0005_alter_recipe_image'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to='user.authorprofile'),
        ),
    ]