# Generated by Django 4.0.4 on 2023-01-27 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0005_module_student_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='time',
            field=models.TimeField(default='12:00'),
        ),
    ]
