# Generated by Django 4.0.4 on 2023-02-19 20:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0013_alter_module_lecturer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='module_id',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='webpage.module'),
        ),
    ]