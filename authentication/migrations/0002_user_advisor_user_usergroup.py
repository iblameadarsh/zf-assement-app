# Generated by Django 4.1 on 2023-10-09 05:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='advisor',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='usergroup',
            field=models.CharField(choices=[('Co', 'Consumer'), ('Ad', 'Advisor')], default='Cu', max_length=56),
        ),
    ]
