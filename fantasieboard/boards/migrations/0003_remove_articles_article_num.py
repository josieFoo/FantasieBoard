# Generated by Django 3.2.9 on 2021-12-16 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0002_auto_20211216_1318'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articles',
            name='article_num',
        ),
    ]
