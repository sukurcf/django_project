# Generated by Django 2.0.7 on 2018-07-23 08:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('djangobin', '0005_auto_20180723_1346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='snippet',
            name='author',
        ),
        migrations.AddField(
            model_name='snippet',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
