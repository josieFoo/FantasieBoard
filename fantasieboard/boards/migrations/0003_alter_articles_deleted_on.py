# Generated by Django 3.2.9 on 2022-03-08 16:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0002_auto_20220308_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='deleted_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
