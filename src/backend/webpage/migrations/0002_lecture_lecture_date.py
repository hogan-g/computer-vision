# Generated by Django 4.0.4 on 2023-01-20 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='lecture_date',
            field=models.DateField(default='2020-01-01'),
        ),
    ]