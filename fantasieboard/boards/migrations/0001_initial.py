# Generated by Django 3.2.9 on 2022-01-14 18:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('pinned', models.BooleanField(default=False)),
                ('written_on', models.DateTimeField(auto_now=True)),
                ('rich_txt', models.TextField(default=' ', max_length=400)),
                ('author_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('community_name', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('written_on', models.DateTimeField(auto_now=True)),
                ('rich_txt', models.TextField(default=' ', max_length=100)),
                ('article_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boards.articles')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='articles',
            name='community_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boards.community'),
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boards.articles')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('article_id', 'user_id')},
            },
        ),
        migrations.CreateModel(
            name='Community_moderator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('community_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boards.community')),
            ],
            options={
                'unique_together': {('community_id', 'admin_id')},
            },
        ),
    ]
