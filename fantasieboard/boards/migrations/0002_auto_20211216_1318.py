# Generated by Django 3.2.9 on 2021-12-16 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='article_num',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='users',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]
