# Generated by Django 4.0.4 on 2023-01-27 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0004_alter_module_lecturer_delete_lecturer'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='student_count',
            field=models.IntegerField(default=1),
        ),
    ]
